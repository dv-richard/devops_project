from flask import Flask, request, jsonify

app = Flask(__name__)

def convert_to_hex(value: int) -> str:
    return hex(value)

@app.route("/")
def index():
    return "Welcome to rda-devops-app! Use /hex?value=123 to convert."

@app.route("/hex")
def hex_converter():
    try:
        value = int(request.args.get("value"))
        result = convert_to_hex(value)
        return jsonify({"value": value, "hex": result})
    except (ValueError, TypeError):
        return jsonify({"error": "Please provide a valid integer in 'value' parameter"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
