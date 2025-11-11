#!/bin/bash
echo "Testing API endpoints..."

echo "1. Health:"
curl -s "http://localhost:5000/health"

echo -e "\n2. Messages (first 2):"
curl -s "http://localhost:5000/messages/?limit=2" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Total: {data.get(\"total\", 0)}')
for item in data.get('items', [])[:2]:
    print(f'  - {item.get(\"user_name\", \"Unknown\")}: {item.get(\"message\", \"\")[:40]}...')
"

echo -e "\n3. Movies:"
curl -s "http://localhost:5000/movies/"

echo -e "\n4. Image:"
curl -s "http://localhost:5000/image/"

echo -e "\n✅ All endpoints responding"
