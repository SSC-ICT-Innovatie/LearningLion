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


	def parse_chatlog(self, chatlog):
			# Parse the chatlog string into a usable list format
			parsed_conversation = []
			# Split chatlog entries by 'map[' to isolate each message entry
			entries = chatlog.split("map[")
			for entry in entries[1:]:  # Skip the first split result, as it's empty
				# Extract whether it's from the user and the message text
				from_user = "fromUser:true" in entry
				message_start = entry.find("message:") + len("message:")
				message_end = entry.find(" username:")
				message = entry[message_start:message_end].strip()
				# Determine the role and append to parsed_conversation
				role = "user" if from_user else "assistant"
				parsed_conversation.append({"role": role, "content": message})
			return parsed_conversation

	def predict(self, prompt, chatlog=None, files=None,system_prompt=None,  generation_kwargs=None):
		if system_prompt is None:
			system_prompt = self.systemPrompt
		# Initialize conversation with the system prompt
		conversation = [{"role": "system", "content": system_prompt}]
		# Parse chatlog and add it to conversation
		if chatlog is not None:
			parsed_chatlog = self.parse_chatlog(chatlog)
			conversation.extend(parsed_chatlog)
		# Add the latest user prompt to the conversation
		conversation.append({"role": "user", "content": prompt})
		# Include any files if provided
		if files is not None:
			conversation.append({"role": "system", "content": f"Relevante bestanden:\n{files}"})
		# Add custom markers as special tokens
		self.generator.tokenizer.add_special_tokens({
			'additional_special_tokens': ['<|im_start|>', '<|im_end|>']
		})
		self.generator.model.resize_token_embeddings(len(self.generator.tokenizer))

		# Generate text prompt without tokenizing
		text = self.generator.tokenizer.apply_chat_template(
			conversation=conversation,
			tokenize=False,
			add_generation_prompt=True,
		)
		base_generate_kwargs = {
				"do_sample": False,
				"temperature": 1.0,
				"max_new_tokens": 500,
			}
		generate_kwargs = base_generate_kwargs
		if generation_kwargs is not None:
			generate_kwargs = {**base_generate_kwargs, **generation_kwargs}
			print(generate_kwargs)

		# Pass the text directly to the generator
		response = self.generator(text, **generate_kwargs)
		response = response[0]["generated_text"]
		response = response.replace(text,"")
  
		return response