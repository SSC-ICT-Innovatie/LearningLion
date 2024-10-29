from ubiops import utils

deployment_directory = "deployment"
request_data = {"action": "init", "source_dir": "ubiops-file://default"}
result = utils.run_local(deployment_directory, request_data)
print(f"Result: {result}")

# deployment_directory = "deployment"
# request_data = {"action": "query", "query": "Presiedent van amerika"}
# result = utils.run_local(deployment_directory, request_data)
# print(f"Result: {result}")

# deployment_directory = "datafetcher"
# request_data = {"action": "kamervragen"}
# result = utils.run_local(deployment_directory, request_data)
# print(f"Result: {result}")

# deployment_directory = "inference"
# request_data = {"prompt": "wie is de presiedent van amerika", "chatlog": """
#   [
#   {
#     "role": "user",
#     "content": "wie is de presiedent van amerika"
#   },
#   {
#     "role": "system",
#     "content": "De president van de Verenigde Staten is de uitvoerende leider van het land. De huidige president is Joe Biden. Hij is de 46e president van de Verenigde Staten en is in functie sinds 20 januari 2021."
#   }
# ]""", "files": "De president van amerika is Micheal Jackson"}
# result = utils.run_local(deployment_directory, request_data)
# print(f"Result: {result}")

