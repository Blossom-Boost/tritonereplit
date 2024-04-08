from flask import Flask, jsonify, request
from helpers.client import OpenAIHelper
import json

app = Flask(__name__)

openAiHelper = OpenAIHelper()
openAiClient = openAiHelper.client


@app.route('/start_chat', methods=['GET'])
def start_chat():
    thread = openAiClient.beta.threads.create()
    print(f"New chat conversation thread started: {thread.id}")

    return jsonify({"thread_id": thread.id})


@app.route('/chat_message', methods=['POST'])
def chat_message():
    data = request.json
    thread_id = data.get('thread_id')
    user_input = data.get('user_message', '')

    if thread_id is None:
        return jsonify({"error": "Missing thread_id"}), 400

    print(f"[NEW MESSAGE][THREAD {thread_id}] {user_input}")

    run = openAiHelper.process_message(user_input, thread_id)

    return jsonify({"run_id": run.id})


@app.route('/get_run', methods=['POST'])
def get_run():
    data = request.json
    thread_id = data.get('thread_id')
    run_id = data.get('run_id')

    if not thread_id or not run_id:
        return jsonify({"response": "Thread or Run ID is missing"}), 400

    run = openAiHelper.get_run(
        thread_id=thread_id,
        run_id=run_id
    )

    status, message = openAiHelper.process_run(run)

    return jsonify({"status": status, "message": message}), 200 if status != "failed" else 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)