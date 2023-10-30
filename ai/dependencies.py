import openai
import os
import dotenv


dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG")

async def chat_completion(prompt, model="gpt-3.5-turbo"):
    completion = openai.ChatCompletion.create(
    model=model,
    messages=[
        {"role": "user", "content": prompt}
    ]
    )
    
    return (completion.choices[0].message.content)

async def image_completion(prompt):
 
    completion = openai.Image.create(
        prompt=prompt,
    )

    return (completion.data[0].url)

async def embed_text(text):
    completion = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text,
        encoding_format="float"
        )


    return (completion.data[0].embedding)