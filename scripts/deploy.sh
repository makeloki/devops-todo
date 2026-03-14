#!/bin/bash

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}🚀 DevOps ToDo Deployment Script${NC}"
echo -e "${GREEN}================================${NC}"

# Проверка наличия Docker
echo -e "\n${YELLOW}🔍 Проверка Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker не установлен!${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Docker установлен${NC}"
fi

# Проверка наличия Docker Compose
echo -e "\n${YELLOW}🔍 Проверка Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose не установлен!${NC}"
    exit 1
else
    echo -e "${GREEN}✅ Docker Compose установлен${NC}"
fi

# Остановка старых контейнеров
echo -e "\n${YELLOW}🛑 Остановка старых контейнеров...${NC}"
docker-compose down

# Сборка и запуск
echo -e "\n${YELLOW}🏗️  Сборка и запуск контейнеров...${NC}"
docker-compose up -d --build

# Проверка статуса
echo -e "\n${YELLOW}📊 Проверка статуса...${NC}"
sleep 5
if curl -s http://localhost > /dev/null; then
    echo -e "${GREEN}✅ Приложение успешно запущено!${NC}"
    echo -e "${GREEN}🌐 Открой в браузере: http://localhost${NC}"
else
    echo -e "${RED}❌ Что-то пошло не так. Проверь логи:${NC}"
    echo -e "${YELLOW}docker-compose logs app${NC}"
    echo -e "${YELLOW}docker-compose logs nginx${NC}"
fi

# Показываем информацию о контейнерах
echo -e "\n${YELLOW}📦 Запущенные контейнеры:${NC}"
docker-compose ps

echo -e "\n${GREEN}✨ Готово!${NC}"
