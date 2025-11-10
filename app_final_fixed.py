from flask import Flask, request, jsonify
import requests
import re
import os

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
        response = requests.get(f"{MEMBER_API_BASE}/messages", timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
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
        return member_data_cache
            
    except Exception as e:
        print(f"Error fetching member data: {e}")
        return []

def extract_member_name(question):
    """Extract member name from the question - SIMPLIFIED VERSION"""
    question_lower = question.lower()
    
    # First, try to match against known member first names
    known_first_names = [
        "sophia", "fatima", "armand", "hans", "layla", 
        "amina", "vikram", "lily", "lorenzo", "thiago"
    ]
    
    # Check if any known first name is in the question
    for name in known_first_names:
        if name in question_lower:
            return name
    
    # Simple pattern matching - just look for words that could be names
    words = question_lower.split()
    for word in words:
        # Skip common question words
        if word in ['what', 'when', 'how', 'many', 'does', 'is', 'are', 'to', 'the', 'a']:
            continue
        # If word looks like a name (starts with capital in original, but we're using lower)
        # Just return the first non-question word as potential name
        if len(word) > 2:  # Avoid very short words
            return word
    
    return None

def answer_question(question, members):
    """Answer question based on member data"""
    question_lower = question.lower()
    member_name = extract_member_name(question)
    
    print(f"DEBUG: Question: '{question}'")
    print(f"DEBUG: Extracted name: '{member_name}'")
    
    if not member_name:
        return "I couldn't identify which member you're asking about. Please mention the member's name in your question."
    
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
    
    # Answer different types of questions
    if "london" in question_lower:
        # Look for London in messages
        for message in messages:
            content = message.get('content', '').lower()
            if 'london' in content:
                return f"{member.get('name')} mentioned London in their messages: '{message.get('content', '')}'"
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
