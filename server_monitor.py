from flask import Flask, jsonify, request, g
import psutil
import socket
import platform
import time
import logging
from datetime import datetime

app = Flask(__name__)

# Configurer les logs pour déboguer les interruptions de connexion
logging.basicConfig(level=logging.INFO)

# Clé d'authentification pour sécuriser les requêtes
AUTH_TOKEN = "ChangeThisByYourTokenForSecurityPurposes"

# Fonction pour obtenir les informations système
def get_system_info():
    boot_time = psutil.boot_time()  # Récupère l'heure du dernier démarrage
    last_restart = datetime.fromtimestamp(boot_time).strftime('%Y-%m-%d %H:%M:%S')  # Convertir en format lisible
    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_version": platform.version(),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "ram_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "uptime": time.time() - boot_time,  # Temps écoulé depuis le démarrage
        "last_restart": last_restart  # Ajouter la date du dernier redémarrage
    }

# Middleware pour désactiver le keep-alive
@app.after_request
def disable_keep_alive(response):
    response.headers["Connection"] = "close"
    return response

# Route pour récupérer les informations système
@app.route('/info', methods=['GET'])
def info():
    # Vérification du token d'authentification
    token = request.headers.get('Authorization')
    if token != f"Bearer {AUTH_TOKEN}":
        return jsonify({"error": "Unauthorized"}), 401

    try:
        # Retourne les informations système
        data = get_system_info()
        logging.info("Données envoyées : %s", data)
        return jsonify(data)
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des informations système : {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

# Route de test
@app.route('/')
def home():
    return "Server monitoring script is running!"

if __name__ == '__main__':
    # Configurer le serveur Flask avec un délai d'attente augmenté
    app.run(host='0.0.0.0', port=5000, threaded=True)
