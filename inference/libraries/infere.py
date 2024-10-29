import json
import os
import torch
from transformers import pipeline

os.environ["TOKENIZERS_PARALLELISM"] = "false"

class Infer:
  generator = None
  systemPrompt = """Je bent een vriendelijke chatbot genaamd Learning Lion. Je wilt altijd graag vragen beantwoorden en blijft altijd vriendelijk. Alle informatie die jij verteld komt uit de bestanden die zijn bijgevoegd, mochten de bestanden niet bestaan of onvoldoende informatie bevatten dan zeg je 'ik weet het niet' of 'ik kan je niet helpen'."""
  def __init__(self, modelName):
    device = 0 if torch.cuda.is_available() else -1
    self.generator = pipeline("text-generation", model=modelName, device=device)
    print("Model loaded")
    

  def predict(self, prompt, chatlog= None, files=None):
    converation = [
        {"role": "system", "content": self.systemPrompt},
        {"role": "user", "content": prompt},
        ]
    
    if chatlog is not None:
      converation.append({"role": "system", "content": f"eerdere berichten {chatlog}"})
    if files is not None:
      converation.append({"role": "system", "content": f"relevante bestanden {files}"})
      
    translatedPrompt = self.generator.tokenizer.apply_chat_template(converation, tokenize=False, add_generation_prompt=True)
    return self.generator(translatedPrompt, max_new_tokens=500)