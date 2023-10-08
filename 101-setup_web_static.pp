#sets up your web servers for the deployment of web_static
$data_test_dirs = ['/data/', '/data/web_static/',
                  '/data/web_static/releases/',
                  '/data/web_static/shared/',
                  '/data/web_static/releases/test/']

$test_file = '/data/web_static/releases/test/index.html'
$symlink = '/data/web_static/current'

package { 'nginx':
  ensure => 'installed',
}

file { $data_test_dirs:
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { $test_file:
  ensure  => 'file',
  content => "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
  </html>",
  require => File[$data_test_dirs],
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file {
  $symlink:
  ensure  => 'link',
  target  => '/data/web_static/releases/test/',
  require => File[$test_file],
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file {
  '/etc/nginx/sites-available/default':
  ensure  => 'present',
  content => "server {
        listen 80 default_server;
        listen [::]:80 default_server;
        add_header X-Served-By ${HOSTNAME};
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
	}",
}

exec { 'restart_nginx':
  command => 'sudo service nginx restart',
  path    => ['/usr/sbin', '/usr/bin', '/sbin', '/bin'],
  require => File['/etc/nginx/sites-available/default'],
}
