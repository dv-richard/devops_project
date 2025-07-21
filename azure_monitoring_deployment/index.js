// Import des variables d'environnement
require('dotenv').config();

// Import des modules
const express = require('express');
const sql = require('mssql');
const redis = require('redis');
const appInsights = require('applicationinsights');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');

// Initialisation Application Insights avec clé d'instrumentation
appInsights.setup(process.env.APPINSIGHTS_INSTRUMENTATIONKEY).start();
const client = appInsights.defaultClient;

// Création de l'application Express
const app = express();
app.use(helmet());
app.use(express.json({ limit: '10mb' }));

// Rate Limiting sur l'API de paiement
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100
});
app.use('/api/', limiter);

// Configuration SQL sécurisée
const config = {
  sql: {
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    server: process.env.DB_SERVER,
    options: {
      encrypt: true,
      trustServerCertificate: false
    },
    pool: {
      max: 10,
      min: 0,
      idleTimeoutMillis: 30000
    }
  }
};

// Création du client Redis global
const redisClient = redis.createClient({
  socket: {
    host: process.env.REDIS_HOST,
    port: 6380,
    tls: true
  },
  password: process.env.REDIS_PASSWORD
});

redisClient.connect().catch(console.error);

// Gestion des erreurs Redis (optionnel mais recommandé)
redisClient.on('error', (err) => {
  console.error('Redis Error:', err);
  client.trackException({ exception: err });
});

// Endpoint /health
app.get('/health', async (req, res) => {
  const healthCheck = {
    uptime: process.uptime(),
    timestamp: Date.now(),
    status: 'OK'
  };

  try {
    const pool = await sql.connect(config.sql);
    await pool.request().query('SELECT 1');
    healthCheck.database = 'Connected';

    await redisClient.ping();
    healthCheck.cache = 'Connected';

    res.status(200).json(healthCheck);
  } catch (error) {
    healthCheck.status = 'ERROR';
    healthCheck.error = error.message;

    client.trackException({ exception: error });
    client.trackMetric({ name: 'HealthCheck.Failure', value: 1 });

    res.status(503).json(healthCheck);
  }
});

// Endpoint /api/payments
app.post('/api/payments', async (req, res) => {
  const startTime = Date.now();
  const { amount, currency, merchantId } = req.body;

  try {
    client.trackEvent({
      name: 'PaymentInitiated',
      properties: { merchantId, currency, amount: amount.toString() }
    });

    const pool = await sql.connect(config.sql);
    const result = await pool.request()
      .input('amount', sql.Decimal(10, 2), amount)
      .input('currency', sql.NVarChar, currency)
      .input('merchantId', sql.NVarChar, merchantId)
      .query(`
        INSERT INTO Payments (Amount, Currency, MerchantId, Status, CreatedAt)
        VALUES (@amount, @currency, @merchantId, 'COMPLETED', GETDATE());
        SELECT SCOPE_IDENTITY() as PaymentId;
      `);

    const paymentId = result.recordset[0].PaymentId;

    const duration = Date.now() - startTime;
    client.trackMetric({ name: 'PaymentProcessing.Duration', value: duration });
    client.trackMetric({ name: 'PaymentProcessing.Success', value: 1 });

    res.status(201).json({
      paymentId,
      status: 'COMPLETED',
      amount,
      currency,
      processedAt: new Date().toISOString()
    });
  } catch (error) {
    const duration = Date.now() - startTime;

    client.trackException({
      exception: error,
      properties: { merchantId, amount: amount?.toString() }
    });
    client.trackMetric({ name: 'PaymentProcessing.Error', value: 1 });
    client.trackMetric({ name: 'PaymentProcessing.Duration', value: duration });

    res.status(500).json({
      error: 'Payment processing failed',
      timestamp: new Date().toISOString()
    });
  }
});

// Démarrage du serveur
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`TechMart Payment API running on port ${PORT}`);
  client.trackEvent({ name: 'ApplicationStarted', properties: { port: PORT.toString() } });
});
