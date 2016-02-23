FROM node:0.12
RUN useradd node -u 1001 && mkdir /home/node && chown -R 1001:0 /home/node
USER 1001
WORKDIR /home/node
