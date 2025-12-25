import json
import os
from typing import List

from environs import Env

env = Env()
env.read_env()   # loads .env

GEMINI_API_KEY = env.str("GEMINI_API_KEY")  # boom — string, guaranteed

from google import genai


ERROR_LOG_PATH = "errors.jsonl"

def read_recent_errors(path: str, limit: int) -> List[dict]:
    errors = []

    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found")

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                errors.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue

    return errors[-limit:]


def build_prompt(errors: List[dict]) -> str:
    prompt = """You are a senior systems engineer.
Analyze the following CLI errors and give me response in the below format for each error:
"guess":"you guess for what the user was trying to type based on the command and error"

Errors:
"""

    for i, e in enumerate(errors, 1):
        prompt += f"""
Error {i}:
Command: {e.get("command")}
Error: {e.get("error")}
Exit Code: {e.get("exit_code")}
"""

    return prompt.strip()


def call_llm(prompt: str) -> str:
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
    )

    return response.text


def main():
    errors = read_recent_errors(ERROR_LOG_PATH , 1)

    if not errors:
        print("No errors found. Congrats, your CLI behaved for once.")
        return

    prompt = build_prompt(errors)
    answer = call_llm(prompt)

    print("\n=== LLM ASSIST ===\n")
    print(answer)


if __name__ == "__main__":
    main()
