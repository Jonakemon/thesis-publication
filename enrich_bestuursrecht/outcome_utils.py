import re

from models import Verdict

gegrond_indicators = ['vernietigt de uitspraak van de rechtbank', 'vernietigt het bestreden besluit', 'verklaart het beroep gegrond', 'vernietigt het besluit van het college van gedeputeerde staten', 'wijst het verzoek tot het treffen van een voorlopige voorziening toe', 'verklaart het verzet gegrond',
                      'verklaart het hoger beroep gegrond', 'wijst het verzoek om een voorlopige voorziening toe', 'verklaart het beroep in verband met het niet tijdig nemen van een besluit op bezwaar gegrond',
                      'verzoek tot beperkte kennisneming gerechtvaardigd', 'beperkte kennisneming gerechtvaardigd', 'wijst het verzoek om voorlopige voorziening toe',
                      'verklaart de beroepen gegrond', 'wijst het verzoek toe', 'schorst bij wijze van voorlopige voorziening het besluit', 'schorst het bestreden besluit ',
                      'treft de voorlopige voorziening dat', 'verklaart het beroep tegen het vervangingsbesluit gegrond', 'schorst het bestreden besluit']
ongegrond_indicators = ['De rechtbank verklaart het beroep ongegrond', 'bevestigt de aangevallen uitspraak', 'verklaart het beroep ongegrond',
                        'De voorzieningenrechter wijst het verzoek om voorlopige voorziening af', 'wijst de verzoeken om een voorlopige voorziening af',
                        'verklaart het beroep tegen het vervangingsbesluit ongegrond', 'wijst de verzoeken af', 'wijst het verzoek af', 'wijst het verzoek om een voorlopige voorziening af', 'bevestigt de beslissing van de kantonrechter', 'et beroep is ongegrond',
                        'bevestigt de aangevallen uitspraken',
                        'wijst de verzoeken om voorlopige voorziening af', 'De beroepen zijn ongegrond', 'bevestigt de uitspraak van de rechtbank']
niet_ontvankelijk_indicators = ['verklaart de beroepen voor zover gericht tegen het niet tijdig nemen van een besluit niet-ontvankelijk', 'verklaart het beroep niet ontvankelijk',
                                'verklaart het beroep tegen het bestreden besluit niet-ontvankelijk', 'verklaart het beroep niet-ontvankelijk']
onbevoegd_indicators = ['verklaart zich onbevoegd']
toch_gegrond_indicators = ['veroordeelt verweerder tot betaling', 'veroordeelt verweerder in de kosten', 'draagt verweerder op een nieuwe uitspraak op het bezwaar']


def determine_outcome(verdict: Verdict):
    text = verdict.beslissings_text

    if is_gegrond(text):
        return 'gegrond'

    if is_ongegrond(text):
        return 'ongegrond'

    if is_niet_ontvankelijk(text):
        return 'niet_ontvankelijk'

    if is_onbevoegd(text):
        return 'onbevoegd'

    if toch_gegrond(text):
        return 'gegrond'

    return 'unknown'


def is_gegrond(text):
    if any(indicator in text for indicator in toch_gegrond_indicators):
        return True

    pattern = re.compile('(verklaart het beroep.* gegrond)|(het .*gebrek .*te herstellen)')
    hits = pattern.search(text)
    if hits:
        return True


def toch_gegrond(text):
    if any(indicator in text for indicator in gegrond_indicators):
        return True

    pattern = re.compile('(veroordeelt .*in de proceskosten)')
    hits = pattern.search(text)
    if hits:
        return True


def is_onbevoegd(text):
    if any(indicator in text for indicator in onbevoegd_indicators):
        return True

    pattern = re.compile('(verklaart zich onbevoegd)')
    hits = pattern.search(text)
    if hits:
        return True


def is_ongegrond(text):
    if any(indicator in text for indicator in ongegrond_indicators):
        return True

    pattern = re.compile('(verklaart .*ongegrond)|(wijst het verzoek .*af)')
    hits = pattern.search(text)
    if hits:
        return True


def is_niet_ontvankelijk(text):
    if any(indicator in text for indicator in niet_ontvankelijk_indicators):
        return True

    pattern = re.compile('(verklaart .*niet-ontvankelijk)|(verklaart de beroepen .*niet.ontvankelijk)|(verklaart het verzoek .*niet-ontvankelijk)')
    hits = pattern.search(text)
    if hits:
        return True
