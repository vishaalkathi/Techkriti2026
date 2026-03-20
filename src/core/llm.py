import os
from openai import OpenAI
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_llm(prompt, model="gpt-5", temperature=0.3):
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"LLM Error: {e}")
        return ""

def call_llm_json(prompt, model="gpt-5"):
    
    response = call_llm(prompt, model=model)

    try:
        return json.loads(response)
    except:
        # fallback: try to extract JSON
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            return json.loads(response[start:end])
        except:
            return {}