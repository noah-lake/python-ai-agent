import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
import sys
from call_function import available_functions


def main():
    load_dotenv("api.env")
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    try:
        content = sys.argv[1]
        messages = [types.Content(role="user", parts=[types.Part(text=content)])]
    except IndexError:
        print("Prompt not provided")
        sys.exit(1)

    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if len(res.function_calls) > 0:
        for call in res.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(res.text)

    try:
        if sys.argv[2] == "--verbose":
            print(
                f"User prompt: {content}, Prompt tokens: {res.usage_metadata.prompt_token_count}, Response tokens: {res.usage_metadata.candidates_token_count}"
            )
    except IndexError:
        pass


if __name__ == "__main__":
    main()
