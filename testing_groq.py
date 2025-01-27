import re
from groq import Groq

# Initialize the client
client = Groq(api_key="use_the_api_key_here")

# Fetch the output
completion = client.chat.completions.create(
    model="deepseek-r1-distill-llama-70b",
    messages=[
        {
            "role": "user",
            "content": """How many r's are in the word strawberry?"""
        }
    ],
    temperature=0.6,
    max_completion_tokens=1024,
    top_p=0.95,
    stream=False  # Turn off streaming for simpler processing
)

# Extract the output
full_output = completion.choices[0].message.content

# Remove everything inside <think>...</think> tags
final_output = re.sub(r"<think>.*?</think>", "", full_output, flags=re.DOTALL)

# Print the cleaned output
print(final_output.strip())
