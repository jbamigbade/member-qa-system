from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

# Base URL for the data source API
API_BASE = "https://november7-730026606190.europe-west1.run.app"

def get_member_data():
    """Fetch and process real member data from the external API"""
    try:
        print("📡 Fetching data from external API...")
        response = requests.get(f"{API_BASE}/messages", timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Received {len(data.get('items', []))} messages")
        
        # Transform API data into member-focused structure
        members = {}
        for item in data.get('items', []):
            user_name = item.get('user_name')
            message_content = item.get('message', '')
            
            if user_name not in members:
                members[user_name] = {
                    'name': user_name,
                    'messages': []
                }
            
            members[user_name]['messages'].append({
                'content': message_content,
                'timestamp': item.get('timestamp', '')
            })
        
        member_list = list(members.values())
        print(f"📊 Processed {len(member_list)} members: {[m['name'] for m in member_list]}")
        return member_list
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return []

def search_member_messages(member, keywords):
    """Search for keywords in member messages"""
    relevant_messages = []
    for msg in member.get('messages', []):
        content = msg.get('content', '').lower()
        if any(keyword in content for keyword in keywords):
            relevant_messages.append(msg.get('content'))
    return relevant_messages

def answer_question(question, members):
    """Answer natural language questions about members using real data"""
    question_lower = question.lower()
    
    # Extract member name with better matching
    member_name = None
    member_full_name = None
    
    # Map common names to actual member names in the data
    name_mapping = {
        'layla': 'Layla Kawaguchi',
        'vikram': 'Vikram Desai', 
        'amira': 'Amira',  # Check if Amira exists in data
        'sophia': 'Sophia Al-Farsi',
        'fatima': 'Fatima El-Tahir',
        'hans': 'Hans Müller',
        'amina': 'Amina Van Den Berg',
        'armand': 'Armand Dupont',
        'lily': "Lily O'Sullivan",
        'lorenzo': 'Lorenzo Cavalli',
        'thiago': 'Thiago Monteiro'
    }
    
    for short_name, full_name in name_mapping.items():
        if short_name in question_lower:
            member_name = short_name
            member_full_name = full_name
            break
    
    if not member_name:
        available = [m['name'] for m in members]
        return f"I couldn't identify which member. Available: {', '.join(available)}"
    
    # Find the member
    member = None
    for m in members:
        if member_full_name and m.get('name') == member_full_name:
            member = m
            break
        elif member_name in m.get('name', '').lower():
            member = m
            break
    
    if not member:
        available = [m['name'] for m in members]
        return f"Member '{member_name}' not found. Available: {', '.join(available)}"
    
    print(f"🔍 Analyzing {len(member['messages'])} messages for {member['name']}")
    
    # Answer specific question types with better search
    if 'london' in question_lower:
        london_messages = search_member_messages(member, ['london'])
        if london_messages:
            # Try to extract timing information
            for msg in london_messages:
                # Look for dates
                date_match = re.search(r'\b\d{4}-\d{2}-\d{2}\b', msg)
                if date_match:
                    return f"{member['name']} is planning a trip to London around {date_match.group()}."
                
                # Look for time references
                time_ref = re.search(r'\b(next week|next month|in june|in july|soon|this weekend)\b', msg.lower())
                if time_ref:
                    return f"{member['name']} is planning a trip to London {time_ref.group()}."
            
            return f"{member['name']} mentioned London in their messages."
        return f"I couldn't find London trip information for {member['name']}."
    
    elif 'car' in question_lower:
        car_messages = search_member_messages(member, ['car', 'vehicle'])
        if car_messages:
            car_count = 1  # Default assumption
            for msg in car_messages:
                # Look for numbers
                numbers = re.findall(r'\b(\d+)\s+car', msg.lower())
                if numbers:
                    car_count = int(numbers[0])
                elif 'second' in msg.lower() or 'another' in msg.lower() or 'two' in msg.lower():
                    car_count = 2
            
            return f"{member['name']} has {car_count} car(s)."
        return f"I couldn't find car information for {member['name']}."
    
    elif 'restaurant' in question_lower:
        restaurant_messages = search_member_messages(member, ['restaurant', 'dinner', 'food', 'eat'])
        if restaurant_messages:
            restaurants = []
            for msg in restaurant_messages:
                # Extract quoted names
                quoted = re.findall(r'["\']([^"\']+?)["\']', msg)
                restaurants.extend(quoted)
                
                # Extract capitalized restaurant-like names
                capitalized = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', msg)
                restaurants.extend([r for r in capitalized if len(r) > 3])
            
            if restaurants:
                unique = list(set(restaurants))
                return f"{member['name']}'s mentioned restaurants: {', '.join(unique)}."
            
            return f"{member['name']} mentioned restaurants in their messages."
        return f"I couldn't find restaurant information for {member['name']}."
    
    else:
        # Return most recent message as general response
        if member['messages']:
            latest = member['messages'][0]['content']
            if len(latest) > 100:
                latest = latest[:100] + "..."
            return f"{member['name']}'s latest: {latest}"
        return f"I found {member['name']} but no messages."

@app.route('/ask', methods=['GET'])
def ask_question():
    """Question-answering endpoint"""
    question = request.args.get('question', '').strip()
    
    if not question:
        return jsonify({"answer": "Please provide a question parameter."})
    
    members = get_member_data()
    
    if not members:
        return jsonify({"answer": "Sorry, I couldn't fetch the member data."})
    
    answer = answer_question(question, members)
    
    return jsonify({"answer": answer})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/members', methods=['GET'])
def list_members():
    """List available members"""
    members = get_member_data()
    return jsonify({
        "members": [m['name'] for m in members],
        "total": len(members)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
