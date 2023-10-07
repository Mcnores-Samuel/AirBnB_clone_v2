#!/usr/bin/env bash
# sets up web servers for the deployment of web_static.

DATA_DIR="/data/"
WEBSTATIC="/data/web_static/"
RELEASES="/data/web_static/releases/"
SHARED="/data/web_static/shared/"
TEST="/data/web_static/releases/test/"
TEMP_HTML="/data/web_static/releases/test/index.html"
LINK="/data/web_static/current"

apt-get update

# Installs Nginx if it not already installed
if [ ! -x "/usr/bin/nginx" ]; then
	apt-get install -y nginx
fi

# Creates the folder /data/ if it doesn’t already exist
if [ ! -d "$DATA_DIR" ]; then
	mkdir -p "$DATA_DIR"
fi

# Creates the folder /data/web_static/ if it doesn’t already exist
if [ ! -d "$WEBSTATIC" ]; then
	mkdir "$WEBSTATIC"
fi

# Creates the folder /data/web_static/releases/ if it doesn’t already exist
if [ ! -d "$RELEASES" ]; then
	mkdir "$RELEASES"
fi

# Creates the folder /data/web_static/shared/ if it doesn’t already exist
if [ ! -d "$SHARED" ]; then
	mkdir "$SHARED"
fi

# Creates the folder /data/web_static/releases/test/ if it doesn’t already exist
if [ ! -d "$TEST" ]; then
	mkdir "$TEST"
fi

if [ ! -f "$TEMP_HTML" ]; then
	echo "Holberton School" > "$TEMP_HTML"
fi

if [ -L "$LINK" ]; then
	rm "$LINK"
fi

ln -sf "$TEST" "$LINK"
chown -R ubuntu:ubuntu "$DATA_DIR"

printf %s "server {
        listen 80 default_server;
        listen [::]:80 default_server;
        add_header X-Served-By $HOSTNAME;
	root /var/www/html;
	index index.html index.html;

	location /hbnb_static {
		alias /data/web_static/current;
		index index.html index.html;
	}

	location /redirect_me {
	        return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
	}

	error_page 404 /404.html;
	location /404.html {
	        root /var/www/nginx-html;
                internal;
	}
}
" > /etc/nginx/sites-available/default
service nginx restart
