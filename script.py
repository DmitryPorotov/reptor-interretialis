#!/usr/bin/env python3
##################################################
# Great work with templates
# Claude knows what he is doing.


import argparse
from string import Template

parser = argparse.ArgumentParser(description="This script generates a nginx config for your domain and subdomains")
parser.add_argument("domain", help="Your domain")


args = parser.parse_args()

subdomains = ['test', 'beta', 'dev', 'www', 'www2']

subdomains = map(lambda x: x + '.' + args.domain, subdomains)

all_subdomains = ' '.join(subdomains)

template = Template('''
upstream static_servers {
    least_conn;
    server 10.0.0.21:80;
    server 10.0.0.22:80;
    server 10.0.0.23:80;
}

server {
        listen 80;
        server_name $domain $all_subdomains;
 
        # -- Security headers --------------------------------------------------
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options DENY always;
        add_header X-Content-Type-Options nosniff always;
 
        # -- Proxy defaults (inherited by all location blocks) -----------------
        proxy_http_version          1.1;
        proxy_set_header Host       $$host;
        proxy_set_header X-Real-IP  $$remote_addr;
        proxy_set_header X-Forwarded-For $$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $$scheme;
        proxy_set_header Connection "";   # required for keepalive to upstreams
        proxy_connect_timeout       10s;
        proxy_send_timeout          30s;
        proxy_read_timeout          30s;
        proxy_next_upstream         error timeout http_502 http_503 http_504;
 
 
        location / {
            proxy_pass http://static_servers;
        }
 
        # ── Health check endpoint (internal use) ──────────────────────────────
        location /nginx-health {
            access_log off;
            allow 127.0.0.1;
            deny  all;
            return 200 "healthy\\n";
            add_header Content-Type text/plain;
        }
 
    }
''')

conf = template.substitute(domain=args.domain, all_subdomains=all_subdomains)

with open('nginx.conf', 'w') as f:
    f.write(conf)
