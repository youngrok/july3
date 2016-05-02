% for web_server_name in web_server_names:
server {
	listen 80;
    server_name www.${web_server_name};
    access_log  /var/log/nginx/${project_name}.log;
    location /static {
        alias /home/ubuntu/static/${project_name};
    }
    location / {
        uwsgi_pass 127.0.0.1:3031;
        include uwsgi_params;
    }
}

server {
    listen       80;
    server_name  ${web_server_name};
    return       301 http://www.${web_server_name}$request_uri;
}

% endfor
