#!/bin/bash

# Test script for Provedores microservice
BASE_URL="http://localhost:5003"

echo "Testing Provedores Microservice"
echo "================================"

# Test health endpoint
echo "1. Testing health endpoint..."
curl -s "$BASE_URL/health" | jq .
echo ""

# Test get all provedores
echo "2. Testing get all provedores..."
curl -s "$BASE_URL/provedores" | jq .
echo ""

# Test get provedor by ID
echo "3. Testing get provedor by ID (ID: 1)..."
curl -s "$BASE_URL/provedores/1" | jq .
echo ""

# Test get provedor by NIT
echo "4. Testing get provedor by NIT (NIT: 900123456)..."
curl -s "$BASE_URL/provedores/nit/900123456" | jq .
echo ""

# Test get provedores by country
echo "5. Testing get provedores by country (Colombia)..."
curl -s "$BASE_URL/provedores/pais/colombia" | jq .
echo ""

# Test search provedores by name
echo "6. Testing search provedores by name (Tecnología)..."
curl -s "$BASE_URL/provedores/buscar?nombre=Tecnología" | jq .
echo ""

echo "All tests completed!"
