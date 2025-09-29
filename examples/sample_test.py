from quantumai import QuantumAI

# Initialize client with API key and custom endpoint
client = QuantumAI(
    api_key="test-key",
    base_url="http://localhost:5000/v1"
)

# Basic chat completion
response = client.chat_complete([
    {"role": "user", "content": "Hello! Can you explain what machine learning is?"}
])

print("Response:", response['choices'][0]['message']['content'])