# 1. Этап сборки
FROM node:24-slim AS builder

WORKDIR /app

# Копируем package.json и package-lock.json
COPY frontend/package*.json ./

# Устанавливаем только prod зависимости
RUN npm install --omit=dev

# Копируем исходники
COPY frontend/ ./

# Собираем production-бандл
RUN npm run build

# 2. Этап финального образа — Nginx
FROM nginx:alpine

# Удаляем дефолтный html
RUN rm -rf /usr/share/nginx/html/*

# Копируем билд
COPY --from=builder /app/build /usr/share/nginx/html

# Копируем конфиг Nginx
COPY frontend/nginx/default.conf /etc/nginx/conf.d/default.conf

# Открываем порт
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]