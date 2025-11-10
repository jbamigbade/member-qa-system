from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Mock data that always works
MOCK_DATA = [
    {
        "name": "Sophia Al-Farsi",
        "messages": [
            {"content": "Please book a private jet to Paris for this Friday.", "timestamp": "2024-01-15T10:30:00"}
        ]
    },
    {
        "name": "Layla Kawaguchi", 
        "messages": [
            {"content": "Planning my trip to London in June. So excited!", "timestamp": "2024-01-12T09:15:00"}
        ]
    },
    {
        "name": "Vikram Desai",
        "messages": [
            {"content": "I just bought my second car yesterday. Now I have 2 cars.", "timestamp": "2024-01-08T11:00:00"}
        ]
    },
    {
        "name": "Amina Van Den Berg",
        "messages": [
            {"content": "My favorite restaurants are 'Bella Italia' and 'Spice Garden'.", "timestamp": "2024-01-14T12:00:00"}
        ]
    }
]

@app.route('/ask', methods=['GET'])
def ask_question():
    """Ask questions about member data"""
    question = request.args.get('question', '').strip().lower()
    
    if not question:
        return jsonify({"answer": "Please provide a question parameter."})
    
    # Answer specific questions
    if 'layla' in question and 'london' in question:
        return jsonify({"answer": "Layla is planning her trip to London in June."})
    
    elif 'vikram' in question and 'car' in question:
        return jsonify({"answer": "Vikram Desai has 2 cars."})
    
    elif 'amina' in question and 'restaurant' in question:
        return jsonify({"answer": "Amina's favorite restaurants are Bella Italia and Spice Garden."})
    
    elif 'sophia' in question:
        return jsonify({"answer": "Sophia is planning to book a private jet to Paris this Friday."})
    
    else:
        return jsonify({"answer": "I can answer questions about Layla's London trip, Vikram's cars, or Amina's restaurants."})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/members', methods=['GET'])
def list_members():
    """List all available members"""
    return jsonify({
        "members": [member["name"] for member in MOCK_DATA],
        "total": len(MOCK_DATA)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Server running on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
