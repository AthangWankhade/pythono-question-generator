import json
import os
import re
from typing import Any, Dict

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


def clean_json_response(content: str) -> str:
    """Extract JSON object from content that may include markdown fences."""
    # Remove code fences like ```json ... ```
    content = re.sub(r"^```(json)?", "", content.strip(), flags=re.MULTILINE)
    content = re.sub(r"```$", "", content.strip(), flags=re.MULTILINE)
    return content.strip()


def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    system_prompt = """You are an expert coding challenge creator.
    Your task is to generate a coding question with multiple choice answers.
    The question should be appropriate for the specified difficulty level.

    For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
    For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
    For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

    Return the challenge in the following JSON structure:
    {
        "title": "The question title",
        "body":"The body of the question",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correct_answer_id": 0, 
        "explanation": "Detailed explanation of why the correct answer is right"
    }

    Make sure the options are plausible but with only one clearly correct answer.
    """

    try:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f'Generate a {difficulty} difficulty coding challenge.'}
            ],
        )

        content = response.choices[0].message.content
        print("Raw response:", content)

        # Clean possible markdown/json formatting
        cleaned = clean_json_response(content)

        challenge_data = json.loads(cleaned)

        required_fields = ["title", "body", "options",
                           "correct_answer_id", "explanation"]
        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing required field: {field}")

        return challenge_data

    except Exception as e:
        print("Error while generating challenge:", e)
        return {
            "title": "Basic Python List Operation",
            "body": "Which method is used to add an item to the end of a Python list?",
            "options": [
                "my_list.append(5)",
                "my_list.add(5)",
                "my_list.push(5)",
                "my_list.insert(5)",
            ],
            "correct_answer_id": 0,
            "explanation": "In Python, append() is the correct method to add an element to the end of a list."
        }
