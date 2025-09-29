#!/usr/bin/env python3
"""
Basic usage example for the LLM Client
"""
import os
from quantumai import QuantumAI

def main():
    # Get API key from environment variable or use placeholder
    api_key = os.getenv("LLM_API_KEY", "your-api-key-here")
    base_url = os.getenv("LLM_BASE_URL", "https://your-deployed-model.com/v1")
    
    # Initialize client
    client = QuantumAI(
        api_key=api_key,
        base_url=base_url,
        default_model="your-model-name",
        debug=True  # Enable debug logging
    )
    
    # Simple chat completion
    print("Sending chat request...")
    try:
        response = client.chat_complete([
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you tell me a joke?"}
        ])
        
        print("\nResponse:")
        print(response['choices'][0]['message']['content'])
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()