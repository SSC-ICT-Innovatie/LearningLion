from infere import Infer


class Deployment:
  inference = None
  def __init__ (self, base_directory=None, context=None):
    self.inference = Infer("BramVanroy/fietje-2-chat")
    print("Deployment class initialized")
    
  def request(self, data, context):
    if "prompt" not in data:
      print("No prompt provided")
      return {"error": "No prompt provided"}
    chatlog = None
    if "chatlog" in data:
      if "chatlog" in data is not None:
        chatlog = data["chatlog"]
    files = None
    if "files" in data:
      if "file" in data is not None:
        files = data["file"]
    return {"output":self.inference.predict(data["prompt"], chatlog, files)}