from flask import Flask, request, jsonify
import requests
import re
import os
import sys

app = Flask(__name__)

# Base URL for the data source API
API_BASE = "https://november7-730026606190.europe-west1.run.app"

def get_member_data():
    """Fetch and process real member data from the external API"""
    try:
        print("📡 Fetching data from external API...", file=sys.stderr)
        response = requests.get(f"{API_BASE}/messages", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Received {len(data.get('items', []))} messages", file=sys.stderr)
        
        # Transform API data into member-focused structure
        members = {}
        for item in data.get('items', []):
            user_name = item.get('user_name')
            message_content = item.get('message', '')
            
            if user_name and user_name not in members:
                members[user_name] = {
                    'name': user_name,
                    'messages': []
                }
            
            if user_name:
                members[user_name]['messages'].append({
                    'content': message_content,
                    'timestamp': item.get('timestamp', '')
                })
        
        # Sort messages by timestamp for each member
        for member in members.values():
            member['messages'].sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        member_list = list(members.values())
        print(f"📊 Processed {len(member_list)} members", file=sys.stderr)
        return member_list
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}", file=sys.stderr)
        return []

def extract_member_name(question):
    """Extract member name from question with fuzzy matching"""
    question_lower = question.lower()
    
    # Common name variations and their mappings
    name_patterns = {
        'layla': ['layla', 'kawaguchi'],
        'vikram': ['vikram', 'desai'],
        'amira': ['amira'],
        'sophia': ['sophia', 'al-farsi', 'alfarsi'],
        'fatima': ['fatima', 'el-tahir', 'eltahir'],
        'hans': ['hans', 'müller', 'muller'],
        'amina': ['amina', 'van den berg'],
        'armand': ['armand', 'dupont'],
        'lily': ['lily', "o'sullivan", 'osullivan'],
        'lorenzo': ['lorenzo', 'cavalli'],
        'thiago': ['thiago', 'monteiro']
    }
    
    for canonical_name, patterns in name_patterns.items():
        if any(pattern in question_lower for pattern in patterns):
            return canonical_name
    return None

def find_member_by_name(members, name):
    """Find member by name with fuzzy matching"""
    name_lower = name.lower()
    
    for member in members:
        member_name = member.get('name', '').lower()
        if name_lower in member_name or any(part in member_name for part in name_lower.split()):
            return member
    
    return None

@app.route('/')
def home():
    return jsonify({
        "message": "Member QA System API",
        "status": "running",
        "endpoints": {
            "/health": "GET - System health check",
            "/members": "GET - List all members", 
            "/ask?question=text": "GET - Ask a question about members"
        },
        "example": "Visit /ask?question=When%20is%20Layla%20planning%20her%20trip%20to%20London"
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "service": "Member QA System",
        "timestamp": "2025-11-12T08:30:00Z"
    })

@app.route('/members', methods=['GET'])
def list_members():
    """List available members"""
    try:
        members = get_member_data()
        member_names = [m['name'] for m in members]
        return jsonify({
            "members": member_names,
            "total": len(members),
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500

@app.route('/ask', methods=['GET'])
def ask_question():
    """Question-answering endpoint"""
    try:
        question = request.args.get('question', '').strip()
        
        if not question:
            return jsonify({
                "answer": "Please provide a question parameter.",
                "example": "/ask?question=When%20is%20Layla%20planning%20her%20trip%20to%20London"
            })
        
        print(f"❓ Question: {question}", file=sys.stderr)
        members = get_member_data()
        
        if not members:
            return jsonify({
                "answer": "Sorry, I couldn't fetch the member data from the external API."
            })
        
        # Extract member name from question
        member_name = extract_member_name(question)
        if not member_name:
            available_names = [m['name'] for m in members]
            return jsonify({
                "answer": f"Which member are you asking about? Available members: {', '.join(available_names[:5])}..."
            })
        
        # Find the specific member
        member = find_member_by_name(members, member_name)
        if not member:
            available_names = [m['name'] for m in members]
            return jsonify({
                "answer": f"Member '{member_name}' not found. Available: {', '.join(available_names[:5])}..."
            })
        
        # Simple answer based on member's most recent messages
        recent_messages = member['messages'][:3]  # Get 3 most recent messages
        if recent_messages:
            summary = " ".join([msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content'] 
                              for msg in recent_messages])
            return jsonify({
                "answer": f"Based on {member['name']}'s recent activity: {summary}",
                "member": member['name'],
                "message_count": len(member['messages'])
            })
        else:
            return jsonify({
                "answer": f"I found {member['name']} but there are no messages available."
            })
            
    except Exception as e:
        print(f"❌ Error in ask endpoint: {e}", file=sys.stderr)
        return jsonify({
            "answer": "Sorry, an error occurred while processing your question.",
            "error": str(e)
        }), 500

# Add a catch-all route for 404 errors
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Endpoint not found",
        "available_endpoints": [
            "/",
            "/health", 
            "/members",
            "/ask"
        ]
    }), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Member QA System on port {port}", file=sys.stderr)
    app.run(host='0.0.0.0', port=port, debug=False)
