FROM node:0.12
RUN useradd node -u 1001 && mkdir /tmp/node
USER 1001
WORKDIR /tmp/node
