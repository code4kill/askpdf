from flask_restx import Namespace, Resource, fields
from flask import request
from src.controller.question_controller import handle_question

# Create the namespace
question_ns = Namespace('question', description='Question operations')

# Define the request and response models for Swagger documentation
question_request_model = question_ns.model('QuestionRequest', {
    'id': fields.String(required=True, description='ID of the user or file'),
    'question': fields.String(required=True, description='Question to ask')
})

question_response_model = question_ns.model('QuestionResponse', {
    'answer': fields.String(required=True, description='Answer to the question')
})

# Route for retrieving history of questions by ID
@question_ns.route('/history/<string:id>')
@question_ns.param('id', 'The user/file identifier')
@question_ns.response(404, 'History not found')
class QuestionHistory(Resource):
    def get(self, id):
        """
        Get history of questions by ID
        """
        # You can implement logic here to retrieve the question history
        return {'message': 'Retrieve question history'}, 200

# Route for asking a question
@question_ns.route('/ask')
class AskQuestion(Resource):
    @question_ns.expect(question_request_model, validate=True)
    @question_ns.marshal_with(question_response_model)
    def post(self):
        """
        Ask a question and get an answer
        """
        # Parse the incoming JSON payload
        question_payload = request.json
        # Extract 'id' and 'question' from the payload and call the controller
        answer = handle_question(id=question_payload["id"], question=question_payload["question"])
        print(answer)
        # Return the response in the expected format
        return {'answer': answer}, 200
