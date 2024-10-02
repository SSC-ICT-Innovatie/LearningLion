# TLDR documenten projectarchief
De documenten in dit projectarchief dateren van oktober 2023 t/m april 2024. Hier vind je per document een kort abstract of samenvatting met de belangrijkste bevindingen. Door op onderstaande titels te klikken kun je gelijk het bijbehorende document downloaden.

## [Advies](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/Advies.docx)
In dit document worden aanbevelingen gedaan op basis van vijf observaties:
1. Er is veel onzekerheid over de meerwaarde van specifieke toepassingen
2. Er wordt volop geëxperimenteerd binnen de rijksoverheid. Er is dus een grote itneresse, maar er zijn meetinstrumenten nodig om de risico's en kwaliteit af te wegen.
3. Veel onderzoeken lopen tegen een vergelijkbaar probleem aan: te weinig rekenkracht en een te langzame kennisopbouw.
4. SSC-ICT kan een toekomstige, beheerde dienstverlening aanbieden door de beschikbare expertise.
5. De bouw van applicaties heeft een grotere meerwaarde dan alleen de applicatie zelf in huis halen. Hierdoor bouw je kennis op.

Het advies heeft als doel om beter zicht te krijgen op: hoe geef je testen goed vorm? Waar is wel en geen vraag naar? Wat werkt wel en wat werkt niet? Pas dan kan je als SSC-ICT een gerichte beheerde dienst leveren.
- Kennis van technologie en diens voor- en nadelen veranderen snel. Het is te vroeg om een specifieke dienst kant-en-klaar aan te leveren of in te kopen van de markt.
- Een indrukwekkende demo geven is makkelijk, maar hier worden vaak niet de bijbehorende risico's in acht genomen.
- Geef prioriteit aan het opbouwen van kennis en behoud flexibiliteit in plaats van de focus op het eindproduct leggen. Dit kan je doen door te blijven experimenteren.
- Zet in op dingen die relevant blijven. Iedere toepassing heeft namelijk rekenkracht nodig.
- Doe op korte termijn Impact Assessments om een "vervanging" voor ChatGPT te kunnen bieden. Als dit goed uitpakt kun je het hosten (met een dikke disclaimer).
- Met een compute platform kunnen we klanten helpen door hun ideeën erop te testen en een stukje consultancy te geven. Om effectiviteit te waarborgen moeten we onze eigen use cases hierop testen om ervaring op te doen.

## [Eindrapportage genAI](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/Eindrapportage%20genAI%202023%20v0.3.docx)
Dit is een voortganagsrapport van het project: onderzoek naar de inzet van generatieve AI voor interne procesverbetering (in het kader van AI en spraakbesturing). Er is bewust niet gekozen voor het pre-trainen finetunen van een model. De focus lag hier op LLM's en RAG. In het rapport worden drie zorgen beschreven die bij de Rijksoverheid leven op het gebied van generatieve AI en hoe deze ondervangen kunnen worden met de RAG-oplossing. Ten eerste de privacygevoeligheid van ingevoerde data. Dit kan mogelijk opgelost worden door het systeem lokaal te runnen. Ten tweede de afhaneklijkheid van specifieke leveranciers. Dit kan mogelijk ondervangen worden door een flexibele architectuur te handhaven waarbij modellen inwisselbaar zijn. Bovendien is er dan ruimte om de nieuwste modellen te implementeren en kan je je pipeline op maat maken voor specifieke use cases. Tot slot zijn er zorgen over de data waarop de modellen getraind zijn, bijvoorbeeld in het kader van de mogelijke schending van auteursrecht. Dit laatste punt ligt buiten de scope van het project. Deze zorgen worden voor nu ondervangen door projecten als GPT-NL, die de middelen hebben om een model vanaf nul te trainen. Er is onderzoek gedaan naar beschikbare LLM's. Voor deze toepassing is het probleem dat vele niet zijn getraind op Nederlandse data. Ook is er is een proof of concept ontwikkeld om het nut van LLM's en RAG laten zien. De uitkomsten van het onderzoek lijken erop dat RAG potentie heeft om voor meer transparantie in taalmodellen te zorgen. Door een (lokale) database aan documenten aan een LLM mee te geven, is het systeem minder geneigd te hallucineren en is het bovendien transparanter, omdat je de bronnen kan herleiden. Er worden enkele suggesties gedaan om dit onderzoek in 2024 voort te zetten: het verbeteren van specifieke onderdelen van de RAG-applicatie en onderzoek doen naar RAG effectief inzetten door bijvoorbeeld de combinatie te maken met LLM agents. Er wordt aanbevolen om te starten met bouwen van een infrastructuur, onderzoek te blijven doen en discussies te blijven voeren die het mogelijk maken om als overheid autonoom te handelen op het gebied van generatieve AI. RAG is een mogelijkheid om de overheid voor zichzelf en de burger inzichtelijker te maken. Een voorbeeld hiervan is de use case: *inzicht in beleid* die in dit rapport wordt beschreven. 

