import os
import time
from functools import lru_cache

import openai
import torch
import transformers
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import BloomForCausalLM, BloomTokenizerFast

from utils.config import Settings

load_dotenv()

# bloom_models = ["", "-6b3", "-2b5", "-1b3", "-760m", "-350m"]
# bloom_model = "bigscience/bloom" + bloom_models[5]

# model = BloomForCausalLM.from_pretrained(bloom_model)
# tokenizer = BloomTokenizerFast.from_pretrained(bloom_model)

# def greedy(prompt: str, result_length: int=50):
#     inputs = tokenizer(prompt, return_tensors="pt")
#     return tokenizer.decode(model.generate(inputs["input_ids"], 
#                     max_new_tokens=result_length
#                     )[0])

# def beam(prompt: str, result_length: int=50):
#     inputs = tokenizer(prompt, return_tensors="pt")
#     return tokenizer.decode(model.generate(inputs["input_ids"],
#                     max_new_tokens=result_length, 
#                     num_beams=2, 
#                     no_repeat_ngram_size=2,
#                     early_stopping=True
#                     )[0])

# def sample(prompt: str, result_length: int=50):
#     inputs = tokenizer(prompt, return_tensors="pt")
#     return tokenizer.decode(model.generate(inputs["input_ids"],
#                     max_new_tokens=result_length, 
#                     do_sample=True, 
#                     top_k=50, 
#                     top_p=0.9
#                     )[0])

def first_sentence(full: str):
    return full.split(full, ".")[0] + "."

def first_line(full: str):
    return full.splitlines()[0]

def first_line_after(full: str, prefix: str):
    lines = full.replace(prefix, "").splitlines()
    if lines[0] == "" and len(lines) > 0:
        return lines[1]
    else:
        return lines[0]

def first_sentence_after(full: str, prefix: str):
    sentences = full.replace(prefix, "").split(".")
    if sentences[0] == "" and len(sentences) > 0:
        return sentences[1]
    else:
        return sentences[0]

# prompt_schema = """
# openapi: 3.1.0
# x-stoplight:
#   id: yjuh6ia0uicil
# info:
#   title: test
#   version: '1.0'
# servers:
#   - url: 'http://localhost:3000'
# paths:
# """
# curr = "The following is an OpenAPI schema describing a petstore:\n" + prompt_schema
# for i in range(10):
#     print(curr)
#     resp = "" # input("Continue?(y/n) ")
#     if resp == 'n':
#         break
#     else:
#         curr += first_line_after(greedy(curr, result_length=25), curr) + "\n"
# print(curr)



# FAST API #

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@lru_cache
def get_settings():
    settings = Settings()
    # print(settings.dict())
    # openai.api_key = settings.openai_api_key
    openai.api_key = os.environ["OPENAI_API_KEY"]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/bloom/")
async def generate(text: str):
    return {"generated": first_sentence_after(greedy(text, result_length=25), text)};

@app.get("/openai/")
async def generate(text: str, settings: Settings = Depends(get_settings)):
            return openai.Completion.create(
                model="text-davinci-002",
                prompt=text,
                max_tokens=25,
                temperature=0.6,
                echo=False
            ).choices[0].text

@app.get("/openai/compare/")
async def generate(text:str , settings: Settings = Depends(get_settings)):
    names = ["ada-001", "babbage-001", "curie-001", "davinci-001", "davinci-002"]
    resp = {};
    for name in names:
        ti = time.time()
        completion = openai.Completion.create(
            model="text-ada-001",
            prompt=text,
            max_tokens=25,
            temperature=0.6,
        ).choices[0].text
        tf = time.time()
        resp[name] = {"time": tf - ti, "text": completion}
    return resp
