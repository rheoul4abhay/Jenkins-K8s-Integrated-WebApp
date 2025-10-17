FROM nginx:alpine



RUN mkdir -p /var/cache/nginx/client_temp && \
    chmod -R 755 /var/cache/nginx
COPY index.html /usr/share/nginx/html/index.html
COPY styles.css /usr/share/nginx/html/styles.css
COPY nginx.conf /etc/nginx/nginx.conf
