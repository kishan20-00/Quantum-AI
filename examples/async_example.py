#!/usr/bin/env python3
"""
Async usage example
"""
import os
import asyncio
from quantumai import QuantumAI

async def async_example():
    api_key = os.getenv("LLM_API_KEY", "your-api-key-here")
    base_url = os.getenv("LLM_BASE_URL", "https://your-deployed-model.com/v1")
    
    client = QuantumAI(api_key=api_key, base_url=base_url)
    
    print("Sending async request...")
    try:
        response = await client.achat_complete([
            {"role": "user", "content": "What's the weather like today?"}
        ])
        
        print("Async response:")
        print(response['choices'][0]['message']['content'])
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(async_example())