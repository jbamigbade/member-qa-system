#!/bin/bash
echo "=== API TEST SCRIPT ==="
echo "Server should be running in another terminal on port 5000"
echo ""

echo "1. Health Check:"
curl -s "http://localhost:5000/health" | python3 -m json.tool
echo ""

echo "2. Members:"
curl -s "http://localhost:5000/members" | python3 -m json.tool
echo ""

echo "3. Example Questions:"
curl -s "http://localhost:5000/ask?question=When%20is%20Layla%20planning%20her%20trip%20to%20London?" | python3 -m json.tool
curl -s "http://localhost:5000/ask?question=How%20many%20cars%20does%20Vikram%20Desai%20have?" | python3 -m json.tool
curl -s "http://localhost:5000/ask?question=What%20are%20Amina's%20favorite%20restaurants?" | python3 -m json.tool
