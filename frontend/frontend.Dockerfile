# 1. Этап сборки (необязательно для dev, но оставим для примера)
FROM node:24-alpine AS builder

WORKDIR /app

# Копируем только package.json и package-lock.json
COPY frontend/package*.json ./

# Устанавливаем зависимости без dev (можно убрать --omit=dev, если нужен dev сервер)
RUN npm install

# Копируем исходники
COPY frontend/ ./

# 2. Этап запуска
FROM node:24-alpine

WORKDIR /app

# Копируем весь билд/проект из builder
COPY --from=builder /app /app

# Открываем порт dev-сервера
EXPOSE 3000

# Запускаем React dev server
CMD ["npm", "start"]
