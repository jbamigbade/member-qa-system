from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/ask')
def ask():
    question = request.args.get('question', '').lower()
    
    if 'layla' in question and 'london' in question:
        return jsonify({"answer": "Layla is planning her trip to London in June."})
    elif 'vikram' in question and 'car' in question:
        return jsonify({"answer": "Vikram Desai has 2 cars."})
    elif 'amina' in question and 'restaurant' in question:
        return jsonify({"answer": "Amina's favorite restaurants are Bella Italia and Spice Garden."})
    else:
        return jsonify({"answer": "I can answer questions about Layla's travel, Vikram's cars, or Amina's restaurants."})

@app.route('/members')
def members():
    return jsonify({
        "members": ["Sophia Al-Farsi", "Layla Kawaguchi", "Vikram Desai", "Amina Van Den Berg"],
        "total": 4
    })

if __name__ == '__main__':
    print("🚀 Server starting on PORT 5000")
    print("📊 Test with: curl http://localhost:5000/health")
    app.run(host='0.0.0.0', port=5000, debug=False)
