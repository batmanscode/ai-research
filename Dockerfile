# syntax=docker/dockerfile:1

FROM nginxinc/nginx-unprivileged:stable-alpine

# The research index lives on the portfolio; this image serves papers only.
USER root
RUN rm -f /usr/share/nginx/html/index.html /usr/share/nginx/html/50x.html
USER 101

# Each destination folder becomes the paper's public path on the chosen host.
COPY graph/secure-domination-p5-free/website/index.html /usr/share/nginx/html/secure-domination-p5-free/
COPY graph/secure-domination-p5-free/website/css /usr/share/nginx/html/secure-domination-p5-free/css
COPY graph/secure-domination-p5-free/website/js /usr/share/nginx/html/secure-domination-p5-free/js

COPY biology/aggregate-chemistry-transfer/website/index.html /usr/share/nginx/html/aggregate-chemistry-transfer/
COPY biology/aggregate-chemistry-transfer/website/css /usr/share/nginx/html/aggregate-chemistry-transfer/css
COPY biology/aggregate-chemistry-transfer/website/assets /usr/share/nginx/html/aggregate-chemistry-transfer/assets

EXPOSE 8080
