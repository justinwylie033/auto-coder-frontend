from flask import Flask, request, jsonify, abort
from LanguageModels import get_gpt4_completion, get_gpt_completion
from flask_cors import CORS
import logging
from GenerateCode import GenerateCode
from ImproveCode import ImproveCode
from RunCode import RunCode
from EvaluateCode import EvaluateCode

# Initialisation
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

@app.route('/get-initial-code', methods=['POST'])
def get_initial_code():
    logging.info('Handling request for initial code generation')
    logging.info(f"Request: {request.json}")

    language = request.json.get("language", "").lower()
    code_requirements = request.json.get("code_requirements", "")

    response, status = GenerateCode(language, code_requirements)

    return jsonify(response), status


@app.route('/run-code', methods=['POST'])
def run_code():
    logging.info('Handling request for code execution')
    logging.info(f"Request: {request.json}")

    language = request.json.get("language", "").lower()
    code = request.json.get("code", "")
    container_name = request.json.get("container_name", "")

    response, status_code = RunCode(language, code, container_name)

    return jsonify(response), status_code


@app.route('/improve-code', methods=['POST'])
def improve_code():
    logging.info('Handling request for code improvement')
    logging.info(f"Request: {request.json}")

    code = request.json.get("code", "")
    problem = request.json.get("error", "")
    code_output = request.json.get("output", "")

    response, status = ImproveCode(code, problem, code_output)

    return jsonify(response), status


@app.route('/evaluate-code', methods=['POST'])
def evaluate_code():
    logging.info('Handling request for code valuation')
    logging.info(f"Request: {request.json}")

    code = request.json.get("code", "")
    output = request.json.get("output", "")
    code_requirements = request.json.get("code_requirements", "")

    response, status = EvaluateCode(code, code_requirements, output)

    return jsonify(response), status

@app.errorhandler(400)
def bad_request(error):
    logging.error(f"Bad request: {error}")
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def server_error(error):
    logging.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An unhandled exception occurred: {e}")
    return jsonify({"error": "An unexpected error occurred."}), 500
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
