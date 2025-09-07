import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
import sys
from available_functions import available_functions
from functions.call_function import call_function


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
            function_call_result = call_function(call)
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Function response not found.")
            else:
                try:
                    if sys.argv[2] == "--verbose":
                        print(
                            f"-> {function_call_result.parts[0].function_response.response}"
                        )
                except IndexError:
                    pass
    else:
        print(res.text)


if __name__ == "__main__":
    main()
