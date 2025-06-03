import time
from openai import OpenAI

# Single API key
# API_KEY = "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"
# API_KEY = "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" # API premium
API_KEY = "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"

# Create a single client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

def send_request(prompt):
    """Send a single request to the API and return the result."""
    print(f"Sending request...")
    start_time = time.time()
    
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "<YOUR_SITE_URL>",
            "X-Title": "<YOUR_SITE_NAME>",
        },
        model="meta-llama/llama-4-scout",   
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    response = completion.choices[0].message.content
    print(f"Response: {response}")
    print(f"Generation time: {elapsed_time:.2f} seconds")
    
    return response

def main():
    prompt = "What is the meaning of life?"
    
    print("Starting request...")
    overall_start_time = time.time()
    
    response = send_request(prompt)
    
    overall_end_time = time.time()
    overall_elapsed_time = overall_end_time - overall_start_time
    
    print(f"\n===== SUMMARY =====")
    print(f"Total execution time: {overall_elapsed_time:.2f} seconds")

if __name__ == "__main__":
    main()