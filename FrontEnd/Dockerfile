FROM node:20-alpine AS build
LABEL authors="D8ug"


ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

WORKDIR /bacon-distance
COPY ./bacon-distance/package*.json ./
RUN npm install
COPY ./bacon-distance/. ./
RUN npm run build

FROM nginx:alpine
COPY --from=build /bacon-distance/dist /usr/share/nginx/html
EXPOSE 80

