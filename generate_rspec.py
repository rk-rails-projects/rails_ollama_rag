import sys
from query_codebase import query_codebase
import requests
# import json

def generate_rspec(prompt):
    documents = query_codebase(prompt)
    if not documents:
        print("[!] No relevant documents found in the codebase.")
        return

    context = "\n\n".join(documents)
    ollama_prompt = f"""You are an expert Ruby on Rails developer and RSpec writer.
        Given the following Rails code:\n\n{context}\n\n
        Write a complete RSpec test suite for the function described by: '{prompt}'.
        Include examples and edge cases."""

    # Send request to Open WebUI/Ollama endpoint
    response = requests.post(
        "http://localhost:11434/api/generate",  # or WebUI endpoint
        json={
            "model": "deepseek-r1:8b",  # your model name in Ollama
            "prompt": ollama_prompt,
            "stream": False
        }
    )

    result = response.json()
    print("\n=== ✅ Suggested RSpec ===\n")
    print(result.get("response", "No response from model"))

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Usage: python generate_rspec.py 'YourController#action'")
    else:
        generate_rspec(sys.argv[1])
