FROM node:10
WORKDIR /usr/src/app
COPY ./package.json /usr/src/app/
RUN npm i npm@latest -g
RUN npm install
COPY . /usr/src/app/
ARG env=prod
CMD ["npm", "start"]