import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
import sys
from available_functions import available_functions
from functions.call_function import call_function


def main():
    # Load up our environment and create some objects
    load_dotenv("api.env")
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    # Here we read the prompt provided in the command line. If none is provided, we exit.
    try:
        content = sys.argv[1]
        # We make a list here containing only our prompt at first. We will append the AI's responses to this list
        # so that it is always aware of its own context when looping.
        messages = [types.Content(role="user", parts=[types.Part(text=content)])]
    except IndexError:
        print("Prompt not provided")
        sys.exit(1)

    # We don't want the AI to run its wheels forever, so we have a limit of 20 iterations.
    loop_count = 0
    while loop_count < 20:
        loop_count += 1

        # We feed the prompt to our AI and record its response
        res = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        # We take a look at everything that the response variations from the AI and add it into our messages list.
        for candidate in res.candidates:
            messages.append(candidate.content)

        # If the AI believes that it should call a function, then we call it feed its result back into the messages list.
        if res.function_calls is not None:
            for call in res.function_calls:
                function_call_result = call_function(call)
                messages.append(
                    types.Content(
                        parts=function_call_result.parts,
                        role="user",
                    )
                )
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Function response not found.")
                else:
                    # If the initial prompt included --verbose, we print the function call result as well.
                    try:
                        if sys.argv[2] == "--verbose":
                            print(
                                f"-> {function_call_result.parts[0].function_response.response}"
                            )
                    except IndexError:
                        pass
        # If the AI doesn't think that it needs to call any more functions, then we print its final response and end the loop.
        else:
            print(f"Final Response:\n{res.text}")
            break


if __name__ == "__main__":
    main()
