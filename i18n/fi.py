#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Finnish language translations for Ask AI Plugin.
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
    def multi_book_default_template(self) -> str:
        return """Tässä on tietoa useista kirjoista: {books_metadata} Käyttäjän kysymys: {query} Vastaa kysymykseen yllä olevan kirjatiedon perusteella."""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin tiedot
            'plugin_name': 'Ask AI Plugin',
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
            'stop_button': 'Pysäytä',
            'suggest_button': 'Satunnainen kysymys',
            'copy_response': 'Kopioi vastaus',
            'copy_question_response': 'Kopioi K&&V',
            'export_pdf': 'Vie PDF',
            'export_current_qa': 'Vie Nykyinen K&V',
            'export_history': 'Vie Historia',
            'export_all_history_dialog_title': 'Vie Koko Historia PDF:ksi',
            'export_all_history_title': 'KOKO K&V HISTORIA',
            'export_history_insufficient': 'Viennissä tarvitaan vähintään 2 historiatietuetta.',
            'history_record': 'Tietue',
            'question_label': 'Kysymys',
            'answer_label': 'Vastaus',
            'default_ai': 'Oletus-AI',
            'export_time': 'Viety',
            'total_records': 'Tietueita Yhteensä',
            'info': 'Tiedot',
            'yes': 'Kyllä',
            'no': 'Ei',
            'no_book_selected_title': 'Kirjaa Ei Valittu',
            'no_book_selected_message': 'Valitse kirja ennen kysymysten esittämistä.',
            'set_default_ai_title': 'Aseta Oletus-AI',
            'set_default_ai_message': 'Olet vaihtanut kohteeseen "{0}". Haluatko asettaa sen oletus-AI:ksi tulevia kyselyitä varten?',
            'set_default_ai_success': 'Oletus-AI on asetettu kohteeseen "{0}".',
            'copied': 'Kopioitu!',
            'pdf_exported': 'PDF viety!',
            'export_pdf_dialog_title': 'Vie PDF-muotoon',
            'export_pdf_error': 'PDF-viennin virhe: {0}',
            'no_question': 'Ei kysymystä',
            'no_response': 'Ei vastausta',
            'saved': 'Tallennettu',
            'close_button': 'Sulje',
            
            # UI - Asetuskentät
            'token_label': 'API-avain:',
            'api_key_label': 'API-avain:',
            'model_label': 'Malli:',
            'language_label': 'Kieli:',
            'language_label_old': 'Kieli',
            'base_url_label': 'Perus-URL:',
            'base_url_placeholder': 'Oletus: {default_api_base_url}',
            'shortcut': 'Pikanäppäin',
            'shortcut_open_dialog': 'Avaa dialogi',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Malli',
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
            'loading': 'Ladataan...',
            'loading_text': 'Kysytään',
            'save_success': 'Asetukset tallennettu',
            'sending': 'Lähetetään...',
            'requesting': 'Pyytää',
            'formatting': 'Pyyntö onnistui, muotoillaan',
            
            # UI - Mallilistan toiminto
            'load_models': 'Lataa mallit',
            'use_custom_model': 'Käytä mukautettua mallin nimeä',
            'custom_model_placeholder': 'Syötä mukautettu mallin nimi',
            'model_placeholder': 'Lataa ensin mallit',
            'models_loaded': '{count} mallia ladattu',
            'load_models_failed': 'Mallien lataus epäonnistui: {error}',
            'model_list_not_supported': 'Tämä palveluntarjoaja ei tue automaattista mallilistan hakua',
            'api_key_required': 'Syötä ensin API-avain',
            'invalid_params': 'Virheelliset parametrit',
            'warning': 'Varoitus',
            'success': 'Onnistui',
            'error': 'Virhe',
            
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
            
            # Multi-book feature
            'books_unit': ' kirjaa',
            'new_conversation': 'Uusi keskustelu',
            'single_book': 'Yksittäinen kirja',
            'multi_book': 'Monikirja',
            'deleted': 'Poistettu',
            'history': 'Historia',
            'no_history': 'Ei historiatietueita',
            'clear_current_book_history': 'Tyhjennä nykyisen kirjan historia',
            'confirm_clear_book_history': 'Haluatko varmasti tyhjentää koko historian:\n{book_titles}?',
            'confirm': 'Vahvista',
            'history_cleared': '{deleted_count} historiatietuetta tyhjennetty.',
            'multi_book_template_label': 'Monien kirjojen kehotteen malli:',
            'multi_book_placeholder_hint': 'Käytä {books_metadata} kirjan tiedoille, {query} käyttäjän kysymykselle',
            
            # Virheviestit
            'error': 'Virhe: ',
            'network_error': 'Verkkovirhe',
            'request_timeout': 'Pyyntö aikakatkaistiin',
            'request_failed': 'Pyyntö epäonnistui',
            'question_too_long': 'Kysymys on liian pitkä',
            'auth_token_required_title': 'API-avain Vaaditaan',
            'auth_token_required_message': 'Aseta kelvollinen API-avain Laajennuksen Asetuksissa.',
            'open_configuration': 'Avaa Asetukset',
            'cancel': 'Peruuta',
            'error_preparing_request': 'Pyynnön valmistelu epäonnistui',
            'empty_suggestion': 'Tyhjä ehdotus',
            'process_suggestion_error': 'Virhe ehdotuksen käsittelyssä',
            'unknown_error': 'Tuntematon virhe',
            'unknown_model': 'Tuntematon malli: {model_name}',
            'suggestion_error': 'Ehdotusvirhe',
            'random_question_success': 'Satunnainen kysymys luotu onnistuneesti!',
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
            'no_model_configured': 'AI-mallia ei ole määritetty. Määritä AI-malli asetuksissa.',
            'no_ai_configured_title': 'AI Ei Määritetty',
            'no_ai_configured_message': 'Tervetuloa! Aloittaaksesi kysymysten esittämisen kirjoistasi, sinun on ensin määritettävä AI-palveluntarjoaja.\n\nSuositellaan aloittelijoille:\n• Nvidia AI - Hanki 6 kuukautta ILMAISTA API-käyttöä vain puhelinnumerollasi (luottokorttia ei tarvita)\n• Ollama - Suorita AI-malleja paikallisesti tietokoneellasi (täysin ilmainen ja yksityinen)\n\nHaluatko avata laajennuksen asetukset AI-palveluntarjoajan määrittämiseksi nyt?',
            'open_settings': 'Laajennuksen Asetukset',
            'ask_anyway': 'Kysy Silti',
            'later': 'Myöhemmin',
            'reset_all_data': 'Nollaa Kaikki Tiedot',
            'reset_all_data_warning': 'Tämä poistaa kaikki API-avaimet, kehotusmallit ja paikalliset historiatietueet. Kieliasetuksesi säilytetään. Jatka varoen.',
            'reset_all_data_confirm_title': 'Vahvista Nollaus',
            'reset_all_data_confirm_message': 'Oletko varma, että haluat palauttaa laajennuksen alkuperäiseen tilaan?\n\nTämä poistaa pysyvästi:\n• Kaikki API-avaimet\n• Kaikki mukautetut kehotusmallit\n• Kaikki keskusteluhistorian\n• Kaikki laajennuksen asetukset (kieliasetus säilytetään)\n\nTätä toimintoa ei voi kumota!',
            'reset_all_data_success': 'Kaikki laajennuksen tiedot on nollattu onnistuneesti. Käynnistä calibre uudelleen, jotta muutokset tulevat voimaan.',
            'reset_all_data_failed': 'Laajennuksen tietojen nollaus epäonnistui: {error}',
            'random_question_error': 'Virhe satunnaisen kysymyksen luomisessa',
            'clear_history_failed': 'Historian tyhjennys epäonnistui',
            'clear_history_not_supported': 'Yksittäisen kirjan historian tyhjennystä ei vielä tueta',
            'missing_required_config': 'Puuttuva pakollinen asetus: {key}. Tarkista asetuksesi.',
            'api_key_too_short': 'API-avain on liian lyhyt. Tarkista ja syötä täydellinen avain.',
            
            # API-vastauksen käsittely
            'api_request_failed': 'API-pyyntö epäonnistui: {error}',
            'api_content_extraction_failed': 'Sisältöä ei voitu poimia API-vastauksesta',
            'api_invalid_response': 'Kelvollista API-vastausta ei saatu',
            'api_unknown_error': 'Tuntematon virhe: {error}',
            
            # Streaming-vastauksen käsittely
            'stream_response_code': 'Streaming-vastauksen tilakoodi: {code}',
            'stream_continue_prompt': 'Jatka edellistä vastaustasi toistamatta jo annettua sisältöä.',
            'stream_continue_code_blocks': 'Edellisessä vastauksessasi oli sulkemattomia koodilohkoja. Jatka ja täydennä nämä koodilohkot.',
            'stream_continue_parentheses': 'Edellisessä vastauksessasi oli sulkemattomia sulkeita. Jatka ja varmista, että kaikki sulkeet on suljettu asianmukaisesti.',
            'stream_continue_interrupted': 'Edellinen vastauksesi näyttää keskeytyneen. Jatka ja viimeistele viimeisin ajatuksesi tai selityksesi.',
            'stream_timeout_error': 'Streaming-lähetys ei ole saanut uutta sisältöä 60 sekuntiin, mahdollisesti yhteysongelman vuoksi.',
            
            # API-virheviestit
            'api_version_model_error': 'API-versio tai mallinimi virhe: {message}\n\nPäivitä API-perus-URL arvoon "{base_url}" ja malli arvoon "{model}" tai johonkin muuhun saatavilla olevaan malliin asetuksissa.',
            'api_format_error': 'API-pyyntömuotovirhe: {message}',
            'api_key_invalid': 'API-avain virheellinen tai ei valtuutettu: {message}\n\nTarkista API-avaimesi ja varmista, että API-käyttö on käytössä.',
            'api_rate_limit': 'Pyyntöraja ylitetty, yritä myöhemmin uudelleen\n\nOlet saattanut ylittää ilmaisen käyttökiintiön. Tämä voi johtua seuraavista syistä:\n1. Liian monta pyyntöä minuutissa\n2. Liian monta pyyntöä päivässä\n3. Liian monta syötetokenia minuutissa',
            
            # Konfigurointivirheet
            'missing_config_key': 'Puuttuva pakollinen konfigurointiavain: {key}',
            'api_base_url_required': 'API-perus-URL vaaditaan',
            'model_name_required': 'Mallinimi vaaditaan',
            'api_key_empty': 'API-avain on tyhjä. Syötä kelvollinen API-avain.',
            
            # Mallilistan haku
            'fetching_models_from': 'Haetaan malleja osoitteesta {url}',
            'successfully_fetched_models': '{count} {provider}-mallia haettu',
            'failed_to_fetch_models': 'Mallien haku epäonnistui: {error}',
            
            # Tietoja
            'author_name': 'Sheldon',
            'user_manual': 'Käyttöopas',
            'about_plugin': 'Miksi Ask AI Plugin?',
            'learn_how_to_use': 'Käyttöohjeet',
            'email': 'iMessage',
            
            # Mallikohtaiset asetukset
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Mukautettu',
            'model_enable_streaming': 'Ota streaming käyttöön',
            
            # AI Switcher
            'current_ai': 'Nykyinen tekoäly',
            'no_configured_models': 'Tekoälyä ei määritetty - Määritä asetuksissa',
            
            # Provider specific info
            'nvidia_free_info': '💡 Uudet käyttäjät saavat 6 kuukautta ilmaista API-käyttöä - Luottokorttia ei tarvita',
            
            # Yleiset järjestelmäviestit
            'default_system_message': 'Olet kirja-analyysin asiantuntija. Tehtäväsi on auttaa käyttäjiä ymmärtämään kirjoja paremmin tarjoamalla oivaltavia kysymyksiä ja analyysejä.',
            
            # Request timeout settings
            'request_timeout_label': 'Pyyntöjen aikakatkaisu:',
            'seconds': 'sekuntia',
            'request_timeout_error': 'Pyyntö aikakatkaistiin. Nykyinen aikakatkaisu: {timeout} sekuntia',
            
            # Parallel AI settings
            'parallel_ai_count_label': 'Rinnakkaisten tekoälyjen määrä:',
            'parallel_ai_count_tooltip': 'Samanaikaisesti kyseltävien tekoälymallien määrä (1-2 saatavilla, 3-4 tulossa pian)',
            'parallel_ai_notice': 'Huomaa: Tämä vaikuttaa vain kysymysten lähettämiseen. Satunnaiset kysymykset käyttävät aina yhtä tekoälyä.',
            'suggest_maximize': 'Vinkki: Suurenna ikkunaa nähdäksesi paremmin 3 tekoälyllä',
            'ai_panel_label': 'Tekoäly {index}:',
            'no_ai_available': 'Ei tekoälyä käytettävissä tälle paneelille',
            'add_more_ai_providers': 'Lisää tekoälyntarjoajia asetuksissa',
            'select_ai': '-- Valitse tekoäly --',
            'select_model': '-- Vaihda Malli --',
            'request_model_list': 'Pyydä malliluettelo',
            'coming_soon': 'Tulossa pian',
            'advanced_feature_tooltip': 'Tämä ominaisuus on kehitysvaiheessa. Pysy kuulolla päivityksistä!',
            
            # PDF export section titles
            'pdf_book_metadata': 'KIRJAN METATIEDOT',
            'pdf_question': 'KYSYMYS',
            'pdf_answer': 'VASTAUS',
            'pdf_ai_model_info': 'TEKOÄLYMALLIN TIEDOT',
            'pdf_generated_by': 'LUONUT',
            'pdf_provider': 'Palveluntarjoaja',
            'pdf_model': 'Malli',
            'pdf_api_base_url': 'API-perus-URL',
            'pdf_panel': 'Paneeli',
            'pdf_plugin': 'Liitännäinen',
            'pdf_github': 'GitHub',
            'pdf_software': 'Ohjelmisto',
            'pdf_generated_time': 'Luontiaika',
            'pdf_info_not_available': 'Tietoja ei saatavilla',
        }