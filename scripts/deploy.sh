#!/bin/bash
set -e

echo "Iniciando proceso de despliegue..."
echo "Verificando variables de entorno..."

# Si la variable de entorno no viene de GitHub Secrets, asigna un valor por defecto
DB_HOST=${DB_HOST:-"localhost"}
DB_USER=${DB_USER:-"admin"}

echo "Conectando a la base de datos en $DB_HOST..."
echo "Ejecutando migraciones de base de datos..."
echo "Despliegue completado con éxito."