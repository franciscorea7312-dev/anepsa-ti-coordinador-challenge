New-Item -ItemType Directory -Path "scripts" -Force
Set-Content -Path "scripts/deploy.sh" -Value '#!/bin/bash
echo "Iniciando despliegue en Producción..."
echo "Servidor BD: $DB_HOST"
echo "Usuario BD: $DB_USER"
echo "Despliegue completado con exito."' -Encoding UTF8