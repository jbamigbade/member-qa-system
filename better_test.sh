#!/bin/bash
echo "=== BETTER API TEST ==="
echo "======================="

BASE_URL="http://localhost:3000"

echo "1. Health Check:"
curl -s "$BASE_URL/health" | python3 -m json.tool
echo ""

echo "2. Available Members:"
curl -s "$BASE_URL/members" | python3 -m json.tool
echo ""

echo "3. Testing Questions:"
echo "---------------------"

# Test each member specifically
members=("Sophia" "Fatima" "Armand" "Hans" "Layla" "Amina" "Vikram" "Lily" "Lorenzo" "Thiago")

for member in "${members[@]}"; do
    echo "Testing: $member"
    curl -s "$BASE_URL/ask?question=What%20did%20$member%20say?" | python3 -m json.tool
    echo ""
done

echo "4. Specific Searches:"
echo "---------------------"
curl -s "$BASE_URL/ask?question=London" | python3 -m json.tool
echo ""
curl -s "$BASE_URL/ask?question=car" | python3 -m json.tool
echo ""
curl -s "$BASE_URL/ask?question=restaurant" | python3 -m json.tool
echo ""
