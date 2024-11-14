from inference.libraries.infere import Infer

inference_Global = None

def infer_run_local(prompt,
                    chatlog=None,
                    files=None, 
                    LLM="BramVanroy/fietje-2-chat", 
                    systemPrompt=None, 
                    generation_kwargs=None):
  global inference_Global
  if inference_Global is None:
    inference_Global = Infer(LLM)
  return inference_Global.predict(prompt, chatlog, files, systemPrompt, generation_kwargs)

def infer_factory(LLM="BramVanroy/fietje-2-chat"):
  return Infer(LLM)