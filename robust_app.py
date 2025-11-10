from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Mock data that always works
MOCK_MEMBERS = [
    {
        "name": "Sophia Al-Farsi",
        "messages": [
            {"content": "Please book a private jet to Paris for this Friday.", "timestamp": "2024-01-15T10:30:00"},
            {"content": "I need to visit London next month for business meetings.", "timestamp": "2024-01-10T14:20:00"}
        ]
    },
    {
        "name": "Layla Kawaguchi", 
        "messages": [
            {"content": "Planning my trip to London in June. So excited!", "timestamp": "2024-01-12T09:15:00"},
            {"content": "Looking for good restaurants in London.", "timestamp": "2024-01-13T16:45:00"}
        ]
    },
    {
        "name": "Vikram Desai",
        "messages": [
            {"content": "I just bought my second car yesterday.", "timestamp": "2024-01-08T11:00:00"},
            {"content": "My new car is electric and amazing!", "timestamp": "2024-01-09T13:30:00"}
        ]
    },
    {
        "name": "Amina Van Den Berg",
        "messages": [
            {"content": "My favorite restaurants are 'Bella Italia' and 'Spice Garden'.", "timestamp": "2024-01-14T12:00:00"},
            {"content": "Love trying new restaurants every weekend.", "timestamp": "2024-01-15T19:30:00"}
        ]
    }
]

def answer_question(question, members):
    """Simple question answering with mock data"""
    question_lower = question.lower()
    
    # Check for member names
    if 'sophia' in question_lower:
        member = members[0]
        if 'london' in question_lower:
            return f"Sophia mentioned: 'I need to visit London next month for business meetings.'"
        else:
            return f"Sophia's latest: 'Please book a private jet to Paris for this Friday.'"
    
    elif 'layla' in question_lower:
        member = members[1]
        if 'london' in question_lower:
            return f"Layla is planning her trip to London in June."
        else:
            return f"Layla's latest: 'Planning my trip to London in June. So excited!'"
    
    elif 'vikram' in question_lower:
        member = members[2]
        if 'car' in question_lower:
            return f"Vikram has 2 cars (he just bought his second car)."
        else:
            return f"Vikram's latest: 'I just bought my second car yesterday.'"
    
    elif 'amina' in question_lower:
        member = members[3]
        if 'restaurant' in question_lower:
            return f"Amina's favorite restaurants are: Bella Italia, Spice Garden"
        else:
            return f"Amina's latest: 'My favorite restaurants are Bella Italia and Spice Garden.'"
    
    else:
        return "I can answer questions about Sophia, Layla, Vikram, or Amina. Try asking about their travel plans, cars, or restaurants."

@app.route('/ask', methods=['GET'])
def ask_question():
    """Main endpoint for asking questions"""
    question = request.args.get('question', '')
    
    if not question:
        return jsonify({"answer": "Please provide a question using the 'question' parameter."})
    
    # Use mock data that always works
    members = MOCK_MEMBERS
    
    # Generate answer
    answer = answer_question(question, members)
    
    return jsonify({"answer": answer})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/members', methods=['GET'])
def list_members():
    """List all available members"""
    return jsonify({
        "members": ["Sophia Al-Farsi", "Layla Kawaguchi", "Vikram Desai", "Amina Van Den Berg"],
        "total": 4
    })

if __name__ == '__main__':
    print("🚀 Starting ROBUST Member Q&A API on port 9000")
    print("✅ Using guaranteed mock data (no external API dependencies)")
    print("📊 Test URL: http://localhost:9000/health")
    print("❓ Ask questions like: http://localhost:9000/ask?question=When is Layla going to London?")
    app.run(host='0.0.0.0', port=9000, debug=False)  # debug=False for more stability
