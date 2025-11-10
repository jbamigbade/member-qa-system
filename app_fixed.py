from flask import Flask, request, jsonify
import requests
import re
from datetime import datetime

app = Flask(__name__)

# Base URL for the member API
MEMBER_API_BASE = "https://november7-730026606190.europe-west1.run.app"

def get_member_data():
    """Fetch member data from the API and transform it to our expected format"""
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
        
        return list(members.values())
            
    except Exception as e:
        print(f"Error: {e}")
        return []

def extract_member_name(question):
    """Extract member name from the question"""
    question_lower = question.lower()
    
    # Common patterns for name extraction
    patterns = [
        r"(?:when is|how many|what are|where is|who is)\s+([a-zA-Z]+(?:\s+[a-zA-Z]+)?(?:'s)?)",
        r"([a-zA-Z]+(?:\s+[a-zA-Z]+)?(?:'s)?)\s+(?:planning|has|favorite|is)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, question_lower)
        if match:
            name = match.group(1)
            # Remove possessive 's if present
            if name.endswith("'s"):
                return name[:-2]
            return name
    
    return None

def answer_question(question, members):
    """Answer question based on member data"""
    question_lower = question.lower()
    member_name = extract_member_name(question)
    
    if not member_name:
        return "I couldn't identify which member you're asking about. Please mention the member's name in your question."
    
    # Find the member
    member = None
    for m in members:
        if m.get('name', '').lower() == member_name.lower():
            member = m
            break
    
    if not member:
        return f"I couldn't find information about {member_name} in the member data."
    
    # Extract messages for the member
    messages = member.get('messages', [])
    
    # Answer different types of questions
    if "when" in question_lower and "london" in question_lower:
        # Look for London trip dates in messages
        for message in messages:
            content = message.get('content', '').lower()
            if 'london' in content:
                # Extract date information
                date_pattern = r'\b\d{4}-\d{2}-\d{2}\b'
                dates = re.findall(date_pattern, message.get('content', ''))
                if dates:
                    return f"{member_name} is planning a trip to London around {dates[0]}."
                else:
                    # Look for day references
                    if 'friday' in content or 'saturday' in content or 'sunday' in content:
                        day_match = re.search(r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b', content)
                        if day_match:
                            return f"{member_name} is planning a trip to London this {day_match.group(1)}."
                    
                    return f"{member_name} is planning a trip to London, but no specific date was mentioned."
        return f"I couldn't find information about {member_name}'s trip to London in the messages."
    
    elif "how many" in question_lower and "car" in question_lower:
        # Count cars mentioned in messages
        car_count = 0
        for message in messages:
            content = message.get('content', '').lower()
            if 'car' in content:
                numbers = re.findall(r'\b(\d+)\s+car', content)
                if numbers:
                    car_count += int(numbers[0])
                else:
                    car_count = max(car_count, 1)
        
        if car_count > 0:
            return f"{member_name} has {car_count} car(s)."
        else:
            return f"I couldn't find information about how many cars {member_name} has."
    
    elif "favorite restaurant" in question_lower:
        # Extract favorite restaurants
        restaurants = []
        for message in messages:
            content = message.get('content', '')
            if 'restaurant' in content.lower():
                restaurant_matches = re.findall(r'["\']([^"\']+?)["\']', content)
                restaurants.extend(restaurant_matches)
        
        if restaurants:
            return f"{member_name}'s favorite restaurants include: {', '.join(set(restaurants))}."
        else:
            return f"I couldn't find specific favorite restaurants for {member_name} in the messages."
    
    else:
        return f"I can answer questions about {member_name}'s travel plans, possessions, or preferences, but I need a more specific question."

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

@app.route('/debug', methods=['GET'])
def debug_api():
    """Debug endpoint"""
    try:
        response = requests.get(f"{MEMBER_API_BASE}/messages", timeout=10)
        members = get_member_data()
        return jsonify({
            "status_code": response.status_code,
            "member_count": len(members),
            "member_names": [m['name'] for m in members[:10]]  # First 10 names
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
