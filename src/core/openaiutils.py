__author__= "nirajkumar"

import os

import openai
from openai import OpenAI


openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_embedding(text, model="text-embedding-ada-002"):
  client = OpenAI()
  response = client.embeddings.create(
    model = model,
    input = text,
    encoding_format = "float"
  )
  embedding = response.data[0].embedding
  return embedding


def qa_prompt_template(question, context, additional_instructions=None):
  """
  Template for creating a Q&A prompt.
  
  Parameters:
  - question (str): The specific question to be answered.
  - context (str): Background information or context for the question.
  - additional_instructions (str, optional): Any further instructions for refining the answer.
  
  Returns:
  - str: A formatted Q&A prompt.
  """

  prompt = f"""
  ### Q&A Prompt ###

  **Context/Background Information:** 
  {context}

  **Question:** 
  {question}

  """
  
  if additional_instructions:
      prompt += f"**Additional Instructions:** \n{additional_instructions}\n"

  return prompt


def chat_completion(prompt, context, model="gpt-4o"):
  refined_prompt = qa_prompt_template(prompt, context)
  client = OpenAI()
  completion = client.chat.completions.create(
    model = model,
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": refined_prompt}
    ])
  answer = completion.choices[0].message.content
  return answer
