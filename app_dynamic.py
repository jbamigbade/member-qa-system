from flask import Flask, request, jsonify
import requests
import re
import os
import socket

app = Flask(__name__)

# Base URL for the member API
MEMBER_API_BASE = "https://november7-730026606190.europe-west1.run.app"

# Cache member data to avoid repeated API calls
member_data_cache = None

def get_member_data():
    """Fetch member data from the API with caching"""
    global member_data_cache
    
    if member_data_cache is not None:
        return member_data_cache
        
    try:
        print("Fetching data from external API...")
        response = requests.get(f"{MEMBER_API_BASE}/messages", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"API returned {len(data.get('items', []))} items")
        
        # Transform the API response to our expected format
        members = {}
        for item in data.get('items', []):
            user_name = item.get('user_name')
            if user_name not in members:
                members[user_name] = {
                    'name': user_name,
                    'messages': []
                }
            
            members[user_name]['messages'].append({
                'content': item.get('message', ''),
                'timestamp': item.get('timestamp', '')
            })
        
        member_data_cache = list(members.values())
        print(f"Transformed to {len(member_data_cache)} members")
        return member_data_cache
            
    except Exception as e:
        print(f"Error fetching member data: {e}")
        return []

def extract_member_name(question):
    """Extract member name from the question - SIMPLIFIED VERSION"""
    question_lower = question.lower()
    
    # Known member first names
    known_first_names = [
        "sophia", "fatima", "armand", "hans", "layla", 
        "amina", "vikram", "lily", "lorenzo", "thiago"
    ]
    
    # Check if any known first name is in the question
    for name in known_first_names:
        if name in question_lower:
            return name
    
    return None

def answer_question(question, members):
    """Answer question based on member data"""
    question_lower = question.lower()
    member_name = extract_member_name(question)
    
    print(f"DEBUG: Question: '{question}'")
    print(f"DEBUG: Extracted name: '{member_name}'")
    
    if not member_name:
        available_names = [m.get('name', '').split()[0] for m in members]
        return f"I couldn't identify which member you're asking about. Available members: {', '.join(available_names)}"
    
    # Find the member - match by first name
    member = None
    for m in members:
        full_name = m.get('name', '').lower()
        first_name = full_name.split()[0] if ' ' in full_name else full_name
        
        if member_name.lower() == first_name:
            member = m
            break
    
    if not member:
        available_names = [m.get('name', '').split()[0] for m in members]
        return f"I couldn't find member '{member_name}'. Available members: {', '.join(available_names)}"
    
    # Extract messages for the member
    messages = member.get('messages', [])
    
    print(f"DEBUG: Found member: {member.get('name')}")
    print(f"DEBUG: Message count: {len(messages)}")
    
    # Show first few messages for debugging
    for i, msg in enumerate(messages[:2]):
        print(f"DEBUG: Message {i}: {msg.get('content', '')[:100]}...")
    
    # Answer different types of questions
    if "london" in question_lower:
        # Look for London in messages
        for message in messages:
            content = message.get('content', '').lower()
            if 'london' in content:
                return f"{member.get('name')} mentioned London: '{message.get('content', '')}'"
        return f"I couldn't find any mentions of London in {member.get('name')}'s messages."
    
    elif "car" in question_lower:
        # Look for car mentions
        for message in messages:
            content = message.get('content', '').lower()
            if 'car' in content:
                return f"{member.get('name')} mentioned cars: '{message.get('content', '')}'"
        return f"I couldn't find any car mentions in {member.get('name')}'s messages."
    
    elif "restaurant" in question_lower:
        # Look for restaurant mentions
        for message in messages:
            content = message.get('content', '').lower()
            if 'restaurant' in content:
                return f"{member.get('name')} mentioned restaurants: '{message.get('content', '')}'"
        return f"I couldn't find any restaurant mentions in {member.get('name')}'s messages."
    
    else:
        # General question - return the most recent message
        if messages:
            latest_message = messages[0].get('content', '')
            if len(latest_message) > 150:
                latest_message = latest_message[:150] + "..."
            return f"{member.get('name')}'s latest message: {latest_message}"
        else:
            return f"I found {member.get('name')} in the system but they don't have any messages."

@app.route('/ask', methods=['GET'])
def ask_question():
    """Main endpoint for asking questions"""
    question = request.args.get('question', '')
    
    if not question:
        return jsonify({"answer": "Please provide a question using the 'question' parameter."})
    
    # Get member data
    members = get_member_data()
    
    if not members:
        return jsonify({"answer": "Sorry, I couldn't fetch the member data at the moment. Please try again later."})
    
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
    members = get_member_data()
    return jsonify({
        "members": [m['name'] for m in members],
        "total": len(members)
    })

def find_available_port():
    """Find an available port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

if __name__ == '__main__':
    port = find_available_port()
    print(f"🚀 Starting Member Q&A API on port {port}")
    print(f"📊 Testing URL: http://localhost:{port}/health")
    print(f"❓ Ask questions: http://localhost:{port}/ask?question=What did Sophia say?")
    app.run(host='0.0.0.0', port=port, debug=True)
