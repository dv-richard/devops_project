# checklist/models.py

from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from simple_history.models import HistoricalRecords

class Section(models.Model):
    titre = models.CharField(max_length=200, unique=True)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre', 'titre']

    def __str__(self):
        return self.titre

class TaskTemplate(models.Model):
    section     = models.ForeignKey(Section, on_delete=models.PROTECT, related_name='taches')
    nom         = models.CharField(max_length=200)
    ordre       = models.PositiveIntegerField(default=0)
    description = models.TextField(
        blank=True,
        help_text="Aide (affiché dans l'infobulle) pour cette tâche."
    )
    doc_url     = models.URLField(
        blank=True,
        help_text="Lien vers un document ou une ressource externe pour cette tâche."
    )

    class Meta:
        unique_together = [('section','nom')]
        ordering = ['section__ordre','ordre','nom']

    def __str__(self):
        return f"{self.section} -> {self.nom}"

class Checklist(models.Model):
    date        = models.DateField(default=timezone.localdate, unique=True)
    verifie_par = models.CharField("Vérifié par", max_length=200)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Checklist {self.date} ({self.verifie_par})"

class CheckItem(models.Model):
    STATUT_CHOICES = [
        ('A_VERIFIER','🔍 À vérifier'),
        ('OK',        '✅ OK'),
        ('KO',        '❌ KO'),
        ('EN_COURS',  '🔄 En cours'),
    ]

    checklist   = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='items')
    nom         = models.CharField(max_length=200)
    statut      = models.CharField(max_length=20, choices=STATUT_CHOICES, default='A_VERIFIER')
    commentaire = models.TextField(blank=True, null=True)
    verifie_par = models.CharField("Vérifié par", max_length=200, blank=True)
    # historique automatique des changements
    history     = HistoricalRecords()

    class Meta:
        ordering = ['nom']

    def __str__(self):
        return f"{self.nom} — {self.statut}"

@receiver(post_save, sender=TaskTemplate)
def add_template_to_today(sender, instance, created, **kwargs):
    """
    À chaque création ou mise à jour d'un template, assure qu'il existe
    dans la checklist du jour.
    """
    today, _ = Checklist.objects.get_or_create(date=timezone.localdate())
    CheckItem.objects.get_or_create(
        checklist=today,
        nom=instance.nom,
        defaults={'statut': 'A_VERIFIER'}
    )

@receiver(post_delete, sender=TaskTemplate)
def remove_template_from_today(sender, instance, **kwargs):
    """
    Si un template est supprimé, on le retire aussi de la checklist du jour.
    """
    try:
        today = Checklist.objects.get(date=timezone.localdate())
    except Checklist.DoesNotExist:
        return
    today.items.filter(nom=instance.nom).delete()

def is_external_user(user):
    """
    Renvoie True si l'utilisateur n'est pas un membre du personnel (staff).
    Utilisé pour restreindre l'accès à certaines fonctionnalités.
    """
    return not user.is_staff
