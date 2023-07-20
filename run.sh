#!/bin/bash

#sudo -E python3 server.py
sudo -E /home/tsuts/.local/bin/gunicorn -b 0.0.0.0:443 --certfile=/etc/letsencrypt/live/mobile-federated-learning.com/fullchain.pem --keyfile=/etc/letsencrypt/live/mobile-federated-learning.com/privkey.pem server:app