# FROM node:latest
# WORKDIR /app
# ADD . .
# RUN yarn install
# CMD node index.js

# The below method is way faster

FROM node:alpine
WORKDIR /app
ADD package*.json ./
RUN yarn install
ADD . .
CMD node index.js