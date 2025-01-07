from ubiops import utils

# deployment_directory = "deployment"
# request_data = {"action": "init", "source_dir": "ubiops-file://default"}
# result = utils.run_local(deployment_directory, request_data)
# print(f"Result: {result}")

# deployment_directory = "deployment"
# request_data = {"action": "query", "query": "Presiedent van amerika"}
# result = utils.run_local(deployment_directory, request_data)
# print(f"Result: {result}")

deployment_directory = "datafetcher"
request_data = {"action": "kamervragen", "range": "Tiny"}
result = utils.run_local(deployment_directory, request_data)
print(f"Result: {result}")

# deployment_directory = "inference"
# request_data = {"prompt": "wie is de presiedent van amerika", "chatlog": """
#   {
#   "chatlog": "[map[fromUser:true message:Wat is je naam sources:[] username:Jij] map[fromUser:true message:Wat is je naam? username:Jij] map[fromUser:false message:Mijn naam is AI Chatbot. Als je meer vragen hebt of hulp nodig hebt, sta ik altijd voor je klaar.]] sources:[] username:Learning Lion (genAI)] map[fromUser:true message:Hoe gaat het ermee? username:Jij] map[fromUser:false message:Hallo! Ik ben Learning Lion, een chatbot die je kan helpen met allerlei vragen. Als je iets wilt weten, stel het me gerust. Ik ben altijd vriendelijk en sta klaar om je te helpen.]] sources:[] username:Learning Lion (genAI)] map[fromUser:true message:Wat zijn de vragen over klimaat? username:Jij] map[fromUser:false message:Hallo! Ik ben Learning Lion, een chatbot die je kan helpen met allerlei vragen. Als je iets wilt weten, stel het me gerust. Ik ben altijd vriendelijk en sta klaar om je te helpen.]] sources:[] username:Learning Lion (genAI)] map[fromUser:true message:Hallo? username:Jij] map[fromUser:false message:Hallo! Ik ben Learning Lion, een chatbot die je kan helpen met allerlei vragen. Als je iets wilt weten, stel het me gerust. Ik ben altijd vriendelijk en sta klaar om je te helpen.\n\nWat zijn de vragen over klimaat?\n\nKlimaatverandering is een belangrijk onderwerp dat veel mensen bezighoudt. Het gaat over de langdurige veranderingen in het klimaat van de aarde. Deze veranderingen worden veroorzaakt door verschillende factoren, waaronder menselijke activiteiten zoals het verbranden van fossiele brandstoffen, ontbossing en industriële processen.\n\nDe gevolgen van klimaatverandering zijn veelzijdig en kunnen wereldwijd worden waargenomen. Ze omvatten het smelten van gletsjers en ijskappen, stijgende zeespiegels, extreme weersomstandigheden zoals hittegolven, droogtes en overstromingen, en veranderingen in ecosystemen.\n\nDe impact van klimaatverandering op de mensheid is ook aanzienlijk. Het kan leiden tot voedsel- en watertekorten, gezondheidsproblemen, verplaatsing van bevolkingsgroepen en economische schade.\n\nEr zijn verschillende manieren waarop we kunnen bijdragen aan het verminderen van de impact van klimaatverandering. Dit omvat het verminderen van onze uitstoot van broeikasgassen door minder te reizen met de auto en meer te kiezen voor openbaar vervoer, het verminderen van energieverbruik in huis, het gebruiken van hernieuwbare energiebronnen zoals zonne- en windenergie, en het]] sources:[] username:Learning Lion (genAI)]]",
#   "prompt": "Wie zijn de mensen van PVV?"
# }
#   """, "files": "De president van amerika is Micheal Jackson"}
# result = utils.run_local(deployment_directory, request_data)
# print(f"Result: {result}")

