import json
import os
from google import genai
from google.genai import types

client = genai.Client()

TOOLS = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="read_file",
                description="Reads content of a file in the workspace.",
                parameters={"type": "OBJECT", "properties": {"path": {"type": "STRING"}}, "required": ["path"]}
            ),
            types.FunctionDeclaration(
                name="apply_patch",
                description="Applies a diff patch to a project file.",
                parameters={"type": "OBJECT", "properties": {"path": {"type": "STRING"}, "diff": {"type": "STRING"}}, "required": ["path", "diff"]}
            ),
            types.FunctionDeclaration(
                name="run_tests",
                description="Executes project unit tests via Gradle.",
                parameters={"type": "OBJECT", "properties": {}}
            )
        ]
    )
]

class PolarisAgent:
    def __init__(self, workspace_path: str, task_prompt: str):
        self.workspace = workspace_path
        self.prompt = task_prompt
        self.trajectory = []

    def step(self, history):
        response = client.models.generate_content(
            model='gemini-1.5-pro',
            contents=history,
            config=types.GenerateContentConfig(
                tools=TOOLS,
                system_instruction="You are a principal software engineer solving long-horizon mobile architecture tasks."
            )
        )
        return response