## [Eindverslag Jitse Goutbeek](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/Eindverslag%20Jitse%20Goutbeek.docx)
In dit document worden de stappen beschreven die er de afgelopen 4 maanden zijn genomen en de belangrijkste inzichten die daaruit gehaald zijn. 

AI brengt risico’s met zich mee. Generatieve AI en RAG zijn geen uitzonderingen. Denk aan vragen rondom dataveiligheid en de betrouwbaarheid en eerlijkheid van de resultaten. Volgens het standpunt vanuit de overheid over generatieve AI moet er een DPIA uitgevoerd worden en een algemene impact assessment zoals de IAMA (ontwikkeld door BZK), de AI impact assessment (ontwikkeld door ECP) en de gelijknamige assessment van I&W.

Bij een RAG toepassing zijn er twee vormen van gegevensverwerking van toepassing. Ten eerste zijn er de gegevens die ooit verwerkt zijn bij het trainen van het taalmodel. Hier kunnen persoonsgegevens of auteursrechtelijk beschermde gegevens in zitten. Dit kan problematisch zijn maar juridisch is de ontwikkelaar van het gebruikte taalmodel hier verantwoordelijk voor. Ten tweede is er de verwerking van de interne documenten, die niet gebruikt worden om het model te trainen maar slechts doorzocht worden. Binnenkort gaat SSC-ICT impact assessments afnemen voor specifieke open source taalmodellen.

Uit experimenten met RAG zijn een aantal belangrijke inzichten gekomen:
- De vragen over wat wel en niet met welke mate van gegevensbescherming verwerkt mag worden speelt nog. Onze rol is tot dusver om te kijken wat er kan onder de aanname dat we alles open source en lokaal doen. Hier blijkt veel rekenkracht voor nodig. Daardoor is er een tweede pad ingeslagen om te onderzoeken of er überhaupt potentie in het project zit. Dit werd gedaan door een vergelijkbare casus uit te voeren met openbare data via de cloud of een API-key. 
- Zowel in de cloud als met de API was het programma in staat om vragen terug te vinden en de antwoorden te reproduceren. Ook als je deze vragen herformuleert. Echter, het stellen van vragen die later gesteld werden op basis van vragen die eerder gesteld waren bleek ingewikkeld, wat goed aan beperkingen van de data zelf zou kunnen liggen. Het is dus lastig om daar meer conclusies uit te trekken.
- Voor extra rekenkracht was er toegang tot GPU’s, helaas bleek het gebruik hiervan uitermate complex. Het is nog niet gelukt om dit te organiseren omdat de applicatie niet samenkwam met de rekenkracht van de GPU’s. Daarom is de applicatie voor een groot deel aangepast en is daarvoor de code gebruikt die Stefan Troost maakte voor het planbureau voor de leefomgeving. Hierdoor kon de code volledig lokaal draaien en kon de tool getest worden. 
- In alle experimenten was minder dan de helft van de antwoorden naar tevredenheid van de gebruikers beantwoord. Wel was er spreiding afhankelijk van welke instellingen er precies gekozen waren. Een imperfecte tool leveren heeft riscio’s. Wat er nu staat is niet goed genoeg om tot dienst te leveren. Gelukkig zijn er heel wat vernieuwingen op het gebied van LLM’s en zijn er genoeg verbetermogelijkheden voor de RAG.

Men is nog zoekende in de manieren hoe generatieve AI nu wordt geëvalueerd. Deze zijn nu vaak ontoereikend. Het is belangrijk om te kijken welke evaluatiemethoden voor onze doeleinden werken. Willen we automatische evaluaties, of willen we met gebruikers in gesprek? Hoe zorgen we daarin voor reproduceerbaarheid? Hierbij moet je enorm veel vragen aan de generatieve AI stellen om de grote variatie in antwoorden te evalueren.

