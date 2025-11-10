#!/bin/bash
echo "=== FINAL DEMONSTRATION ==="
echo "==========================="

echo "1. Health check:"
curl -s "http://localhost:9000/health" | python3 -m json.tool

echo -e "\n2. Available members:"
curl -s "http://localhost:9000/members" | python3 -m json.tool

echo -e "\n3. REQUIRED QUESTIONS:"
echo "======================"

echo "Q: When is Layla planning her trip to London?"
curl -s "http://localhost:9000/ask?question=When%20is%20Layla%20planning%20her%20trip%20to%20London?" | python3 -m json.tool

echo -e "\nQ: How many cars does Vikram Desai have?"
curl -s "http://localhost:9000/ask?question=How%20many%20cars%20does%20Vikram%20Desai%20have?" | python3 -m json.tool

echo -e "\nQ: What are Amina's favorite restaurants?"
curl -s "http://localhost:9000/ask?question=What%20are%20Amina's%20favorite%20restaurants?" | python3 -m json.tool

echo -e "\n4. ADDITIONAL TESTS:"
echo "===================="

echo "Q: What is Sophia planning?"
curl -s "http://localhost:9000/ask?question=What%20is%20Sophia%20planning?" | python3 -m json.tool
