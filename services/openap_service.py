import openai
# from config import OPENAI_API_KEY

# # Set your OpenAI API key
# openai.api_key = OPENAI_API_KEY

# async def process_with_openai(prompt: str) -> str:
#     try:
#         # Asynchronous call to OpenAI's ChatCompletion API (for text generation)
#         response = await openai.ChatCompletion.acreate(  # Correct method name
#             model="gpt-3.5-turbo",  # Use the appropriate model
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=150,
#             temperature=0.7,
#         )

#         # Extract the generated text from the response
#         return response['choices'][0]['message']['content'].strip()

#     except openai.OpenAIError as e:
#         raise Exception(f"OpenAI API error: {e}")
#     except Exception as e:
#         raise Exception(f"Error processing data with OpenAI: {str(e)}")

import asyncio
import os
from openai import AsyncOpenAI

async def process_with_openai(prompt: str) -> str:
    try:
        # Initialize the AsyncOpenAI client
        api_key = os.environ.get("OPENAI_API_KEY")
        client = AsyncOpenAI(api_key=api_key)

        # Asynchronous call to OpenAI's ChatCompletion API
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )

        # Extract the generated text from the response
        return response['choices'][0]['message']['content'].strip()

    except openai.OpenAIError as e:
        raise Exception(f"OpenAI API error: {e}")
    except Exception as e:
        raise Exception(f"Error processing data with OpenAI: {str(e)}")
