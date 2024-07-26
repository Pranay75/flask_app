#!/bin/bash
set -e

sudo apt-get update
sudo apt install nginx python3 python3-pip virtualenv -y
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

# Create .env
echo
echo "Creating .env file..."
core_env_file=".env"
if [[ ! -f $core_env_file ]]; then
    cp .env.example $core_env_file
fi

generate_key() {
    local chars='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-'
    tr -dc "$chars" < /dev/urandom | head -c "24"
}

SECRET_KEY=$(generate_key)
sed -i "s/^SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" $core_env_file

ADMIN_USERNAME=$(grep "^ADMIN_USERNAME=" $core_env_file | cut -d'=' -f2)
read -p "Enter the username for the admin user [default: $ADMIN_USERNAME]: " ADMIN_USERNAME
if [[ -n "$ADMIN_USERNAME" ]]; then
    sed -i "s/^ADMIN_USERNAME=.*/ADMIN_USERNAME=$ADMIN_USERNAME/" $core_env_file
fi

ADMIN_PASSWORD=$(grep "^ADMIN_PASSWORD=" $core_env_file | cut -d'=' -f2)
read -p "Enter the password for the admin user [default: $ADMIN_PASSWORD]: " ADMIN_PASSWORD
if [[ -n "$ADMIN_PASSWORD" ]]; then
    sed -i "s/^ADMIN_PASSWORD=.*/ADMIN_PASSWORD=$ADMIN_PASSWORD/" $core_env_file
fi