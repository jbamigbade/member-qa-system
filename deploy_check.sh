#!/bin/bash
echo "=== Deployment Readiness Check ==="
echo "1. Python version: $(python3 --version)"
echo "2. Files in directory:"
ls -la
echo "3. Requirements check:"
cat requirements.txt
echo "4. Procfile check:"
cat Procfile
echo "5. App.py exists: $(test -f app.py && echo 'YES' || echo 'NO')"
echo "=== Ready for Render Deployment ==="
