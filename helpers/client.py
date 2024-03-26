import time

from openai import OpenAI
import json
import os

from openai.types.beta.threads import Run

from helpers.instructions import instructions
from helpers.tools import Tools

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']  # Requires access to the GPT 4 API


class OpenAIHelper:
    client = None
    assistant_id = None
    assistant = None
    tools = Tools()
    assistant_file_path = 'assistant.json'

    def __init__(self):
        self.get_client()
        self.get_assistant_id()

    def get_client(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def load_assistant_id(self):
        if os.path.exists(self.assistant_file_path):
            with open(self.assistant_file_path, 'r') as file:
                assistant_data = json.load(file)
                self.assistant_id = assistant_data['assistant_id']

    def create_assistant(self):
        knowledge_base = self.client.files.create(file=open("knowledge_base.txt", "rb"), purpose='assistants')

        assistant = self.client.beta.assistants.create(
            instructions=instructions,
            model="gpt-4-1106-preview",
            tools=self.tools.registered,
            file_ids=[knowledge_base.id]
        )

        with open(self.assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)
            print(f"[CLIENT ASSISTANT][ASSISTANT {assistant.id}] Assistant created and saved successfully")

        self.assistant_id = assistant.id
        return self.assistant_id

    def get_assistant_id(self):
        self.load_assistant_id()

        if self.assistant_id is None:
            return self.create_assistant()

        print(f"[CLIENT ASSISTANT][ASSISTANT {self.assistant_id}] Assistant created/loaded successfully")

        return self.assistant_id

    def process_message(self, input, thread_id):
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=input
        )

        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant_id
        )

        print(f"[MESSAGE PROCESSING][THREAD {thread_id}][RUN {run.id}] Processing new message")

        return run

    def get_run(self, thread_id, run_id):
        run = self.client.beta.threads.runs.retrieve(
            run_id=run_id,
            thread_id=thread_id
        )

        print(f"[RETRIEVE RUN][THREAD {thread_id}][RUN {run.id}] Run status {run.status}")
        return run

    @staticmethod
    def convert_thread_messages_to_message(thread_messages):
        thread_message = thread_messages.data[0].content[0].text
        annotations = thread_message.annotations
        for annotation in annotations:
            thread_message.value = thread_message.value.replace(
                annotation.text, '')

        return thread_message

    def process_tool_calls(self, run: Run):
        tool_outputs = []

        for tool_call in run.required_action.submit_tool_outputs.tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            output = self.tools.registered_callers[tool_name](arguments)
            tool_outputs.append({
                "tool_call_id": tool_call.id,
                "output": json.dumps(output)
            })

        self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=run.thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )

    def process_run(self, run: Run):
        if run.status == "completed":
            thread_messages = self.client.beta.threads.messages.list(thread_id=run.thread_id)
            return "completed", self.convert_thread_messages_to_message(thread_messages=thread_messages).value

        if run.status == 'in_progress':
            time.sleep(1)
            return "processing", "not_completed"

        if run.status == 'requires_action':
            self.process_tool_calls(run)
            time.sleep(1)
            return "processing", "not_completed"

        if run.status == 'failed':
            print(f"[RUN FAILED][THREAD {run.thread_id}][RUN {run.id}] {run.error_message}")
            return "error", "Não consegui processar sua mensagem."