Voor nu is het voor de organisatie belangrijk om meer rekenkracht te realiseren zodat er sneller en beter onderzoek gedaan kan worden. Hiervoor zijn al contacten gelegd. Om de kennis nog verder op te bouwen is het belangrijk om zelf aan de slag te blijven met het bouwen en testen van applicaties. Deze kennis kan bijvoorbeeld worden ingezet om beoordelingsinstrumenten in te richten. Daarbij is het belangrijk om deze kennis te blijven delen.


## [Experimenteren met RAG](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/Experimenteren%20met%20RAG.docx)
In dit verslag wordt een set van experimenten beschreven van een pipeline die werden beoordeeld aan de hand van zelf opgestelde beoordelingscriteria. Het doel was om een systematiek te ontwikkelen om onze applicatie met alternatieven te kunnen vergelijken en een begrip krijgen van een specifieke RAG infrastructuur en bepaalde keuzes die je daarin maakt. Dit experiment is uitgevoerd binnen de context van een bepaalde use case en vertaalt dus niet 1 op 1 naar een andere use case. De applicatie die hiervoor werd gebruikt was appl-docchat. Hier kan je je instellingen naar eigen wens aanpassen. De knowledge-base die werd gebruikt bestond uit alle gespreksverslagen van de verhoren van de eerste week van de Parlementaire enquêtecommissie Fraudebeleid en Dienstverlening. Bij elk experiment zijn steeds 11 vragen gesteld en wisselde steeds de instellingen. Het vinden van een goed functionerend open source embeddingmodel was lastig, maar jegormeister/bert-base-dutch-cased deed het erg goed en is de keuze voor veredere experimenten of open source toepassingen. Als taalmodel wordt in de toekomst GPT3.5 gebruikt en gaat er gewerkt worden met 4 chunk sizes van 1024.

