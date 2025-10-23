FROM nginx:alpine


RUN mkdir -p /var/cache/nginx/client_temp /var/cache/nginx/proxy_temp && \
    chown -R 1001:0 /var/cache/nginx && \
    chmod -R 775 /var/cache/nginx

COPY index.html /usr/share/nginx/html/index.html
COPY nginx.conf /etc/nginx/nginx.conf
