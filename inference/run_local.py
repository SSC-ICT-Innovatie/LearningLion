from inference.libraries.infere import Infer


def infer_run_local(prompt, chatlog=None, files=None):
  inference = Infer("BramVanroy/fietje-2-chat")
  inference.predict(prompt, chatlog, files)