FROM node:0.12
RUN useradd node -u 1001 && mkdir /tmp/node && chown -R 1001:0 /tmp/node && chmod 0777 /tmp/node
USER 1001
WORKDIR /tmp/node
