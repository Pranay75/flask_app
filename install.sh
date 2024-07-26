#!/bin/bash
set -e

sudo apt-get update
sudo apt install vim nginx python3 python3-pip virtualenv -y
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Systemd Service
echo "Creating systemd service..."
user=$USER
sudo tee /etc/systemd/system/question-panel-app.service << EOF
[Service]
User=$user
WorkingDirectory=$PWD
Environment="PATH=$PWD/venv/bin"
ExecStart=$PWD/venv/bin/gunicorn -w 3 --bind 127.0.0.1:5963 app:app
Restart=always
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable question-panel-app
# Nginx config
echo "Creating nginx server..."
sudo tee /etc/nginx/sites-available/question-panel-app << EOF
server {
listen 80;
server_name question-panel;

location / {
  include proxy_params;
  proxy_pass http://127.0.0.1:5963/;
  proxy_set_header Host \$http_host;
  proxy_set_header X-Real-IP \$remote_addr;
  proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto \$scheme;
    }

}
EOF


sudo ln -s /etc/nginx/sites-available/question-panel-app /etc/nginx/sites-enabled 
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo nginx -s reload && \
sudo systemctl restart nginx 