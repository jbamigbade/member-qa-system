# API Service

## Endpoints
- GET /messages/ - Paginated messages
- GET /movies/ - Movies list
- GET /image/ - Random image
- GET /health - Health check

## Local Development
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py

**test.sh:**
```bash
cat > test.sh << 'EOF'
#!/bin/bash
echo "Testing API endpoints..."

echo "1. Health:"
curl -s "http://localhost:5000/health"

echo -e "\n2. Messages:"
curl -s "http://localhost:5000/messages/?limit=2"

echo -e "\n3. Movies:"
curl -s "http://localhost:5000/movies/"

echo -e "\n4. Image:"
curl -s "http://localhost:5000/image/"

echo -e "\nDone."
