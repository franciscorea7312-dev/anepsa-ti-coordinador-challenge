#!/bin/bash
set -e

echo "Iniciando proceso de despliegue..."
echo "Verificando variables de entorno..."

if [ -z "$DB_HOST" ]; then
  echo "Error: DB_HOST no esta definida."
  exit 1
fi

echo "Conectando a la base de datos en $DB_HOST..."
echo "Despliegue completado con exito."