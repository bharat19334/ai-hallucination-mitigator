import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("ERROR: GROQ_API_KEY nahi mili! Please check your .env file.")

client = Groq(
    api_key=api_key 
)

def generate_baseline_response(query: str) -> str:

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", 
            temperature=0.7, 
            messages=[
                {"role": "system", "content": "You are a helpful educational tutor. Answer the student's question clearly."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        
        return f"Error connecting to Groq LLM: {str(e)}"
    


def generate_stochastic_samples(query: str, num_samples: int = 3) -> list:
    
    print(f"Generating {num_samples} stochastic samples for SelfCheck...")
    samples = []
    
    for i in range(num_samples):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                temperature=1.0, 
                messages=[
                    {"role": "system", "content": "You are a helpful educational tutor. Answer the student's question clearly."},
                    {"role": "user", "content": query}
                ]
            )
            samples.append(response.choices[0].message.content)
        except Exception as e:
            print(f"Error generating sample {i}: {e}")
            
    return samples