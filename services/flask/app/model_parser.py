
class ModelAnswerParser:
    def __init__(self):
        pass

    def get_queries_from_model_answer(self, answer):
        self.answer = answer

        cleaned_answer = answer.replace('sql', '').replace('`','')
        
        queries = [query.strip() for query in cleaned_answer.split(';') if query.strip()]

        return queries