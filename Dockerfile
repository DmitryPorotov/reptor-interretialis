FROM debian:bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nginx \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

RUN rm /etc/nginx/sites-enabled/default

EXPOSE 80
EXPOSE 443


CMD ["nginx", "-g", "daemon off;"]
