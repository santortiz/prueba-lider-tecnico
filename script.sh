#!/bin/bash

# Carpeta raíz del proyecto (ajústala si es necesario)
ROOT_DIR="/home/sant/orquestia/prueba-lider-tecnico"

# Archivo de salida
OUTPUT_FILE="scripts_dump.txt"

# Limpia el archivo si ya existe
> "$OUTPUT_FILE"

# Encuentra todos los archivos .py excluyendo el directorio .venv
find "$ROOT_DIR" -type f -name "*.py" ! -path "$ROOT_DIR/.venv/*" | while read -r filepath; do
  echo "$filepath" >> "$OUTPUT_FILE"
  echo "" >> "$OUTPUT_FILE"
  cat "$filepath" >> "$OUTPUT_FILE"
  echo -e "\n\n" >> "$OUTPUT_FILE"
done

echo "Todos los scripts han sido escritos en $OUTPUT_FILE"
