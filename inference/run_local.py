from inference.libraries.infere import Infer


def infer_run_local(prompt,
                    chatlog=None,
                    files=None, 
                    LLM="BramVanroy/fietje-2-chat", 
                    systemPrompt=None, 
                    generation_kwargs=None):
  inference = Infer(LLM)
  return inference.predict(prompt, chatlog, files, systemPrompt, generation_kwargs)

def infer_factory(LLM="BramVanroy/fietje-2-chat"):
  return Infer(LLM)