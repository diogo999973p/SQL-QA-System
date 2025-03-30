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
    #question = None
    #print(f'DATA:{data}',file=sys.stderr)
    #print(f'QUESTION:{question}',file=sys.stderr)

    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    #return jsonify({'error': f'question:{question}'}), 400

    model_queries_answer = get_query_from_model(question)
    
    sql_queries = model_answers_parser.get_queries_from_model_answer(model_queries_answer)

    formatted_sql_queries = [sqlparse.format(query, reindent=True, keyword_case='upper') for query in sql_queries]

    queries_text = '\n\n'.join(formatted_sql_queries)
    
    #.get_data(as_text=True)
    # return jsonify({'error': f'sql_query:{queries}'}), 400

    # sql_query:{'error': "generate_text() got an unexpected keyword argument 'firs_instruction'"}
    
    # sql_query:(<Response 82 bytes [200 OK]>, 500)


    ##print(sqlparse.format(first, reindent=True, keyword_case='upper'))
    
    answer = generate_answer(question)



    response_data = jsonify({
        'sql_query': queries_text,
        'answer': answer
    })

    # print(f"response_data:{response_data}") 
    # print(f"response_type:{type(response_data)}") 

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