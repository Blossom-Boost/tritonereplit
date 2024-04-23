import logging
import os
from time import sleep
from helpers.client import OpenAIHelper
from flask import Flask, jsonify, request

app = Flask(__name__)

openAiHelper = OpenAIHelper()
openAiClient = openAiHelper.client

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

@app.route('/start_chat', methods=['GET'])
def start_chat():
    thread = openAiClient.beta.threads.create()
    logger.info(f"New chat conversation thread started: {thread.id}")

    return jsonify({"thread_id": thread.id})


@app.route('/chat_message', methods=['POST'])
def chat_message():
    data = request.json
    thread_id = data.get('thread_id')
    user_input = data.get('user_message', '')

    if thread_id is None:
        return jsonify({"error": "Missing thread_id"}), 400

    logger.info(f"[NEW MESSAGE][THREAD {thread_id}] {user_input}")

    run, thread_id = openAiHelper.process_message(user_input, thread_id)

    return jsonify({"run_id": run.id, "thread_id": thread_id})


@app.route('/delay', methods=['GET'])
def delay():
    delay_seconds = 3
    logger.info(f"[API DELAY] Delaying for {delay_seconds} seconds...")
    sleep(delay_seconds)
    return jsonify({"delay": delay_seconds})


@app.route('/get_run', methods=['POST'])
def get_run():
    data = request.json
    thread_id = data.get('thread_id')
    run_id = data.get('run_id')

    logger.info(f"[GET RUN][THREAD {thread_id}][RUN {run_id}]")

    if not thread_id or not run_id:
        return jsonify({"response": "Thread or Run ID is missing"}), 400

    run = openAiHelper.get_run(thread_id=thread_id, run_id=run_id)

    status, message = openAiHelper.process_run(run)

    return jsonify({
        "status": status,
        "message": message
    }), 200 if status != "failed" else 500


@app.route('/background', methods=['POST'])
def background_run():
    data = request.json
    thread_id = data.get('thread_id')
    run_id = data.get('run_id')

    logger.info(f"[GET RUN][THREAD {thread_id}][RUN {run_id}]")

    if not thread_id or not run_id:
        return jsonify({"response": "Thread or Run ID is missing"}), 200

    run = openAiHelper.get_run(thread_id=thread_id, run_id=run_id)

    status, message = openAiHelper.process_run(run)

    should_continue = openAiHelper.convert_to_background_run_response(status, run.usage, run.id)

    return jsonify({
        "status": status,
        "message": message,
        "should_continue": should_continue
    }), 200 if not should_continue else 425


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=os.environ.get('PORT', 8080))
