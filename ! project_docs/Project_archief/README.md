# TLDR documenten projectarchief
De documenten in dit projectarchief dateren van oktober 2023 t/m april 2024. Hier vind je per document een kort abstract of samenvatting met de belangrijkste bevindingen.

## Advies

## Eindrapportage genAI

## Eindverslag Jitse Goutbeek

## Experimenteren met RAG

## Kabinetsvisie

## Project plan

## PvA Generatieve AI v1.0
In dit document wordt een plan van aanpak gepresenteert voor een onderzoek naar hoe generatieve AI kan worden ingezet binnen SSC-ICT en de specifieke use case van de servicedesk. Het onderzoek bestaat uit twee onderdelen. Ten eerste is het plan om zelf een open soucre Chatbot te ontwikkelen door een bestaande LLM te finetunen. Ten tweede wordt er onderzocht wat de mogelijkheden zijn voor het ontwikkelen van een chatbot binnen de infrastructuur binnen Microsoft Azure. Deze twee worden daarna met elkaar vergeleken op basis van nader op te stellen (meetbare) beoordelingscriteria. Het idee van de chatbots is dat ze kunnen worden ingezet bij de servicedesk van SSC-ICT om medewerkers te helpen bij het beantwoorden van vragen die daar binnenkomen. Het doel is om medewerkers te ondersteunen in hun werk en interene processen optimaliseren.  

## RAG testen met inkoopmedewerkers I&W
In dit document worden bevindingen gedeeld met betrekking tot de vraag:  *kunnen we vragen van leveranciers die in een NVI gesteld worden beantwoorden op basis van eerdere Nota van Inlichtingen en andere documentatie?* Hierbij was het belangrijk dat het model lokaal draaide. De documenten die werden meegegeven waren: een Nota van Inlichtingen en een breed scala aan documenten over beleidsadvies en ingenieursdiensten van I&W. Verschillende instellingen zijn getest door dertien vragen tegelijk te stellen aan het model. Vervolgens zijn de resultaten met behulp van inkoopmedewerkers van I&W vergeleken. Er is vooral gefocust op het aanpassen van de prompt die je meegeeft. Over het algemeen lijken de open source embeddingsmodellen maar matig in hun beheersing van het Nederlands, De taalmodellen die op een laptop kunnen draaien hadden ook moeite met het volgen van instructies. Er lijkt wel aanleiding te zijn om te denken dat een uitgebreide uitleg van de situatie en opdracht in de prompt helpen in het verbeteren van de kwaliteit van de antwoorden.

## RAG voor inkoop, resultaten en bedenkingen
In dit document worden bevindingen gedeeld met betrekking tot de vraag:  *kunnen we vragen van leveranciers die in een NVI gesteld worden beantwoorden op basis van eerdere Nota van Inlichtingen en andere documentatie?* De documenten die werden meegegeven waren: een Nota van Inlichtingen en een breed scala aan documenten over beleidsadvies en ingenieursdiensten van I&W. Er is een cloudoplossing en een oplossing met een API-key getest. Daarom is er alleen gebruik gemaakt van openbare documentatie. Bij de eerste experimenten is vooral globaal gekeken naar accuraatheid. Er is daarom louter beoordeeld of het antwoord grofweg of helemaal overeenkwam met het daadwerkelijke antwoord vanuit de inkopers (eerste verkenning kwaliteit om potentie in te schatten). Het maakt niet uit of je rekenkracht via Azure of een API-key gebruikt. Hierin zijn steeds dezelfde modellen gebruikt. Beide applicaties lukt het redelijk goed vragen terug te vinden in een Nota van Inlichtingen. Daarentegen leek het amper mogelijk vragen uit een tweede Nota van Inlichtingen te beantwoorden op basis van het aanbestedingsdocument en de eerste Nota van Inlichtingen. Dit kan aan de beperkingen van de data zelf liggen, dus het is lastig om daar meer conclusies uit te trekken.

## Vergelijking open source modellen
Verschillende documenten waarin de state of the art LLM's worden besproken.

### Versie 1.0: Oktober 2023
Belangrijkste conclusies uit dit document:
- Er wordt een sterke voorkeur uitgesproken voor modellen met minder parameters vanwege de beschikbare rekenkracht, energie en kosten.
- Mistral-7B-OpenOrca lijkt het beste basismodel om verder op te trainen voor chatbotfuncties binnen de Rijksoverheid. De verhouding tussen de prestaties en het aantal parameters is goed.
- Er is gesproken met Bram Vanroy. Hij adviseerd Mistral-modellen te gebruiken in plaats van de zijne. Het blijkt lastig te zijn om een model dat heel weinig in het Nederlands pre-trained is, goed Nederlands te leren met de datasets die momenteel beschikbaar zijn. 
- De Nederlandse datasets die nu beschikbaar zijn, zijn van lage kwaliteit. Echter heeft het Orcaproject (Microsoft) laten zien dat je met relatief veel data van hoge kwaliteit hele goede resultaten kan bereiken. Het vertalen van Orca naar het Nederlands zou dus een meerwaarde zijn, maar valt voor nu buiten de scope.

### Versie 2.0: Januari 2024
Belangrijkste conclusies uit dit document:
- De modellen gaan gebruikt worden voor RAG (retrieval augmented generation)

De meest kansrijke modellen zijn:
- Mistral-7x8B mixture of expert
- Geitje: het op nederlands gefinetunede mistral-7B model van Rijserberg
- SciPhi SelfRAG: het voor RAG gefinetunede mistral-7B model met de self-rag dataset
- Mistral-7B-OpenOrca: de met Orca gefinetunede versie van Mistral
- Qwen 14 miljard, om ook een niet Mistral model te bekijken

### Versie 2.1: Maart 2024
De meest kansrijke modellen zijn:
- Mistral-7x8B mixture of expert
- Geitje Ultra
- Zephyr
- SciPhi SelfRAG: het voor RAG gefinetunede mistral-7B model met de self-rag dataset
- Mistral-7B-OpenOrca: de met Orca gefinetunede versie van Mistral

## Verbetermogelijkheden RAG
In dit document wordt kort de pipeline uitgelegd van de manier hoe RAG is vormgegeven. Ook vind je hier een visuele weergave met de libraries en applicaties die zijn gebruikt. Daarnaast worden een aantal mogelijkheden beschreven om RAG te verbeteren inclusief de bijbehorende bronvermelding:

1. Verbeteren van de zoekfunctie: hoe zorg je ervoor dat je de relevante stukken tekst vindt?
Dit kan bijvoorbeeld door:
- Metadata opslaan en filteren
- Samenvattingen opslaan en doorzoeken
- Hybride zoeken
- Hypothetische vragen of antwoorden embedden
- Klein zoeken, groot maken (hiërarchisch zoeken)
2. Toevoegingen maken aan de architectuur: Wat als je dingen wilt weten die niet in die paar stukjes tekst te vinden zijn?
Dit kan bijvoorbeeld door:
- Knowledge graphs
- Self-RAG
3. Overige technieken:
- Query transformation
- Bronverbelding verbeteren
- Embeddings of rerankers finetunen
- Chunking strategie verbeteren (semantisch chunken)

## Visiestuk SSC-ICT