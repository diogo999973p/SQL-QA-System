from flask import Flask, render_template, request
from flask import g, jsonify
from database import Database

# Create the Flask application instance
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

USERNAME = 'sa'
PASSWORD = 'SqlServer2019!'
DATABASE = 'master'

def get_db():
    """Ensure a database connection per request."""
    if 'db' not in g:
        g.db = Database(USERNAME, PASSWORD, DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(exception):
    """Close the database connection after the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/users')
def get_users():
    """Fetch users from the database."""
    db = get_db()
    query = "SELECT * FROM production.categories"
    result = db.execute_query(query)
    users = [dict(row) for row in result]
    return jsonify(users)

def generate_sql_query(question):
    return f"SELECT * FROM table WHERE column = '{question}';"

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