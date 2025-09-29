#!/usr/bin/env python3
"""
Streaming example
"""
import os
from quantumai import QuantumAI

def streaming_example():
    api_key = os.getenv("LLM_API_KEY", "your-api-key-here")
    base_url = os.getenv("LLM_BASE_URL", "https://your-deployed-model.com/v1")
    
    client = QuantumAI(api_key=api_key, base_url=base_url)
    
    print("Streaming response...")
    try:
        for chunk in client.stream_chat([
            {"role": "user", "content": "Explain quantum computing in simple terms"}
        ]):
            content = chunk.get('choices', [{}])[0].get('delta', {}).get('content', '')
            if content:
                print(content, end='', flush=True)
        print()  # New line after streaming
        
    except Exception as e:
        print(f"Error during streaming: {e}")

if __name__ == "__main__":
    streaming_example()