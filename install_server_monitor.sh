#!/bin/bash

echo "=== Début de l'installation ==="

# Met à jour le système
echo "Mise à jour des paquets..."
sudo apt update -y && sudo apt upgrade -y

# Installe Python et pip
echo "Installation de Python et pip..."
sudo apt install -y python3 python3-pip

# Installe Flask
echo "Installation de Flask..."
pip3 install flask

# Télécharge le script de monitoring
echo "Téléchargement du script server_monitor.py..."
curl -o /opt/server_monitor.py https://votre-domaine.com/server_monitor.py
chmod +x /opt/server_monitor.py

# Crée un service systemd
echo "Configuration du service systemd..."
cat <<EOF | sudo tee /etc/systemd/system/server_monitor.service
[Unit]
Description=Server Monitor Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/server_monitor.py
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

echo "=== Installation terminée ==="
echo "Le script server_monitor est maintenant en cours d'exécution."