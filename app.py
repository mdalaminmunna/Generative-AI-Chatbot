import sqlite3

def init_db():
    conn = sqlite3.connect('database/chatbot.db')
    with open('models/interaction.sql') as f:
        conn.executescript(f.read())
    conn.close()

def log_interaction(user_query, chatbot_response):
    conn = sqlite3.connect('database/chatbot.db')
    conn.execute(
        "INSERT INTO interaction (user_query, chatbot_response) VALUES (?,?)",
        (user_query, chatbot_response),
    )
    conn.commit()
    conn.close()

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_query = request.json.get('query')
        if not user_query:
            return jsonify({'error': 'Query is Required'}), 400
        
        #Generate prompt and fetch GIT response
        prompt = generate_prompt(user_query)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["\n"]
        )
        chatbot_response = response.choices[0].text.strip()

        #Log interaction in the database
        log_interaction(user_query, chatbot_response)

        return jsonify({'response': chatbot_response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analytics', methods=['GET'])
def analytics():
    try:
        from analytics import generate_analytics
        generate_analytics()
        return jsonify({'message': 'Analytics Generated Successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500