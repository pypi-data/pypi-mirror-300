import os
import openai
import re
import time
import argparse



PROMPT = f"""You are Helpful AI Assistant"""

class llm_terminal:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL","https://api.together.xyz/v1")
        try:
            self.client = openai.OpenAI(
                                        api_key=os.getenv("PROVIDER_API_KEY"),
                                        base_url=self.base_url
            ) 
        except Exception as e:
            log_error_message(e)
            
            
    def generate_response(self, prompt):
        model = os.getenv("MODEL_ID","google/gemma-2-27b-it")
        
        try:
            respose = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": prompt},
            ],
            stream=True
            )       
        except Exception as e:
            log_error_message(e)
        print(print_yellow_text("Provider: "), end="")
        print(print_yellow_text(self.base_url), end=" ")
        print(print_yellow_text("Model:"), end=" ")
        print(print_yellow_text(model))

        print(print_green_text("#AI Assistant:"))
        for chunk in respose:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")
        print("\n")

        
def print_green_text(text) -> str:
    return f"\033[92m{text}\033[0m"

def print_blue_text(text)-> str:
    return f"\033[94m{text}\033[0m"

def print_red_text(text) -> str:
    return f"\033[91m{text}\033[0m"

def print_yellow_text(text) -> str:
    return f"\033[93m{text}\033[0m"
def log_error_message(message):
    """Logs an error message in a user-friendly format, highlighting missing API key and providing instructions for configuration."""

    print(print_red_text("**ERROR: Missing API Key**"))
    print(print_yellow_text("The API key required to access the provider is missing or invalid."))

    print("\n**Steps to Resolve:**")
    print(print_green_text(1), ".Set the PROVIDER_API_KEY environment variable:")
    print(print_blue_text(f"\t- export PROVIDER_API_KEY='YOUR_API_KEY' or set PROVIDER_API_KEY='YOUR_API_KEY' for CMD "))  # Example usage
    print(print_yellow_text("\t\tYou can find your API key in the Providers dashboard."))

    print(print_green_text(2), ".Optional Configuration (default values provided):")
    print(print_blue_text(f"\t- BASE_URL (default: https://api.together.xyz/v1):"))
    print(print_blue_text("\t\texport BASE_URL='https://api.openai.com/v1'"))  # Example
    print(print_blue_text(f"\t- MODEL_ID (default: not set):"))
    print(print_blue_text("\t\texport MODEL_ID='meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo'"))  # Example

    print("\n**Environment Variables Summary:**")
    print(print_green_text("  - PROVIDER_API_KEY: Your Model API key."))
    print(print_green_text("  - BASE_URL: The base URL for the Providers API (optional)."))
    print(print_green_text("  - MODEL_ID: The ID of the Model to use (optional)."))

    print("\n**Additional Information:**")
    print(print_green_text("- For more information, refer to the documentation."))

    print("\n**Error Details:**")
    print(print_blue_text(f"{message}"))

    # Terminate execution with a clear exit message
    print(print_red_text("Exiting program due to missing API key."))
    exit()



def main():
    parser = argparse.ArgumentParser(description="Generate terminal command responses using OpenAI.")
    parser.add_argument("command", type=str, help="The command to generate a response for.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Additional arguments for the command.")
    args = parser.parse_args()
    
    prompt = " ".join([args.command] + args.args)
    terminal = llm_terminal()
    terminal.generate_response(prompt)

