import transformers
from transformers import BloomForCausalLM
from transformers import BloomTokenizerFast
import torch

bloom_models = ["", "-6b3", "-2b5", "-1b3", "-760m", "-360m"]
bloom_model = "bigscience/bloom" + bloom_models[4]

model = BloomForCausalLM.from_pretrained(bloom_model)
tokenizer = BloomTokenizerFast.from_pretrained(bloom_model)

def greedy(prompt: str, result_length: int=50):
    inputs = tokenizer(prompt, return_tensors="pt")
    return tokenizer.decode(model.generate(inputs["input_ids"], 
                    max_new_tokens=result_length
                    )[0])

def beam(prompt: str, result_length: int=50):
    inputs = tokenizer(prompt, return_tensors="pt")
    return tokenizer.decode(model.generate(inputs["input_ids"],
                    max_new_tokens=result_length, 
                    num_beams=2, 
                    no_repeat_ngram_size=2,
                    early_stopping=True
                    )[0])

def sample(prompt: str, result_length: int=50):
    inputs = tokenizer(prompt, return_tensors="pt")
    return tokenizer.decode(model.generate(inputs["input_ids"],
                    max_new_tokens=result_length, 
                    do_sample=True, 
                    top_k=50, 
                    top_p=0.9
                    )[0])

def first_sentence(full: str):
    return full.split(full, ".")[0] + "."

def first_line(full: str):
    return full.splitlines()[0]

def first_line_after(full: str, prefix: str):
    print(full.replace(prefix, "").splitlines())
    lines = full.replace(prefix, "").splitlines()
    if lines[0] == "" and len(lines) > 0:
        return lines[1]
    else:
        return lines[0]

prompt_schema = """
openapi: 3.1.0
x-stoplight:
  id: yjuh6ia0uicil
info:
  title: test
  version: '1.0'
servers:
  - url: 'http://localhost:3000'
paths:
"""
curr = "The following is an OpenAPI schema describing a petstore:\n" + prompt_schema
for i in range(10):
    print(curr)
    resp = "" # input("Continue?(y/n) ")
    if resp == 'n':
        break
    else:
        curr += first_line_after(greedy(curr, result_length=25), curr) + "\n"
print(curr)