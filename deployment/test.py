import unittest

from libraries.preprocessor import Preprocessor


class IngesterTest(unittest.TestCase):

	def test_split(self):
			pre = Preprocessor()
			doc="""Vraag 1: Wat is de hoofdstad van Nederland? Antwoord 1: Amsterdam"""
			self.assertEqual(pre.get_question_and_answer(doc), [['Vraag 1: Wat is de hoofdstad van Nederland?'], ['Antwoord 1: Amsterdam']])
			
			doc = """Vraag 1: Wat is de hoofdstad van Nederland? Antwoord 1: Amsterdam Vraag 2: Wat is de hoofdstad van België? Antwoord 2: Brussel"""
			self.assertEqual(pre.get_question_and_answer(doc), [['Vraag 1: Wat is de hoofdstad van Nederland?', 'Vraag 2: Wat is de hoofdstad van België?'], ['Antwoord 1: Amsterdam', 'Antwoord 2: Brussel']])
			
			doc = """Vraag 1: Wat is de hoofdstad van Nederland? Antwoord 1: Amsterdam Vraag 2: Wat is de hoofdstad van België? Antwoord 2: Brussel Vraag 3: Wat is de hoofdstad van Frankrijk? Antwoord 3: Parijs"""
			self.assertEqual(pre.get_question_and_answer(doc), [['Vraag 1: Wat is de hoofdstad van Nederland?', 'Vraag 2: Wat is de hoofdstad van België?', 'Vraag 3: Wat is de hoofdstad van Frankrijk?'], ['Antwoord 1: Amsterdam', 'Antwoord 2: Brussel', 'Antwoord 3: Parijs']])
			
			doc = """
			Tweede Kamer der Staten-Generaal2
Vergaderjaar 2022–2023  Aanhangsel van de Handelingen 
Vragen gesteld door de leden der Kamer, met de daarop door de 
regering gegeven antwoorden  
3649  
Vragen van het lid Bromet (GroenLinks) aan de Ministers van Landbouw, 
Natuur en Voedselkwaliteit en voor Natuur en Stikstof over het bericht 
«Verguisde stalvloer tegen stikstofuitstoot kan stoppende boer in de weg zitten» (ingezonden 4 juli 2023).

Antwoord van Minister Van der Wal-Zeggelink (Natuur en Stikstof) 
(ontvangen 14 september 2023). Zie ook Aanhangsel Handelingen, vergaderjaar 2022–2023, nr. 3276.

Vraag 1
Kent u het bericht «Verguisde stalvloer tegen stikstofuitstoot kan stoppende boer in de weg zitten»?
1 
Antwoord 1
Ja. 
Vraag 2
Klopt het dat melkveehouders met een emissiearme vloer (meestal) niet voor de piekbelastersregeling in aanmerking komen?

Antwoord 2
Ook een melkveehouder met een emissiearme vloer kan voldoen aan de drempelwaarde van de aanpak piekbelasting. Berekeningen in de tool, AERIUS Check, worden gemaakt op basis van meerdere factoren, waaronder de emissiefacto-ren per huisvestings-systeem zoals vastgesteld in bijlage 1 van de Regeling ammoniak en veehouderij (Rav). Andere aspecten die hierbij meewegen zijn de grootte van het bedrijf en de afstand tot een Natura2000-gebied.

Vraag 3
Zo ja, waarom geldt er voor hun een aftrek, terwijl in de brief van 30 juni 2023 wordt bevestigd dat de emissiearme stalvloeren van voor 2021 niet werken?

1Brabants Dagblad, 2 juli 2023, «Verguisde stalvloer tegen stikstofuitstoot kan stoppende boer in 
de weg zitten: «Dit is zo krom»» (https://www.bd.nl/binnenland/verguisde-stalvloer-tegen-stikstofuitstoot-kan-stoppende-boer-in-de-weg-zitten-dit-is-zo-krom~a1b2a0fc/?cb=dbaa9fe0cf5ce3793898530f1307b5d2&auth_rd=1).

	
ah-tk-20222023-3649
ISSN 0921 - 7398’s-Gravenhage 2023Tweede Kamer, vergaderjaar 2022–2023, Aanhangsel 1Antwoord 3
Binnen het kader van de aanpak piekbelasting en de Lbv wordt uitgegaan van 
de emissiefactoren zoals ze golden op het moment van inregelen van de tool en die op dit moment nog steeds gelden. In de Kamerbrief van 30 juni 2023
2 
is aangegeven dat bij de onderzochte melkveevloeren de reductie van ammoniakemissie die verwacht zou worden volgens de emissiefactoren in bijlage 1 van de Rav in de praktijk helaas niet wordt gehaald. Dit heeft uiteindelijk consequenties voor de emissiefactoren die voor deze stalsyste-men zijn vastgesteld. In genoemde brief wordt nader op deze consequenties ingegaan, waaronder op het proces voor de aanpassing van de emissiefacto-ren voor de emissiearme vloeren in melkveestallen. De emissiefacto-ren zijn op dit moment nog niet aangepast. Zoals aangegeven in het antwoord op vraag 2, worden berekeningen in AERIUS Check gemaakt mede op basis van emissiefactoren per huisvestings-systeem zoals vastgesteld in bijlage 1 van de Rav. Ik onderzoek momenteel wat de mogelijkheden zijn om binnen het kader van de aanpak piekbelasting en de Lbv onzekerheden over deelnamemogelijkheden weg te nemen.

Vraag 4
Om hoeveel extra verborgen piekbelasters gaat het?  
Antwoord 4
Om te toetsen aan de drempelwaarde van de aanpak piekbelasting, moet iedere ondernemer zelf gegevens invoeren in de tool. Er wordt niet gewerkt met een lijst. Om deze reden is ook niet precies te zeggen hoeveel bedrijven extra voldoen aan de drempelwaarde als met een hogere emissiefactor gerekend zou worden. Ik heb het RIVM gevraagd om bij benadering te bepalen om hoeveel bedrijven het zou kunnen gaan. Deze informatie is nodig bij de verdere verkenning van de mogelijkheden.

Vraag 5
Wat is het gevolg als boeren in het systeem invoeren dat ze een emissiearme vloer hebben die niet werkt? Klopt het dat ze alleen een melding krijgen dat hun vloer (mogelijk!) niet werkt, maar verder niets?

Antwoord 5
De tool doet geen uitspraken over de werking van een stalsysteem. De gebruiker vult zelf de aanwezige emissiebronnen in, waarbij voor stalsyste-men automatisch de emissiefactor van ammoniak uit bijlage 1 van de Rav wordt toegepast. Het systeem rekent vervolgens met die emissie. Hierbij wordt een waarschuwing weergegeven dat de werking van sommige staltypen, en daarmee de berekende emissie, onzeker is.

Vraag 6
Hoe groot is het effect op de beleidsresultaten, voor de natuur, als we bepaalde feitelijke piekbelasters niet uitkopen en andere die in de praktijk minder uitstoten wel?

Antwoord 6
Elke ondernemer die ervoor kiest om zijn of haar bedrijf te beëindigen, levert een bijdrage aan het herstel van de natuur. Het niet-beëindigen van onderne-mingen die feitelijk wel voldoen aan de drempelwaarde van de aanpak piekbelasting heeft een remmend effect op de opbrengst van de aanpak.

Vraag 7
Waarom is er dan nog een aftrek voor emissiearme vloeren gezien de conclusies van het Centraal Bureau voor Statistiek (CBS) uit 2019 dat de emissiearme vloeren niet werken nu zijn bevestigd? Moet die aftrek niet nul zijn, zoals het onderzoek concludeert?

2Kamerstuk 29 383, nr. 406.
Tweede Kamer, vergaderjaar 2022–2023, Aanhangsel 2Antwoord 7
In de Kamerbrief van 30 juni jl. is de Kamer geïnformeerd over de resultaten 
van het onderzoek naar de stikstof-fosfaatverhouding in mest bij de excretie en bij het afvoeren van het bedrijf. Dit was één van de vervolgacties op het advies «Stikstofverliezen uit mest in stallen en opslagen» van de Commissie Deskundigen Meststoffenwet (CDM). Het onderzoek is een verificatie van een studie van het Centraal Bureau voor de Statistiek (CBS) uit 2019. In de Kamerbrief van 30 juni 2023
3 ingegaan op het proces voor aanpassing van de 
emissiefactoren voor emissiearme vloeren in melkveestallen. De emissiefacto-ren zijn op dit moment nog niet aangepast. Ik onderzoek momenteel wat de mogelijkheden zijn om binnen het kader van de aanpak piekbelasting en de Lbv onzekerheden over deelnamemogelijkheden weg te nemen.

Vraag 8
Hoeveel melkveehouders hebben via de niet-werkende staltechniek een vergunning voor uitbreiding gekregen?

Antwoord 8
Provincies zijn het bevoegd gezag voor het verlenen van natuurvergunningen. Intern salderen is niet vergunningplichtig op dit moment. Dit betekent dat veehouders niet in alle gevallen toestemming hebben hoeven vragen voor uitbreiding. Daardoor is niet inzichtelijk om hoeveel en welke melkveehouders het precies gaat.

Vraag 9
Hoeveel subsidie is hiervoor verstrekt en hoeveel hebben boeren zelf geïnvesteerd?

Antwoord 9
Zoals aangegeven in het antwoord op vraag 8, is niet inzichtelijk om hoeveel en welke melkveehouders het hier precies gaat. Zonder deze gegevens is het niet mogelijk om te achterhalen of en zo ja, hoeveel subsidie er voor investeringen in deze staltechnieken verstrekt is door het Rijk of door andere overheden.

Vraag 10
Tot hoeveel extra vee en/of emissie heeft dit geleid?  
Antwoord 10
Zoals aangegeven in het antwoord op vraag 8 en 9, is niet inzichtelijk om hoeveel en welke melkveehouders het hier precies gaat. De emissie kan daarnaast verschillen per locatie, afhankelijk van de locatie specifieke omstandigheden. De feitelijke emissie kan hierdoor per individueel bedrijf anders zijn, waardoor het niet mogelijk is om een landelijk beeld te geven. In de monitoring van de totale depositie op de natuur wordt door het RIVM gerekend met de feitelijke emissie. Op dit proces heeft het CBS onderzoek dus geen invloed.

Vraag 11
Is dit een groter of een kleiner probleem dan de Programma Aanpak Stikstof (PAS)-melders, die ook te goeder trouw, maar onterecht mochten uitbreiden?

Antwoord 11
Dit zijn twee verschillende zaken die slecht met elkaar te vergelijken zijn. De PAS-meldingen betreft activiteiten waarvoor ten tijde van het PAS een meldingsplicht gold. Uit de PAS uitspraak volgt dat voor deze activiteiten niet had kunnen worden volstaan met een melding en dat deze activiteiten alsnog een vergunning nodig hebben. De toepassing van emissiearme stallen in de afgelopen jaren heeft daarentegen geleid tot in rechte vaststaande vergunnin-gen.

Vraag 12
Lopen deze boeren het risico dat hun vergunning wordt ingetrokken?  
3Kamerstuk 29 383, nr. 406.
Tweede Kamer, vergaderjaar 2022–2023, Aanhangsel 3Antwoord 12
Verleende Wnb-vergunningen waar geen rechtsmiddel meer tegen open staat 
(dus waar geen bezwaar of beroep meer mogelijk is), zijn onherroepelijk en staan in rechte vast. Deze bieden rechtszekerheid voor de agrariër en zijn er daarvoor in principe geen gevolgen. De Wet natuurbescherming kent artikel 5.4 om vergunningen ambtshalve of op verzoek in te trekken. De provincies zijn op grond van deze wet het bevoegde gezag om te beslissen over aanvragen voor vergunningen en het wijzigen of intrekken daarvan.

Vraag 13
Bent u voornemens de piekbelastersregeling alsnog open te stellen voor de verborgen piekbelasters met een niet-werkende stal? En andere beëindigings-regelingen?

Antwoord 13
Ik onderzoek momenteel of er mogelijkheden zijn om op korte termijn duidelijkheid te bieden aan de ondernemers die het betreft. Over de uitkomsten van dit onderzoek zal ik uw kamer op korte termijn informeren, in ieder geval ruim voor het sluiten van de openstellingsperiode van de Lbv (1 december 2023). De ondernemers die het betreft, adviseer ik om in gesprek te gaan met een zaakbegeleider van de aanpak piekbelasting. Meer informatie over het aanvragen van een zaakbegeleider is beschikbaar op de website aanpakpiekbelasting.nl.

Vraag 14
Kunnen de fabrikanten van deze stallen aansprakelijk worden gesteld en de directies strafrechtelijk vervolgd, net als bij de sjoemeldiesels?

Antwoord 14
Zoals aangegeven in de beantwoording van vergelijkbare Kamervragen van het lid Bromet (GL)
4 is de problematiek rond de werking van emissiearme 
stalsystemen in de praktijk niet te vergelijken met het dieselschandaal. Uit eerder onderzoek van WUR
5 is gebleken dat het nodige mis is met de 
effectiviteit van emissiearme stalsystemen in de praktijk. Dit heeft betrekking op zowel het ontwerp, de beoordeling en het gebruik van deze stalsystemen. Het rapport benadrukte de noodzaak om de effectiviteit van de werking van emissiearme stalsystemen fors te verbeteren en deed daartoe ook aanbeve-lingen. In de Kamerbrief van 25 november 2022
6 is geschetst hoe opvolging 
wordt gegeven aan de aanbevelingen. Bij een aansprakelijkheidsstelling moet kenbaar zijn dat door het doen of nalaten van een ander schade is geleden. Het is aan de koper van een emissiearm stalsysteem om de fabrikant eventueel aansprakelijk te stellen.
4(Aanhangsel Handelingen, vergaderjaar 2022–203, nr. 844).
5Bijlage bij Kamerstuk 29 383, nr. 384.
6Kamerstuk 29 383, nr. 384.
Tweede Kamer, vergaderjaar 2022–2023, Aanhangsel 4"""
			expected_output = [
[
        "Vraag 1 Kent u het bericht «Verguisde stalvloer tegen stikstofuitstoot kan stoppende boer in de weg zitten»? 1",
        "Vraag 2 Klopt het dat melkveehouders met een emissiearme vloer (meestal) niet voor de piekbelastersregeling in aanmerking komen?",
        "Vraag 3 Zo ja, waarom geldt er voor hun een aftrek, terwijl in de brief van 30 juni 2023 wordt bevestigd dat de emissiearme stalvloeren van voor 2021 niet werken? 1Brabants Dagblad, 2 juli 2023, «Verguisde stalvloer tegen stikstofuitstoot kan stoppende boer in de weg zitten: «Dit is zo krom»» (https://www.bd.nl/binnenland/verguisde-stalvloer-tegen-stikstofuitstoot-kan-stoppende-boer-in-de-weg-zitten-dit-is-zo-krom~a1b2a0fc/?cb=dbaa9fe0cf5ce3793898530f1307b5d2&auth_rd=1). ah-tk-20222023-3649 ISSN 0921 - 7398’s-Gravenhage 2023Tweede Kamer, vergaderjaar 2022–2023, Aanhangsel 1",
        "Vraag 4 Om hoeveel extra verborgen piekbelasters gaat het?",
        "Vraag 5 Wat is het gevolg als boeren in het systeem invoeren dat ze een emissiearme vloer hebben die niet werkt? Klopt het dat ze alleen een melding krijgen dat hun vloer (mogelijk!) niet werkt, maar verder niets?",
        "Vraag 6 Hoe groot is het effect op de beleidsresultaten, voor de natuur, als we bepaalde feitelijke piekbelasters niet uitkopen en andere die in de praktijk minder uitstoten wel?",
        "Vraag 7 Waarom is er dan nog een aftrek voor emissiearme vloeren gezien de conclusies van het Centraal Bureau voor Statistiek (CBS) uit 2019 dat de emissiearme vloeren niet werken nu zijn bevestigd? Moet die aftrek niet nul zijn, zoals het onderzoek concludeert? 2Kamerstuk 29 383, nr. 406. Tweede Kamer, vergaderjaar 2022–2023, Aanhangsel 2",
        "Vraag 8 Hoeveel melkveehouders hebben via de niet-werkende staltechniek een vergunning voor uitbreiding gekregen?",
        "Vraag 9 Hoeveel subsidie is hiervoor verstrekt en hoeveel hebben boeren zelf geïnvesteerd?",
        "Vraag 10 Tot hoeveel extra vee en/of emissie heeft dit geleid?",
        "Vraag 11 Is dit een groter of een kleiner probleem dan de Programma Aanpak Stikstof (PAS)-melders, die ook te goeder trouw, maar onterecht mochten uitbreiden?",
        "Vraag 12 Lopen deze boeren het risico dat hun vergunning wordt ingetrokken? 3Kamerstuk 29 383, nr. 406. Tweede Kamer, vergaderjaar 2022–2023, Aanhangsel 3",
        "Vraag 13 Bent u voornemens de piekbelastersregeling alsnog open te stellen voor de verborgen piekbelasters met een niet-werkende stal? En andere beëindigings-regelingen?",
        "Vraag 14 Kunnen de fabrikanten van deze stallen aansprakelijk worden gesteld en de directies strafrechtelijk vervolgd, net als bij de sjoemeldiesels?"
    ],
    [
        "Antwoord 1 Ja.",
        "Antwoord 2 Ook een melkveehouder met een emissiearme vloer kan voldoen aan de drempelwaarde van de aanpak piekbelasting. Berekeningen in de tool, AERIUS Check, worden gemaakt op basis van meerdere factoren, waaronder de emissiefacto-ren per huisvestings-systeem zoals vastgesteld in bijlage 1 van de Regeling ammoniak en veehouderij (Rav). Andere aspecten die hierbij meewegen zijn de grootte van het bedrijf en de afstand tot een Natura2000-gebied.",
        "Antwoord 3 Binnen het kader van de aanpak piekbelasting en de Lbv wordt uitgegaan van de emissiefactoren zoals ze golden op het moment van inregelen van de tool en die op dit moment nog steeds gelden. In de Kamerbrief van 30 juni 2023 2 is aangegeven dat bij de onderzochte melkveevloeren de reductie van ammoniakemissie die verwacht zou worden volgens de emissiefactoren in bijlage 1 van de Rav in de praktijk helaas niet wordt gehaald. Dit heeft uiteindelijk consequenties voor de emissiefactoren die voor deze stalsyste-men zijn vastgesteld. In genoemde brief wordt nader op deze consequenties ingegaan, waaronder op het proces voor de aanpassing van de emissiefacto-ren voor de emissiearme vloeren in melkveestallen. De emissiefacto-ren zijn op dit moment nog niet aangepast. Zoals aangegeven in het antwoord op vraag 2, worden berekeningen in AERIUS Check gemaakt mede op basis van emissiefactoren per huisvestings-systeem zoals vastgesteld in bijlage 1 van de Rav. Ik onderzoek momenteel wat de mogelijkheden zijn om binnen het kader van de aanpak piekbelasting en de Lbv onzekerheden over deelnamemogelijkheden weg te nemen.",
        "Antwoord 4 Om te toetsen aan de drempelwaarde van de aanpak piekbelasting, moet iedere ondernemer zelf gegevens invoeren in de tool. Er wordt niet gewerkt met een lijst. Om deze reden is ook niet precies te zeggen hoeveel bedrijven extra voldoen aan de drempelwaarde als met een hogere emissiefactor gerekend zou worden. Ik heb het RIVM gevraagd om bij benadering te bepalen om hoeveel bedrijven het zou kunnen gaan. Deze informatie is nodig bij de verdere verkenning van de mogelijkheden.",
        "Antwoord 5 De tool doet geen uitspraken over de werking van een stalsysteem. De gebruiker vult zelf de aanwezige emissiebronnen in, waarbij voor stalsyste-men automatisch de emissiefactor van ammoniak uit bijlage 1 van de Rav wordt toegepast. Het systeem rekent vervolgens met die emissie. Hierbij wordt een waarschuwing weergegeven dat de werking van sommige staltypen, en daarmee de berekende emissie, onzeker is.",
        "Antwoord 6 Elke ondernemer die ervoor kiest om zijn of haar bedrijf te beëindigen, levert een bijdrage aan het herstel van de natuur. Het niet-beëindigen van onderne-mingen die feitelijk wel voldoen aan de drempelwaarde van de aanpak piekbelasting heeft een remmend effect op de opbrengst van de aanpak.",
        "Antwoord 7 In de Kamerbrief van 30 juni jl. is de Kamer geïnformeerd over de resultaten van het onderzoek naar de stikstof-fosfaatverhouding in mest bij de excretie en bij het afvoeren van het bedrijf. Dit was één van de vervolgacties op het advies «Stikstofverliezen uit mest in stallen en opslagen» van de Commissie Deskundigen Meststoffenwet (CDM). Het onderzoek is een verificatie van een studie van het Centraal Bureau voor de Statistiek (CBS) uit 2019. In de Kamerbrief van 30 juni 2023 3 ingegaan op het proces voor aanpassing van de emissiefactoren voor emissiearme vloeren in melkveestallen. De emissiefacto-ren zijn op dit moment nog niet aangepast. Ik onderzoek momenteel wat de mogelijkheden zijn om binnen het kader van de aanpak piekbelasting en de Lbv onzekerheden over deelnamemogelijkheden weg te nemen.",
        "Antwoord 8 Provincies zijn het bevoegd gezag voor het verlenen van natuurvergunningen. Intern salderen is niet vergunningplichtig op dit moment. Dit betekent dat veehouders niet in alle gevallen toestemming hebben hoeven vragen voor uitbreiding. Daardoor is niet inzichtelijk om hoeveel en welke melkveehouders het precies gaat.",
        "Antwoord 9 Zoals aangegeven in het antwoord op vraag 8, is niet inzichtelijk om hoeveel en welke melkveehouders het hier precies gaat. Zonder deze gegevens is het niet mogelijk om te achterhalen of en zo ja, hoeveel subsidie er voor investeringen in deze staltechnieken verstrekt is door het Rijk of door andere overheden.",
        "Antwoord 10 Zoals aangegeven in het antwoord op vraag 8 en 9, is niet inzichtelijk om hoeveel en welke melkveehouders het hier precies gaat. De emissie kan daarnaast verschillen per locatie, afhankelijk van de locatie specifieke omstandigheden. De feitelijke emissie kan hierdoor per individueel bedrijf anders zijn, waardoor het niet mogelijk is om een landelijk beeld te geven. In de monitoring van de totale depositie op de natuur wordt door het RIVM gerekend met de feitelijke emissie. Op dit proces heeft het CBS onderzoek dus geen invloed.",
        "Antwoord 11 Dit zijn twee verschillende zaken die slecht met elkaar te vergelijken zijn. De PAS-meldingen betreft activiteiten waarvoor ten tijde van het PAS een meldingsplicht gold. Uit de PAS uitspraak volgt dat voor deze activiteiten niet had kunnen worden volstaan met een melding en dat deze activiteiten alsnog een vergunning nodig hebben. De toepassing van emissiearme stallen in de afgelopen jaren heeft daarentegen geleid tot in rechte vaststaande vergunnin-gen.",
        "Antwoord 12 Verleende Wnb-vergunningen waar geen rechtsmiddel meer tegen open staat (dus waar geen bezwaar of beroep meer mogelijk is), zijn onherroepelijk en staan in rechte vast. Deze bieden rechtszekerheid voor de agrariër en zijn er daarvoor in principe geen gevolgen. De Wet natuurbescherming kent artikel 5.4 om vergunningen ambtshalve of op verzoek in te trekken. De provincies zijn op grond van deze wet het bevoegde gezag om te beslissen over aanvragen voor vergunningen en het wijzigen of intrekken daarvan.",
        "Antwoord 13 Ik onderzoek momenteel of er mogelijkheden zijn om op korte termijn duidelijkheid te bieden aan de ondernemers die het betreft. Over de uitkomsten van dit onderzoek zal ik uw kamer op korte termijn informeren, in ieder geval ruim voor het sluiten van de openstellingsperiode van de Lbv (1 december 2023). De ondernemers die het betreft, adviseer ik om in gesprek te gaan met een zaakbegeleider van de aanpak piekbelasting. Meer informatie over het aanvragen van een zaakbegeleider is beschikbaar op de website aanpakpiekbelasting.nl.",
        "Antwoord 14 Zoals aangegeven in de beantwoording van vergelijkbare Kamervragen van het lid Bromet (GL) 4 is de problematiek rond de werking van emissiearme stalsystemen in de praktijk niet te vergelijken met het dieselschandaal. Uit eerder onderzoek van WUR 5 is gebleken dat het nodige mis is met de effectiviteit van emissiearme stalsystemen in de praktijk. Dit heeft betrekking op zowel het ontwerp, de beoordeling en het gebruik van deze stalsystemen. Het rapport benadrukte de noodzaak om de effectiviteit van de werking van emissiearme stalsystemen fors te verbeteren en deed daartoe ook aanbeve-lingen. In de Kamerbrief van 25 november 2022 6 is geschetst hoe opvolging wordt gegeven aan de aanbevelingen. Bij een aansprakelijkheidsstelling moet kenbaar zijn dat door het doen of nalaten van een ander schade is geleden. Het is aan de koper van een emissiearm stalsysteem om de fabrikant eventueel aansprakelijk te stellen. 4(Aanhangsel Handelingen, vergaderjaar 2022–203, nr. 844). 5Bijlage bij Kamerstuk 29 383, nr. 384. 6Kamerstuk 29 383, nr."
    ]]
			self.assertEqual(pre.get_question_and_answer(doc), expected_output)

	def testGetContext(self):
			self.maxDiff = None
			pre = Preprocessor()
			self.assertEqual("""Tweede Kamer der Staten-Generaal 2
Vergaderjaar 2023–2024 Aanhangsel van de Handelingen
Vragen gesteld door de leden der Kamer, met de daarop door de
regering gegeven antwoorden
1433
Vragen van het lid Kostic ´ (PvdD) aan de Minister voor Natuur en Stikstof over
het aanpassen van antwoorden op schriftelijke vragen over de landelijke
vrijstellingslijst en het toch niet uitvoeren van een aangenomen motie, vlak na
gesprekken met de jagerslobby (ingezonden 29 februari 2024).
Antwoord van Minister Van der Wal-Zeggelink (Natuur en Stikstof)
(ontvangen 5 april 2024). Zie ook Aanhangsel Handelingen, vergaderjaar
2023–2024, nr. 1283.""",pre.get_context("""Tweede Kamer der Staten-Generaal 2
Vergaderjaar 2023–2024 Aanhangsel van de Handelingen
Vragen gesteld door de leden der Kamer, met de daarop door de
regering gegeven antwoorden
1433
Vragen van het lid Kostic ´ (PvdD) aan de Minister voor Natuur en Stikstof over
het aanpassen van antwoorden op schriftelijke vragen over de landelijke
vrijstellingslijst en het toch niet uitvoeren van een aangenomen motie, vlak na
gesprekken met de jagerslobby (ingezonden 29 februari 2024).
Antwoord van Minister Van der Wal-Zeggelink (Natuur en Stikstof)
(ontvangen 5 april 2024). Zie ook Aanhangsel Handelingen, vergaderjaar
2023–2024, nr. 1283.
Vraag 1
Kunt u bevestigen dat de Kamer een motie van de Partij voor de Dieren heeft
aangenomen, waarmee de regering wordt verzocht om diersoorten die in hun
voortbestaan worden bedreigd per direct van de landelijke vrijstellingslijst af
te halen?1
Antwoord 1
Ja.
Vraag 2
Kunt u bevestigen dat u op 15 februari 2024 in antwoorden op schriftelijke
vragen het volgende schreef aan de Kamer: «Om aan de motie tegemoet te
komen, zal ik voorbereidingen treffen voor het intrekken van de vrijstelling en
de aanwijzing van konijn, houtduif en kauw»?2
Antwoord 2
Ja. Op 15 februari 2024 heb ik uw Kamer, in antwoord op vragen van het lid
Akerboom (PvdD) over de landelijke vrijstellingslijst (Aanhangsel Handelin-
gen, vergaderjaar 2023–2024, nr. 1045), geïnformeerd over de wijze waarop ik
uitvoering wil geven aan de motie van het lid Akerboom, 36 410 XIV, nr. 9,
waarin wordt opgeroepen de soorten die in hun voortbestaan worden
bedreigd per direct van de vrijstellingslijst af te halen. Door een menselijke
fout is op 15 februari 2024 een verkeerde versie van mijn antwoord verstuurd,
hetgeen ik betreur.
1 Motie van het lid Akerboom (PvdD) over diersoorten die in hun voortbestaan worden bedreigd
per direct van de landelijke vrijstellingslijst af halen (Kamerstuk 36 410 XIV, nr. 9)
2 Antwoorden op schriftelijke vragen van het lid Akerboom over de landelijke vrijstellingslijst
(deze versie is offline gehaald)
ah-tk-20232024-1433
ISSN 0921 - 7398
’s-Gravenhage 2024 Tweede Kamer, vergaderjaar 2023–2024, Aanhangsel 1"""))


if __name__ == '__main__':
		unittest.main()
