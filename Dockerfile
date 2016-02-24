FROM node:0.12
RUN useradd node -u 1001 && mkdir /home/node && chown -R 1001:0 /home/node && npm install -g grunt-cli bower
USER 1001
WORKDIR /home/node
