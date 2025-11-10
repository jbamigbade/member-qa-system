#!/bin/bash
echo "=== FINAL API TEST ==="
echo "======================"

echo "1. Health Check:"
curl -s "http://localhost:3000/health" | python3 -m json.tool
echo ""

echo "2. Available Members:"
curl -s "http://localhost:3000/members" | python3 -m json.tool
echo ""

echo "3. Testing Questions:"
echo "---------------------"

questions=(
    "What is Sophia planning?"
    "When is Layla going to London?"
    "How many cars does Vikram have?"
    "What are Amina's favorite restaurants?"
    "What does Fatima want?"
    "What is Armand planning?"
    "How many cars does Hans have?"
    "When is Lily going to London?"
)

for question in "${questions[@]}"; do
    echo "Q: $question"
    encoded_question=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$question'))")
    curl -s "http://localhost:3000/ask?question=$encoded_question" | python3 -m json.tool
    echo ""
done
