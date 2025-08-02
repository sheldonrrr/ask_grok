#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Finnish language translations for Ask Grok plugin.
"""

from ..models.base import BaseTranslation, TranslationRegistry, AIProvider


@TranslationRegistry.register
class FinnishTranslation(BaseTranslation):
    """Finnish language translation."""
    
    @property
    def code(self) -> str:
        return "fi"
    
    @property
    def name(self) -> str:
        return "Suomi"
    
    @property
    def default_template(self) -> str:
        return 'Kirjasta "{title}": Kirjailija: {author}, Kustantaja: {publisher}, Julkaisuvuosi: {pubyear}, kirjan kieli: {language}, Sarja: {series}, Kysymykseni on: {query}'
    
    @property
    def suggestion_template(self) -> str:
        return """Olet kirja-arvostelun asiantuntija. Kirjalle "{title}" kirjailijana {author}, julkaisukieli on {language}, luo YKSI oivaltava kysymys, joka auttaa lukijoita ymmärtämään kirjaa paremmin. Säännöt: 1. Palauta VAIN kysymys, ilman johdantoa tai selitystä 2. Keskity kirjan sisältöön, älä pelkästään otsikkoon 3. Tee kysymyksestä käytännöllinen ja ajatuksia herättävä 4. Pidä se lyhyenä (30-200 sanaa) 5. Ole luova ja luo eri kysymys joka kerta, myös samalle kirjalle"""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin tiedot
            'plugin_name': 'Ask Grok',
            'plugin_desc': 'Kysy kirjasta tekoälyn avulla',
            
            # UI - Välilehdet ja osiot
            'config_title': 'Asetukset',
            'general_tab': 'Yleiset',
            'ai_models': 'Tekoäly',
            'shortcuts': 'Pikanäppäimet',
            'about': 'Tietoja',
            'metadata': 'Metatiedot',
            
            # UI - Painikkeet ja toiminnot
            'ok_button': 'OK',
            'save_button': 'Tallenna',
            'send_button': 'Lähetä',
            'suggest_button': 'Satunnainen kysymys',
            'copy_response': 'Kopioi vastaus',
            'copy_question_response': 'Kopioi K&&V',
            'copied': 'Kopioitu!',
            
            # UI - Asetuskentät
            'token_label': 'API-avain:',
            'model_label': 'Malli:',
            'language_label': 'Kieli',
            'base_url_label': 'Perus-URL:',
            'base_url_placeholder': 'Oletus: {default_api_base_url}',
            'shortcut': 'Pikanäppäin',
            'shortcut_open_dialog': 'Avaa dialogi',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Malli',
            'current_ai': 'Nykyinen tekoäly:',
            'action': 'Toiminto',
            'reset_button': 'Nollaa',
            'prompt_template': 'Kehotepohja',
            'ask_prompts': 'Kysymyskehoteet',
            'random_questions_prompts': 'Satunnaisten kysymysten kehoteet',
            'display': 'Näyttö',
            
            # UI - Dialogielementit
            'input_placeholder': 'Kirjoita kysymyksesi tähän...',
            'response_placeholder': 'Vastaus tulee pian...',
            
            # UI - Valikkovaihtoehdot
            'menu_title': 'Kysy',
            'menu_ask': 'Kysy {model}',
            
            # UI - Tilaviestit
            'loading': 'Ladataan',
            'loading_text': 'Kysytään',
            'save_success': 'Asetukset tallennettu',
            'sending': 'Lähetetään...',
            'requesting': 'Pyytää',
            'formatting': 'Pyyntö onnistui, muotoillaan',
            
            # Metatietokentät
            'metadata_title': 'Otsikko',
            'metadata_authors': 'Kirjailija',
            'metadata_publisher': 'Kustantaja',
            'metadata_pubyear': 'Julkaisupäivä',
            'metadata_language': 'Kieli',
            'metadata_series': 'Sarja',
            'no_metadata': 'Ei metatietoja',
            'no_series': 'Ei sarjaa',
            'unknown': 'Tuntematon',
            
            # Virheviestit
            'error': 'Virhe: ',
            'network_error': 'Verkkovirhe',
            'request_timeout': 'Pyyntö aikakatkaistiin',
            'request_failed': 'Pyyntö epäonnistui',
            'question_too_long': 'Kysymys on liian pitkä',
            'auth_token_required_title': 'API-avain vaaditaan',
            'auth_token_required_message': 'Aseta API-avain asetuksissa',
            'error_preparing_request': 'Virhe pyyntöä valmistellessa',
            'empty_suggestion': 'Tyhjä ehdotus',
            'process_suggestion_error': 'Virhe ehdotuksen käsittelyssä',
            'unknown_error': 'Tuntematon virhe',
            'unknown_model': 'Tuntematon malli: {model_name}',
            'suggestion_error': 'Ehdotusvirhe',
            'book_title_check': 'Kirjan nimi vaaditaan',
            'avoid_repeat_question': 'Käytä eri kysymystä',
            'empty_answer': 'Tyhjä vastaus',
            'invalid_response': 'Virheellinen vastaus',
            'auth_error_401': 'Ei valtuutettu',
            'auth_error_403': 'Pääsy evätty',
            'rate_limit': 'Liian monta pyyntöä',
            'invalid_json': 'Virheellinen JSON',
            'no_response': 'Ei vastausta',
            'template_error': 'Pohjavirhe',
            'no_model_configured': 'Tekoälymallia ei ole määritetty. Määritä tekoälymalli asetuksissa.',
            'random_question_error': 'Virhe satunnaisen kysymyksen luonnissa',
            'clear_history_failed': 'Historian tyhjennys epäonnistui',
            'clear_history_not_supported': 'Yksittäisen kirjan historian tyhjennystä ei vielä tueta',
            
            # Tietoja
            'author_name': 'Sheldon',
            'user_manual': 'Käyttöopas',
            'about_plugin': 'Miksi Ask Grok?',
            'learn_how_to_use': 'Käyttöohjeet',
            'email': 'iMessage',
            
            # Mallikohtaiset asetukset
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
        }
