#!/bin/bash
echo "=== API TEST ==="
echo "Testing on: http://localhost:5000"
echo ""

echo "1. Health:"
curl -s "http://localhost:5000/health"
echo -e "\n"

echo "2. Members:"
curl -s "http://localhost:5000/members"
echo -e "\n"

echo "3. Required Questions:"
echo "Layla London:"
curl -s "http://localhost:5000/ask?question=When%20is%20Layla%20planning%20her%20trip%20to%20London?"
echo -e "\n"

echo "Vikram Cars:"
curl -s "http://localhost:5000/ask?question=How%20many%20cars%20does%20Vikram%20Desai%20have?"
echo -e "\n"

echo "Amina Restaurants:"
curl -s "http://localhost:5000/ask?question=What%20are%20Amina's%20favorite%20restaurants?"
echo -e "\n"
