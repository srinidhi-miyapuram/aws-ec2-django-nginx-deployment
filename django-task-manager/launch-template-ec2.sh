# ec2-user-data.sh

#!/bin/bash

exec > >(tee /var/log/django-user-data.log | logger -t user-data -s 2>/dev/console) 2>&1

set -euxo pipefail

echo "===== USER DATA STARTED ====="

# -----------------------------
# System packages
# -----------------------------

dnf update -y

dnf install -y \
    python3.12 \
    python3.12-pip \
    nginx \
    postgresql18 \
    amazon-ssm-agent

# -----------------------------
# SSM Agent
# -----------------------------

systemctl enable amazon-ssm-agent
systemctl start amazon-ssm-agent

# -----------------------------
# Nginx
# -----------------------------

systemctl enable nginx
systemctl start nginx

# -----------------------------
# Application directory
# -----------------------------

mkdir -p /opt/my-django-app

cd /opt/my-django-app

# -----------------------------
# Download Django application
# -----------------------------

echo "Downloading Django application from S3..."

aws s3 cp \
    s3://rds-django/django-task-manager/ \
    /opt/my-django-app/ \
    --recursive

ls -la /opt/my-django-app

# -----------------------------
# Create Python virtual env
# -----------------------------

python3.12 -m venv /opt/my-django-app/venv

source /opt/my-django-app/venv/bin/activate

python -m pip install --upgrade pip

# -----------------------------
# Python dependencies
# -----------------------------

if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    pip install django gunicorn psycopg2-binary python-dotenv
fi
pip install django gunicorn psycopg2-binary python-dotenv
pip install python-dotenv

# -----------------------------
# Django environment
# -----------------------------


chmod 600 /opt/my-django-app/.env

# -----------------------------
# Check RDS connectivity
# -----------------------------

source /opt/my-django-app/.env

echo "Testing RDS connectivity..."

until PGPASSWORD="$DB_PASSWORD" psql \
    "host=$DB_HOST port=$DB_PORT dbname=$DB_NAME user=$DB_USER sslmode=require" \
    -c "SELECT 1"
do
    echo "RDS is not ready/reachable. Retrying..."
    sleep 10
done

echo "RDS connection successful."

# -----------------------------
# Django migrations
# -----------------------------

cd /opt/my-django-app

python manage.py migrate

# -----------------------------
# Nginx configuration
# -----------------------------

aws s3 cp \
    s3://rds-django/django.conf \
    /etc/nginx/conf.d/django.conf

nginx -t

systemctl restart nginx

# -----------------------------
# Static files
# -----------------------------

python manage.py collectstatic --noinput

# -----------------------------
# Gunicorn systemd service
# -----------------------------

cat > /etc/systemd/system/gunicorn.service <<EOF
[Unit]
Description=Django Gunicorn Application
After=network.target

[Service]
User=root
WorkingDirectory=/opt/my-django-app
EnvironmentFile=/opt/my-django-app/.env
Environment="PATH=/opt/my-django-app/venv/bin"
ExecStart=/opt/my-django-app/venv/bin/gunicorn \
    --workers 2 \
    --bind 127.0.0.1:8000 \
    config.wsgi:application
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable gunicorn
systemctl restart gunicorn



# -----------------------------
# Permissions for static files
# -----------------------------

chmod o+x /opt
chmod o+x /opt/my-django-app

if [ -d /opt/my-django-app/staticfiles ]; then
    chmod -R o+rX /opt/my-django-app/staticfiles
fi

# -----------------------------
# Verification
# -----------------------------

echo "===== GUNICORN STATUS ====="
systemctl status gunicorn --no-pager || true

echo "===== NGINX STATUS ====="
systemctl status nginx --no-pager || true

echo "===== PORT 8000 ====="
ss -lntp | grep 8000 || true

echo "===== USER DATA COMPLETED ====="