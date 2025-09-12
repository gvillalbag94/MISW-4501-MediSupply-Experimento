#!/bin/bash

echo "=== Probando API Gateway con Microservicio de Productos ==="
echo

# Iniciar el microservicio de productos en background
echo "Iniciando microservicio de productos..."
cd ../productos/src && pipenv run python main.py &
PRODUCTOS_PID=$!

# Esperar a que el microservicio esté listo
echo "Esperando a que el microservicio de productos esté listo..."
sleep 5

# Iniciar el API Gateway en background
echo "Iniciando API Gateway..."
cd ../../gateway/src && pipenv run python main.py &
GATEWAY_PID=$!

# Esperar a que el gateway esté listo
echo "Esperando a que el API Gateway esté listo..."
sleep 5

echo
echo "=== Health Check del Gateway ==="
curl -s http://localhost:5000/health/ | python -m json.tool

echo
echo "=== Obtener todos los productos a través del Gateway ==="
curl -s http://localhost:5000/productos | python -m json.tool

echo
echo "=== Obtener producto por ID a través del Gateway ==="
curl -s http://localhost:5000/productos/1 | python -m json.tool

echo
echo "=== Obtener productos por categoría a través del Gateway ==="
curl -s http://localhost:5000/productos/categoria/electronicos | python -m json.tool

echo
echo "=== Buscar productos por nombre a través del Gateway ==="
curl -s "http://localhost:5000/productos/buscar?nombre=iPhone" | python -m json.tool

echo
echo "=== Limpiando procesos ==="
kill $GATEWAY_PID 2>/dev/null
kill $PRODUCTOS_PID 2>/dev/null
echo "Servicios detenidos."
