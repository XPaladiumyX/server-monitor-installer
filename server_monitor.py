from flask import Flask, jsonify, request
import psutil
import socket
import platform
import time

app = Flask(__name__)

# Clé d'authentification pour sécuriser les requêtes
AUTH_TOKEN = "ChangeThisByYourTokenForSecurityPurposes"

# Fonction pour obtenir les informations système
def get_system_info():
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "ram_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "uptime": time.time() - psutil.boot_time(),
    }

# Route pour récupérer les informations système
@app.route('/info', methods=['GET'])
def info():
    # Vérification du token d'authentification
    token = request.headers.get('Authorization')
    if token != f"Bearer {AUTH_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    # Retourne les informations système
    return jsonify(get_system_info())

# Route de test
@app.route('/')
def home():
    return "Server monitoring script is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