## [Kabinetsvisie](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/Kabinetsvisie.docx)
Sinds 1 januari 2024 is er een [overheidsbrede kabinetsvisie op Generatieve AI](https://www.rijksoverheid.nl/documenten/rapporten/2024/01/01/overheidsbrede-visie-generatieve-ai). RAG is een vorm van generatieve AI, dus is het belangrijk om bij dit document stil te staan. Er wordt ten eerste beargumenteerd dat RAG veel potentie heeft om bij te dragen aan deze visie, maar het raakt ook bepaalde zorgen die voor een groot deel nog op waarde geschat moeten worden. Daarnaast geven de experimenten die nu worden uitgevoerd een mooie bijdrage aan de visie, omdat deze op zichzelf al waardevol zijn. Tot slot wordt er geconcludeerd dat er nog een aantal plekken voor nader onderzoek zijn om te bepalen of, hoe en wanneer het in productie nemen van RAG-applicaties bijdraagt aan de visie. 

Er zijn een tal van RAG-projecten binnen de overheid. Ze proberen andere problemen op te lossen en andere documenten te onderzoeken. Er worden ook verschillende keuzes gemaakt in de opbouw van de architectuur. Dit heeft onder andere te maken met het zoeken naar de meest relevante stukken tekst, welk taalmodel er gebruikt wordt en hoe je de rekenkracht het beste inricht. Door deze gemeenschappelijke vragen is er sinds begin februari een [community of practice](https://generatieveai.pleio.nl/) opgericht waar projecten die met dezelfde vragen worstelen daar met elkaar over kunnen praten en van elkaar kunnen leren.

De overheid wil graag dat ambtenaren generatieve AI op een verantwoorde manier kunnen gebruiken om hun werk efficiënter uit te voeren. Zeker als het aankomt op het doorzoeken en opzoeken van de vele documenten. RAG zou bij kunnen dragen aan deze doelstellingen. Om te weten of we die meerwaarde ook echt in de praktijk kunnen realiseren, moet er onderzoek gedaan worden en worden geëxperimenteerd. Dit wordt in de kabinetsvisie aangemoedigd. Zo kunnen we inschatten waar de functionaliteit ligt, wat het doel is en wat de risico’s zijn. RAG heeft bovendien een meerwaarde in het kader van uitlegbaarheid. Dit is niet alleen belangrijk als het gaat om verantwoording, maar het helpt ook met het adequaat omgaan met eventuele risico’s. Dit raakt aan het probleem van hallucinaties die grote taalmodellen soms genereren. Bij RAG zie je welke context is gebruikt om tot een gegenereerd antwoord te komen. We kunnen dus uitleggen dat het antwoord voortkomt uit een specifiek document. Dit document vertrouwen we en dus is het antwoord te vertrouwen. Tegelijkertijd is het niet te zeggen waarom precies dit antwoord op basis van de documenten gegeven wordt. Daarnaast is hallucinatie niet uitgesloten.

Een belangrijke vraag is of het verbinden van een zoekmachine aan een taalmodel voldoende meerwaarde oplevert. Er zijn namelijk genoeg zorgen rondom het gebruik van taalmodellen zoals bias, afhankelijkheid of hallucinaties. Echter wil de overheid en het kabinet graag gebruik maken van generatieve AI om de overheid toegankelijker te maken (voor zichzelf en de burger). Hier zou RAG enorm bij kunnen helpen en is dus de koppeling met een taalmodel cruciaal. Het is zaak om eerst een applicatie voor intern gebruik te maken voordat we het aanbieden aan burgers om uitgebreid te kunnen testen.

Een belangrijke afweging bij het in productie nemen van een RAG-applicatie is hoe je de rekenkracht organiseert. Er zijn meerdere opties die verschillende voor- en tegenargumenten hebben: een API-key, cloud of het volledig lokaal hosten.

Voordat het daadwerkelijk in productie genomen wordt moet er een [DPIA](https://www.autoriteitpersoonsgegevens.nl/themas/basis-avg/praktisch-avg/data-protection-impact-assessment-dpia) en een algoritme impact assessment zoals de [IAMA](https://www.rijksoverheid.nl/documenten/rapporten/2021/02/25/impact-assessment-mensenrechten-en-algoritmes) worden uitgevoerd. De uitkomsten hiervan dienen voorafgaand aan de inzet van de toepassing ter advies aan de (departementale) CIO en de Functionaris Gegevensbescherming te worden voorgelegd. Zij moeten hierover oordelen. Het oordeel zal waarschijnlijk afhangen van welke documentatie er wordt doorzocht en hoe de hardware is ingericht. Het is daarnaast belangrijk dat het voor de gebruiker duidelijk is dat ze met een AI interacteren en wat de beperkingen van het model zijn. 


## [PvA Generatieve AI v1.0](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/PvA%20Generatieve%20AI%20v1.0.docx)
In dit document wordt een plan van aanpak gepresenteert voor een onderzoek naar hoe generatieve AI kan worden ingezet binnen SSC-ICT en de specifieke use case van de servicedesk. Het onderzoek bestaat uit twee onderdelen. Ten eerste is het plan om zelf een open soucre Chatbot te ontwikkelen door een bestaande LLM te finetunen. Ten tweede wordt er onderzocht wat de mogelijkheden zijn voor het ontwikkelen van een chatbot binnen de infrastructuur binnen Microsoft Azure. Deze twee worden daarna met elkaar vergeleken op basis van nader op te stellen (meetbare) beoordelingscriteria. Het idee van de chatbots is dat ze kunnen worden ingezet bij de servicedesk van SSC-ICT om medewerkers te helpen bij het beantwoorden van vragen die daar binnenkomen. Het doel is om medewerkers te ondersteunen in hun werk en interene processen optimaliseren.  

## [RAG testen met inkoopmedewerkers I&W](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/RAG%20testen%20met%20inkoopmedwerkers%20I&W.docx)
In dit document worden bevindingen gedeeld met betrekking tot de vraag:  *kunnen we vragen van leveranciers die in een NVI gesteld worden beantwoorden op basis van eerdere Nota van Inlichtingen en andere documentatie?* Hierbij was het belangrijk dat het model lokaal draaide. De documenten die werden meegegeven waren: een Nota van Inlichtingen en een breed scala aan documenten over beleidsadvies en ingenieursdiensten van I&W. Verschillende instellingen zijn getest door dertien vragen tegelijk te stellen aan het model. Vervolgens zijn de resultaten met behulp van inkoopmedewerkers van I&W vergeleken. Er is vooral gefocust op het aanpassen van de prompt die je meegeeft. Over het algemeen lijken de open source embeddingsmodellen maar matig in hun beheersing van het Nederlands, De taalmodellen die op een laptop kunnen draaien hadden ook moeite met het volgen van instructies. Er lijkt wel aanleiding te zijn om te denken dat een uitgebreide uitleg van de situatie en opdracht in de prompt helpen in het verbeteren van de kwaliteit van de antwoorden.

## [RAG voor inkoop, resultaten en bedenkingen](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/RAG%20voor%20inkoop,%20resultaten%20en%20bedenkingen%20(1).docx)
In dit document worden bevindingen gedeeld met betrekking tot de vraag:  *kunnen we vragen van leveranciers die in een NVI gesteld worden beantwoorden op basis van eerdere Nota van Inlichtingen en andere documentatie?* De documenten die werden meegegeven waren: een Nota van Inlichtingen en een breed scala aan documenten over beleidsadvies en ingenieursdiensten van I&W. Er is een cloudoplossing en een oplossing met een API-key getest. Daarom is er alleen gebruik gemaakt van openbare documentatie. Bij de eerste experimenten is vooral globaal gekeken naar accuraatheid. Er is daarom louter beoordeeld of het antwoord grofweg of helemaal overeenkwam met het daadwerkelijke antwoord vanuit de inkopers (eerste verkenning kwaliteit om potentie in te schatten). Het maakt niet uit of je rekenkracht via Azure of een API-key gebruikt. Hierin zijn steeds dezelfde modellen gebruikt. Beide applicaties lukt het redelijk goed vragen terug te vinden in een Nota van Inlichtingen. Daarentegen leek het amper mogelijk vragen uit een tweede Nota van Inlichtingen te beantwoorden op basis van het aanbestedingsdocument en de eerste Nota van Inlichtingen. Dit kan aan de beperkingen van de data zelf liggen, dus het is lastig om daar meer conclusies uit te trekken.

## Vergelijking open source modellen
Verschillende documenten waarin de state of the art LLM's worden besproken.

### [Versie 1.0: Oktober 2023](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/v1.0%20-%20Vergelijking%20open%20source%20modellen.docx)
Belangrijkste conclusies uit dit document:
- Er wordt een sterke voorkeur uitgesproken voor modellen met minder parameters vanwege de beschikbare rekenkracht, energie en kosten.
- Mistral-7B-OpenOrca lijkt het beste basismodel om verder op te trainen voor chatbotfuncties binnen de Rijksoverheid. De verhouding tussen de prestaties en het aantal parameters is goed.
- Er is gesproken met Bram Vanroy. Hij adviseerd Mistral-modellen te gebruiken in plaats van de zijne. Het blijkt lastig te zijn om een model dat heel weinig in het Nederlands pre-trained is, goed Nederlands te leren met de datasets die momenteel beschikbaar zijn. 
- De Nederlandse datasets die nu beschikbaar zijn, zijn van lage kwaliteit. Echter heeft het Orcaproject (Microsoft) laten zien dat je met relatief veel data van hoge kwaliteit hele goede resultaten kan bereiken. Het vertalen van Orca naar het Nederlands zou dus een meerwaarde zijn, maar valt voor nu buiten de scope.

### [Versie 2.0: Januari 2024](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/v2.0%20-%20Vergelijking%20open%20source%20modellen.docx)
Belangrijkste conclusies uit dit document:
- De modellen gaan gebruikt worden voor RAG (retrieval augmented generation)
- De meest kansrijke modellen zijn:
    - Mistral-7x8B mixture of expert
    - Geitje: het op nederlands gefinetunede mistral-7B model van Rijserberg
    - SciPhi SelfRAG: het voor RAG gefinetunede mistral-7B model met de self-rag dataset
    - Mistral-7B-OpenOrca: de met Orca gefinetunede versie van Mistral
    - Qwen 14 miljard, om ook een niet Mistral model te bekijken

### [Versie 2.1: Maart 2024](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/v2.1%20-%20Vergelijking%20open%20source%20modellen.docx)
De meest kansrijke modellen zijn:
- Mistral-7x8B mixture of expert
- Geitje Ultra
- Zephyr
- SciPhi SelfRAG: het voor RAG gefinetunede mistral-7B model met de self-rag dataset
- Mistral-7B-OpenOrca: de met Orca gefinetunede versie van Mistral

## [Verbetermogelijkheden RAG](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/Verbetermogelijkheden%20RAG.docx)
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

## [Visiestuk SSC-ICT](https://github.com/SSC-ICT-Innovatie/LearningLion-kamervragen/raw/refs/heads/main/!%20project_docs/Project_archief/Visiestuk%20SSC-ICT.docx)
Er worden in dit document een aantal standpunten ingenomen:

1. SSC-ICT gaat geen foundational model (willen) maken: er is geen beschikbaar budget voor een project dat gericht is op dataverzameling. Het is nuttiger om het werk zo in te richten dat we gebruik kunnen maken van toekomstige Nederlandstalige modellen zoals GPT-NL.
2. SSC-ICT gaat nu geen model finetunen: er wordt meerwaarde gehecht aan het maken van iets dat niet op een specifiek model voortbouwt, maar om de flexibiliteit te behouden. Bovendien kan finetunen juist bestaande problematiek zoals bias in de hand werken.
3. We kiezen momenteel voor RAG om een aantal redenen:
    - Je kan extra kennis meegeven zonder het model opnieuw te trainen.
    - Je antwoorden zijn betrouwbaarder omdat ze gebaseerd zijn op louter eigen documenten waarvan je weet dat de inhoud klopt.
    - De technologie is breed inzetbaar binnen de overheid.

Het doel is om een blauwdruk van een RAG-applicatie te ontwikkelen die voor de gehele overheid beschikbaar gemaakt kan worden zodat specifieke organisaties dit kunnen kopiëren. Zo kunnen ze hun eigen knowledge-base toevoegen en zelf keuzes maken over bijvoorbeeld welke LLM gebruikt wordt.

Er worden een aantal zorgen beschreven die er bestaan en hoe RAG dit kan ondervangen:

- **De manier waarop LLM's getraind zijn** Auteursrechtelijk beschermde informatie en mogelijk persoonsgegevens. Het kan dus juridisch twijfelachtig zijn of je de informatie uit de output mag gebruiken.

    Met RAG doe je niets aan deze zorgen. Je kan de architectuur wel zo maken dat het onafhankelijk werkt van welke LLM je gebruikt. Zodra er een LLM beschikbaar is waarbij er geen of minimale zorgen zijn over de manier van trainen, kunnen we die gebruiken (GPT-NL).
- **Wat gebeurt er met de gegevens die in een prompt staan** De (gevoelige) informatie in een prompt die je naar ChatGPT of GPT4 stuurt gaat naar OpenAI.

    Afhankelijk van hoe je het taalmodel aanspreekt, kan je kiezen waar je je gegevens naartoe stuurt. Je kan een open source taalmodel volledig lokaal draaien. Retrieval vindt dus ook lokaal plaats en dus gaat de data nergens naartoe. Hiervoor heb je GPU’s nodig. Dit is waarschijnlijk niet goed schaalbaar. Je zou dit ook in de cloud kunnen doen met de juiste contracten en afspraken. Als je gebruik maakt van een API-key of online service stuur je de data op naar die partij. Deze partij kan het gebruiken voor eigen doeleinden. Deze zorgen hangen dus af van hoe de retrieval plaatsvindt en welke rekenkrcaht daarvoor gebruikt moet worden. 
- **Afhankelijkheidsrelaties die we opbouwen met (Amerikaanse) bedrijven** Hoe meer wij specifieke taalmodellen integreren, hoe afhankelijker wij worden van deze leveranciers.

    Zolang de architectuur is gebouwd dat de modellen inwisselbaar zijn, beperk je de afhankelijkheidsrelaties. Als je kiest voor de cloud ben je daar natuurlijk wel afhankelijk van.

- **Bias in LLM's** Bias komt voort uit de data waarop het model getraind is.

    Je kan in theorie de bias uit de trainingsdata waarop het gebruikte model getraind is reproduceren. Echter limiteer je de antwoorden bij RAG tot de beschikbare context. Dit kan de gevolgen van het gebruik van een model met bias beperken wanneer documenten die je toevoegt geen bias bevatten. Bij het beoordelen van personen moet je altijd blijven opletten!

- **Intransparantie** Het is vaak niet duidelijk hoe een model tot een antwoord komt (black-box property)

    Bij RAG kan je makkelijk herleiden welke informatie gebruikt is om een antwoord te genereren. Dit betekent niet dat hallucinatie uitgesloten is. Je kan het wel makkelijker opsporen.

In het kader van bovenstaande overwegingen is het belangrijk de volgende stappen te ondernemen: 
- Zoek nauwe samenwerking met zoveel mogelijk anderen die hiermee bezig zijn (binnen de overheid);
- Onderzoek wat we met RAG willen doen. Voor welke use cases willen we het gaan gebruiken?;
- En onderzoek hoe de RAG-applicatie gaan runnen. Wat is er nodig om RAG in productie te brengen en waar kun je rekenkracht vandaan halen?



