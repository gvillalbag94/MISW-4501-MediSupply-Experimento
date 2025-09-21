#!/bin/bash

echo "=== Probando Microservicio de Productos ==="
echo

# Iniciar el microservicio en background
echo "Iniciando microservicio..."
cd src && pipenv run python main.py &
MICROSERVICE_PID=$!

# Esperar a que el microservicio esté listo
echo "Esperando a que el microservicio esté listo..."
sleep 5

echo
echo "=== Health Check ==="
curl -s http://localhost:6001/health | python -m json.tool

echo
echo "=== Obtener todos los productos ==="
curl -s http://localhost:6001/productos | python -m json.tool

echo
echo "=== Obtener producto por ID ==="
curl -s http://localhost:6001/productos/1 | python -m json.tool

echo
echo "=== Obtener productos por categoría (electronicos) ==="
curl -s http://localhost:6001/productos/categoria/electronicos | python -m json.tool

echo
echo "=== Buscar productos por nombre (iPhone) ==="
curl -s "http://localhost:6001/productos/buscar?nombre=iPhone" | python -m json.tool

echo
echo "=== Limpiando procesos ==="
kill $MICROSERVICE_PID 2>/dev/null
echo "Microservicio detenido."
