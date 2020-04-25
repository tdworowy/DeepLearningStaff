# Dockerfile
FROM node:latest
COPY . .
WORKDIR "/dashboard"
RUN npm install
RUN npm audit fix
CMD [ "npm", "start" ]