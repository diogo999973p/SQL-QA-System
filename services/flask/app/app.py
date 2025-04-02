from flask import Flask, render_template, request
from flask import g, jsonify
from database import Database
import sqlparse
import model
import sys


# Create the Flask application instance
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

USERNAME = 'sa'
PASSWORD = 'SqlServer2019!'
DATABASE = 'master'
MODELNAME = 'deepseek/deepseek-r1:free'

model_client = model.Model(MODELNAME)
model_answers_parser = model.ModelAnswerParser()

print('LOADING FLASK',file=sys.stderr)

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

def get_query_from_model(question):
    try:
        response_text = model_client.generate_text(first_instruction=model.DATABASE_DESCRIPTION, second_instruction=model.FIRST_STEP_DESCRIPTION, prompt=question)
        return response_text
    except Exception as e:
        return e

def get_query_results_from_database(queries):
    # Replace this with actual logic to generate answers
    database_responses = []

    db = get_db()

    for query in queries:
        database_response = db.execute_query(query)
        
        response_rows = []

        for row in database_response:
            response_rows.append(row)

        database_responses.append(response_rows)
    return database_responses

def generate_answer(question, database_responses):
    second_step_instruction = f"""
        Considerer this question: {question} and this database data {database_responses} and answer the question.
        Separate your response if there are multiple questions or answers.
        Do not show the database data on the answer.
        Formatt your response in HTML code, but use only tags that are normaly used inside the body tag, do not use html or body tags.
    """
    ##    
    try:
        response_text = model_client.generate_text(first_instruction=model.DATABASE_DESCRIPTION, second_instruction=second_step_instruction, prompt=question)
        return response_text
    except Exception as e:
        return e

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    model_queries_answer = get_query_from_model(question)
    
    sql_queries = model_answers_parser.get_queries_from_model_answer(model_queries_answer)

    formatted_sql_queries = [sqlparse.format(query, reindent=True, keyword_case='upper') for query in sql_queries]

    queries_text = '\n\n'.join(formatted_sql_queries)

    database_responses = get_query_results_from_database(sql_queries)

    if not database_responses:
        return jsonify({'error': 'No answer from database'}), 400

    answer = generate_answer(question, database_responses)

    response_data = jsonify({
        'sql_query': queries_text,
        'answer': answer
    })

    return response_data

@app.route('/users')
def get_users():
    """Fetch users from the database."""
    db = get_db()
    query = "SELECT * FROM production.categories"
    result = db.execute_query(query)
    users = [dict(row) for row in result]
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)