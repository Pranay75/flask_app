#!/bin/bash
set -e

sudo apt install nginx
sudo apt install python3
sudo apt install python3.10-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Systemd Service
echo "Creating systemd service..."
sudo tee /etc/systemd/system/question-panel-app.service << EOF
[Service]
User=$USER
Group=www-data
WorkingDirectory=$PWD
Environment="PATH=$PWD/venv/bin"
ExecStart=$PWD/venv/bin/gunicorn -w 3 --bind unix:app.sock -m 007 wsgi:app
Restart=always
[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable app
# Nginx config
echo "Creating nginx server..."
sudo tee /etc/nginx/sites-available/question-panel-app << EOF
server {
listen 80;
server_name question-panel;

location / {
  include proxy_params;
  proxy_pass http://unix:$PWD/app.sock;
  proxy_set_header Host \$http_host;
  proxy_set_header X-Real-IP \$remote_addr;
  proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto \$scheme;
    }

}
EOF


sudo ln -s /etc/nginx/sites-available/question-panel-app /etc/nginx/sites-enabled
sudo chmod 775 -R ./
sudo chmod 775 -R ../
sudo nginx -t && sudo nginx -s reload && \
sudo systemctl restart nginx