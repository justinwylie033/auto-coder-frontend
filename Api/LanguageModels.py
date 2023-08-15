from tenacity import retry, wait_random_exponential, stop_after_attempt
import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPEN_AI_KEY = os.getenv('OPEN_AI_KEY')
LLM_MODEL = os.getenv('LLM_MODEL')
EMBED_MODEL = os.getenv('EMBED_MODEL')

openai.api_key = OPEN_AI_KEY

def get_gpt_completion(prompt):
    # Use GPT-3.5-turbo to generate the content based on the prompt
    # Return the generated content
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": f"generate  {prompt} "}],
            temperature=0.55,
        )
        response = completion.choices[0].message.content
        
        return response
    except Exception as e:
        print(e)

def get_gpt4_completion(prompt):
    # Use GPT-3.5-turbo to generate the content based on the prompt
    # Return the generated content
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": f"generate  {prompt} "}],
            temperature=1,
        )
        response = completion.choices[0].message.content
        
        return response
    except Exception as e:
        print(e)

def get_writing_completion(prompt):
    # Use GPT-4-turbo to generate the content based on the prompt
    # Return the generated content
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": f"generate  {prompt} "}],
            temperature=1,
            frequency_penalty=1,
            presence_penalty=0.73,
        )
        response = completion.choices[0].message.content
        
        return response
    except Exception as e:
        print(e)

#gets the embedding of a sentence
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text: str) -> list[float]:
    embedding = openai.Embedding.create(input=text, model=EMBED_MODEL)["data"][0]["embedding"]
    return embedding


        
