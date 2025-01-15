#!/bin/bash

echo "=== Début de l'installation ==="

# Met à jour le système
echo "Mise à jour des paquets..."
sudo apt update -y && sudo apt upgrade -y

# Désactivation du dépôt PHP pour éviter les erreurs avec apt
echo "Désactivation du dépôt PHP inutile..."
sudo add-apt-repository --remove ppa:ondrej/php
sudo apt update -y

# Installe Python, pip et Gunicorn
echo "Installation de Python, pip et Gunicorn..."
sudo apt install -y python3 python3-pip
sudo pip3 install gunicorn

# Installe Flask et psutil
echo "Installation de Flask et psutil..."
sudo pip3 install flask psutil

# Télécharge le script de monitoring
echo "Téléchargement du script server_monitor.py..."
curl -o /opt/server_monitor.py https://raw.githubusercontent.com/XPaladiumyX/server-monitor-installer/main/server_monitor.py
chmod +x /opt/server_monitor.py

# Crée un service systemd pour Gunicorn
echo "Configuration du service systemd pour Gunicorn..."
cat <<EOF | sudo tee /etc/systemd/system/server_monitor.service
[Unit]
Description=Server Monitor Service
After=network.target

[Service]
ExecStart=/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:5000 server_monitor:app
WorkingDirectory=/opt
Restart=always
User=nobody
Group=nogroup

[Install]
WantedBy=multi-user.target
EOF

# Recharge systemd et active le service
echo "Activation du service..."
sudo systemctl daemon-reload
sudo systemctl enable server_monitor.service
sudo systemctl start server_monitor.service

# Vérifie si le service a démarré correctement
echo "Vérification du statut du service..."
sudo systemctl status server_monitor.service --no-pager

echo "=== Installation terminée ==="
echo "Le script server_monitor est maintenant en cours d'exécution avec Gunicorn."
