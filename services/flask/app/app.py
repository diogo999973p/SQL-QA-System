from flask import Flask, render_template, request, jsonify

# Create the Flask application instance
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Mock function to generate an SQL query
def generate_sql_query(question):
    # Replace this with actual logic to generate SQL queries
    return f"SELECT * FROM table WHERE column = '{question}';"

# Mock function to generate an answer
def generate_answer(question):
    # Replace this with actual logic to generate answers
    return f"This is the answer to your question: '{question}'."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    sql_query = generate_sql_query(question)
    answer = generate_answer(question)

    return jsonify({
        'sql_query': sql_query,
        'answer': answer
    })

if __name__ == '__main__':
    app.run(debug=True)