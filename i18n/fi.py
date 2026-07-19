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
        return 'Konteksti: Autat calibre-sovelluksen (http://calibre-ebook.com), tehokkaan e-kirjojen hallintasovelluksen, käyttäjää "Ask AI Plugin" -liitännäisen kautta. Tämä liitännäinen mahdollistaa käyttäjien esittää kysymyksiä calibre-kirjastossaan olevista kirjoista. Huomautus: Tämä liitännäinen voi vastata vain valitun kirjan sisältöä, teemoja tai aiheeseen liittyviä kysymyksiä - se ei voi suoraan muokata kirjan metatietoja tai suorittaa calibre-toimintoja. Kirjan tiedot: Otsikko: "{title}", Tekijä: {author}, Kustantaja: {publisher}, Julkaisuvuosi: {pubyear}, Kieli: {language}, Sarja: {series}. Käyttäjän kysymys: {query}. Anna hyödyllinen vastaus kirjan tietojen ja tietämyksesi perusteella.'
    
    @property
    def suggestion_template(self) -> str:
        return """Olet asiantunteva kirja-arvostelija. Kirjasta "{title}" kirjoittanut {author}, julkaisukieli on {language}, luo YKSI oivaltava kysymys, joka auttaa lukijoita ymmärtämään kirjan ydinasioita, käytännön sovelluksia tai ainutlaatuisia näkökulmia paremmin. Säännöt: 1. Palauta AINOASTAAN kysymys, ilman johdantoa tai selitystä 2. Keskity kirjan sisältöön, ei vain sen otsikkoon 3. Tee kysymyksestä käytännöllinen ja ajatuksia herättävä 4. Pidä se tiiviinä (30-200 sanaa) 5. Ole luova ja luo joka kerta erilainen kysymys, jopa samasta kirjasta"""
    
    @property
    def multi_book_default_template(self) -> str:
        return """Tässä on tietoa useista kirjoista: {books_metadata} Käyttäjän kysymys: {query} Ole hyvä ja vastaa kysymykseen yllä olevan kirjatiedon perusteella."""
    
    @property
    def translations(self) -> dict:
        return {
            # Plugin information
            'plugin_name': 'Ask AI -lisäosa',
            'plugin_desc': 'Kysy kirjoista tekoälyn avulla',
            
            # UI - Tabs and sections
            'config_title': 'Asetukset',
            'general_tab': 'Yleiset',
            'ai_models': 'Tekoälypalveluntarjoajat',
            'shortcuts': 'Pikakuvakkeet',
            'shortcuts_note': "Voit mukauttaa näitä pikakuvakkeita Calibressa: Asetukset -> Pikakuvakkeet (hae 'Ask AI').\nTämä sivu näyttää oletus-/esimerkkikuvakkeet. Jos olet muuttanut niitä Pikakuvakkeissa, Calibren asetukset ovat etusijalla.",
            'prompts_tab': 'Kehotteet',
            'about': 'Tietoja',
            'metadata': 'Metatiedot',
            
            # Section subtitles
            'language_settings': 'Kieli',
            'language_subtitle': 'Valitse haluamasi käyttöliittymän kieli',
            'ai_providers_subtitle': 'Määritä tekoälypalveluntarjoajat ja valitse oletustekoäly',
            'prompts_subtitle': 'Mukauta, miten kysymykset lähetetään tekoälylle',
            'export_settings_subtitle': 'Aseta oletuskansio PDF-tiedostojen viemiseen',
            'reset_all_data_subtitle': 'Varoitus: Tämä poistaa pysyvästi kaikki asetuksesi ja tietosi',
            
            # Prompts tab
            'language_preference_title': 'Kieliasetukset',
            'language_preference_subtitle': 'Hallitse, vastaako tekoälyn vastaukset käyttöliittymäsi kieltä',
            'prompt_templates_title': 'Kehotemallit',
            'prompt_templates_subtitle': 'Mukauta, miten kirjan tiedot lähetetään tekoälylle käyttämällä dynaamisia kenttiä, kuten {title}, {author}, {query}',
            'ask_prompts': 'Kysy kehotteita',
            'random_questions_prompts': 'Satunnaisten kysymysten kehotteet',
            'multi_book_prompts_label': 'Usean kirjan kehotteet',
            'multi_book_placeholder_hint': 'Käytä {books_metadata} kirjan tiedoille, {query} käyttäjän kysymykselle',
            'dynamic_fields_title': 'Dynaamisten kenttien viite',
            'dynamic_fields_subtitle': 'Saatavilla olevat kentät ja esimerkkisarvot Mary Shelleyn "Frankensteinista"',
            'dynamic_fields_examples': '<b>{title}</b> → Frankenstein<br><b>{author}</b> → Mary Shelley<br><b>{publisher}</b> → Lackington, Hughes, Harding, Mavor & Jones<br><b>{pubyear}</b> → 1818<br><b>{language}</b> → Englanti<br><b>{series}</b> → (ei mikään)<br><b>{query}</b> → Kysymystekstisi',
            'reset_prompts': 'Palauta kehotteet oletusarvoihin',
            'reset_prompts_confirm': 'Oletko varma, että haluat palauttaa kaikki kehotemallit oletusarvoihin? Tätä toimintoa ei voi kumota.',
            'unsaved_changes_title': 'Tallentamattomia muutoksia',
            'unsaved_changes_message': 'Kehotteet-välilehdellä on tallentamattomia muutoksia. Haluatko tallentaa ne?',
            'use_interface_language': 'Pyydä aina tekoälyä vastaamaan nykyisen lisäosan käyttöliittymän kielellä',
            'language_instruction_label': 'Kehotteisiin lisätty kieliohje:',
            'language_instruction_text': 'Vastaa {language_name}.',
            
            # Persona settings
            'persona_title': 'Persona',
            'persona_subtitle': 'Määritä tutkimustaustasi ja tavoitteesi auttaaksesi tekoälyä tarjoamaan osuvampia vastauksia',
            'use_persona': 'Käytä personaa',
            'persona_label': 'Persona',
            'persona_placeholder': 'Tutkijana haluan tutkia kirjan dataa.',
            'persona_hint': 'Mitä enemmän tekoäly tietää kohteestasi ja taustastasi, sitä parempia ovat tutkimus- tai generointitulokset.',
            
            # UI - Buttons and actions
            'ok_button': 'OK',
            'save_button': 'Tallenna',
            'send_button': 'Lähetä',
            'stop_button': 'Pysäytä',
            'suggest_button': 'Satunnainen kysymys',
            'copy_response': 'Kopioi vastaus',
            'copy_question_response': 'Kopioi K&V',
            'export_pdf': 'Vie PDF',
            'export_current_qa': 'Vie nykyinen K&V',
            'export_history': 'Vie historia',
            'export_all_history_dialog_title': 'Vie koko historia PDF-muotoon',
            'export_all_history_title': 'KOKO K&V HISTORIA',
            'export_history_insufficient': 'Vähintään 2 historiatietuetta tarvitaan vientiin.',
            'history_record': 'Tietue',
            'question_label': 'Kysymys',
            'answer_label': 'Vastaus',
            'default_ai': 'Oletustekoäly',
            'export_time': 'Viety klo',
            'total_records': 'Yhteensä tietueita',
            'info': 'Tietoa',
            'yes': 'Kyllä',
            'no': 'Ei',
            'no_book_selected_title': 'Kirjaa ei valittu',
            'no_book_selected_message': 'Valitse kirja ennen kysymysten esittämistä.',
            'set_default_ai_title': 'Aseta oletustekoäly',
            'set_default_ai_message': 'Olet vaihtanut "{0}":aan. Haluatko asettaa sen oletustekoälyksi tuleville kyselyille?',
            'set_default_ai_success': 'Oletustekoälyksi on asetettu "{0}".',
            'default_ai_mismatch_title': 'Oletus-tekoäly muuttunut',
            'default_ai_mismatch_message': 'Oletus-tekoäly on asetuksissa vaihdettu "{default_ai}"-tyyppiseksi,\nmutta nykyinen valinta on "{current_ai}".\n\nHaluatko vaihtaa uuteen oletus-tekoälyyn?',
            'copied': 'Kopioitu!',
            'pdf_exported': 'PDF viety!',
            'export_pdf_dialog_title': 'Vie PDF-muotoon',
            'export_pdf_error': 'PDF-tiedoston vienti epäonnistui: {0}',
            'no_question': 'Ei kysymystä',
            'no_response': 'Ei vastausta',
            'saved': 'Tallennettu',
            'close_button': 'Sulje',
            'open_local_tutorial': 'Avaa paikallinen opas',
            'tutorial_open_failed': 'Oppaiden avaaminen epäonnistui',
            'tutorial': 'Opas',
            
            'model_display_name_perplexity': 'Perplexity',
            
            # UI - Configuration fields
            'token_label': 'API-avain:',
            'api_key_label': 'API-avain:',
            'model_label': 'Malli:',
            'language_label': 'Kieli:',
            'language_label_old': 'Kieli',
            'base_url_label': 'Perus-URL:',
            'base_url_placeholder': 'Oletus: {default_api_base_url}',
            'shortcut': 'Pikakuvakeavain',
            'shortcut_open_dialog': 'Avaa valintaikkuna',
            'shortcut_enter': 'Ctrl + Enter',
            'shortcut_return': 'Command + Return',
            'using_model': 'Malli',
            'action': 'Toiminto',
            'reset_button': 'Palauta oletusarvoihin',
            'reset_current_ai': 'Palauta nykyinen tekoäly oletusarvoihin',
            'reset_ai_confirm_title': 'Vahvista palautus',
            'reset_ai_confirm_message': 'Olet palauttamassa {ai_name} oletustilaan.\n\nTämä tyhjentää:\n• API-avaimen\n• Mukautetun mallin nimen\n• Muut konfiguroidut parametrit\n\nJatkaa?',
            'reset_tooltip': 'Palauta nykyinen tekoäly oletusarvoihin',
            'unsaved_changes_title': 'Tallentamattomia muutoksia',
            'unsaved_changes_message': 'Sinulla on tallentamattomia muutoksia. Mitä haluat tehdä?',
            'save_and_close': 'Tallenna ja sulje',
            'discard_changes': 'Hylkää muutokset',
            'cancel': 'Peruuta',
            'yes_button': 'Kyllä',
            'no_button': 'Ei',
            'cancel_button': 'Peruuta',
            'invalid_default_ai_title': 'Virheellinen oletustekoäly',
            'invalid_default_ai_message': 'Oletustekoäly "{default_ai}" ei ole oikein määritetty.\n\nHaluatko vaihtaa "{first_ai}"-kohteeseen sen sijaan?',
            'switch_to_ai': 'Vaihda {ai}',
            'keep_current': 'Pidä nykyinen',
            'prompt_template': 'Kehotemalli',
            'ask_prompts': 'Kysy kehotteita',
            'random_questions_prompts': 'Satunnaisten kysymysten kehotteet',
            'display': 'Näytä',
            'export_settings': 'Vientiasetukset',
            'enable_default_export_folder': 'Vie oletuskansioon',
            'no_folder_selected': 'Kansiota ei valittu',
            'browse': 'Selaa...',
            'select_export_folder': 'Valitse vientikansio',
            
            # Button text and menu items
            'copy_response_btn': 'Kopioi vastaus',
            'copy_qa_btn': 'Kopioi K&V',
            'export_current_btn': 'Vie K&V PDF-muodossa',
            'export_history_btn': 'Vie historia PDF-muodossa',
            'copy_mode_response': 'Vastaus',
            'copy_mode_qa': 'K&V',
            'copy_format_plain': 'Pelkkä teksti',
            'copy_format_markdown': 'Markdown',
            'export_mode_current': 'Nykyinen K&V',
            'export_mode_history': 'Historia',
            
            # PDF Export related
            'model_provider': 'Palveluntarjoaja',
            'model_name': 'Malli',
            'model_api_url': 'API:n perus-URL',
            'pdf_model_info': 'Tekoälymallin tiedot',
            'pdf_software': 'Ohjelmisto',
            
            # UI - Dialog elements
            'input_placeholder': 'Kirjoita kysymyksesi...',
            'response_placeholder': 'Vastaus pian...',  # Used for all models
            
            # UI - Menu items
            'menu_title': 'Kysy tekoälyltä',
            'menu_ask': 'Kysy',
            
            # UI - Status information
            'loading': 'Ladataan',
            'loading_text': 'Kysytään',
            'loading_models_text': 'Ladataan malleja',
            'save_success': 'Asetukset tallennettu',
            'sending': 'Lähetetään...',
            'requesting': 'Pyydetään',
            'formatting': 'Pyyntö onnistui, muotoillaan',
            
            # UI - Model list feature
            'load_models': 'Lataa malleja',
            'load_models_list': 'Lataa mallilista',
            'test_current_model': 'Testaa nykyistä mallia',
            'use_custom_model': 'Käytä mukautettua mallinimeä',
            'custom_model_placeholder': 'Anna mukautettu mallinimi',
            'model_placeholder': 'Lataa mallit ensin',
            'models_loaded': 'Ladattiin {count} mallia onnistuneesti',
            'models_loaded_with_selection': 'Ladattiin {count} mallia onnistuneesti.\nValittu malli: {model}',
            'load_models_failed': 'Mallien lataaminen epäonnistui: {error}',
            'model_list_not_supported': 'Tämä palveluntarjoaja ei tue automaattista mallilistojen hakua',
            'api_key_required': 'Syötä API-avain ensin',
            'invalid_params': 'Virheelliset parametrit',
            'warning': 'Varoitus',
            'success': 'Onnistui',
            'error': 'Virhe',
            'error_opening_dialog': 'Virhe dialogin avaamisessa:',
            'skipped_books_warning': '{count} kirja(a) ohitettiin tiedostojen käyttövirheiden vuoksi.\nTämä voi johtua virheellisistä merkeistä tiedostopoluissa tai toisen ohjelman lukitsemista tiedostoista.',
            'failed_to_read_all_books': 'Kaikkien valittujen kirjojen metatietoja ei voitu lukea.\nTämä voi johtua virheellisistä merkeistä tiedostopoluissa tai toisen ohjelman lukitsemista tiedostoista.',
            'error_starting_request': 'Virhe pyynnön käynnistämisessä',
            'default_ai_mismatch_title': 'Oletus-AI muutettu',
            'default_ai_mismatch_message': 'Asetuksissa oletus-AI on muutettu arvoon "{default_ai}",\nmutta nykyinen keskustelu käyttää "{current_ai}".\n\nHaluatko vaihtaa uuteen oletus-AI:hin?',
            
            # Metadata fields
            'metadata_title': 'Otsikko',
            'metadata_authors': 'Tekijä',
            'metadata_publisher': 'Kustantaja',
            'metadata_pubdate': 'Julkaisupäivä',
            'metadata_pubyear': 'Julkaisuvuosi',
            'metadata_language': 'Kieli',
            'metadata_series': 'Sarja',
            'no_metadata': 'Ei metatietoja',
            'no_series': 'Ei sarjaa',
            'unknown': 'Tuntematon',
            
            # Multi-book feature
            'books_unit': ' kirjaa',
            'new_conversation': 'Uusi keskustelu',
            'single_book': 'Yksi kirja',
            'multi_book': 'Useita kirjoja',
            'deleted': 'Poistettu',
            'history': 'Historia',
            'no_history': 'Ei historiatietueita',
            'empty_question_placeholder': '(Ei kysymystä)',
            'history_ai_unavailable': 'Tämä tekoäly on poistettu asetuksista',
            'clear_current_book_history': 'Tyhjennä nykyisen kirjan historia',
            'confirm_clear_book_history': 'Oletko varma, että haluat tyhjentää kaiken historian:\n{book_titles}?',
            'confirm': 'Vahvista',
            'history_cleared': '{deleted_count} historiatietuetta tyhjennetty.',
            'multi_book_template_label': 'Usean kirjan kehotemalli:',
            'multi_book_placeholder_hint': 'Käytä {books_metadata} kirjan tiedoille, {query} käyttäjän kysymykselle',
            
            # Error messages (Note: 'error' is already defined above, these are other error types)
            'network_error': 'Verkkovirhe',
            'request_timeout': 'Pyynnön aikakatkaisu',
            'request_failed': 'Pyyntö epäonnistui',
            'request_stopped': 'Pyyntö pysäytetty',
            'question_too_long': 'Kysymys liian pitkä',
            'question_too_long_detail': (
                'Kehote on liian pitkä ({current} merkkiä, raja {limit}, yli {over}). '
                'Olet valinnut {book_count} kirjaa.'
            ),
            'question_too_long_detail_library': (
                'Kehote on liian pitkä ({current} merkkiä, raja {limit}, yli {over}). '
                'Kirjastoindeksissäsi on {book_count} kirjaa.'
            ),
            'question_too_long_hint_ai_search': (
                'Kirjastonlaajuisiin hakuun käytä AI Search -toimintoa (kysy valitsematta kirjoja '
                'tai käytä AI Search -valikkoa) sen sijaan, että valitsisit monta kirjaa.'
            ),
            'question_too_long_hint_library_search': (
                'Kirjastoindeksisi ylittää nykyisen kehotteen rajan. Ota käyttöön mukautettu kehotteen '
                'pituusraja kohdassa Lisäosan asetukset → General (suositus: 524288 merkkiä), '
                'tai esitä tarkempi kysymys.'
            ),
            'question_too_long_reduce_books': (
                'Vertaillaksesi pienempää joukkoa syvällisesti, kokeile poistaa valinta noin {count} kirjasta.'
            ),
            'question_too_long_hint_default': (
                'Nykyinen oletusraja: {limit} merkkiä ({mode}). '
                'Yhden kirjan oletus on 128 000; usean kirjan oletus on 256 000. '
                'Edistyneet käyttäjät voivat ottaa mukautetun rajan käyttöön kohdassa Lisäosan asetukset → General.'
            ),
            'question_too_long_hint_custom': (
                'Olet ottanut mukautetun kehotteen rajan käyttöön. Jos pyynnöt aikakatkaistaan, '
                'laske rajaa kohdassa Lisäosan asetukset → General tai vähennä valittuja kirjoja / '
                'käytä tarkempaa kyselyä.'
            ),
            'large_selection_dialog_title': 'Monta kirjaa valittu',
            'large_selection_dialog_message': (
                'Olet valinnut {count} kirjaa. Kirjastonlaajuisiin kysymyksiin AI Search sopii paremmin '
                'ja hakee koko kirjastostasi tiiviillä metatiedoilla.\n\n'
                'Vaihdetaanko AI Searchiin vai jatketaanko valituilla kirjoilla tiiviissä muodossa?'
            ),
            'large_selection_use_ai_search': 'Käytä AI Search',
            'large_selection_continue': 'Jatka valinnalla',
            'multi_book_truncation_note': (
                'Huom: Vain ensimmäiset {included}/{total} valittua kirjaa sisältyvät kehotteen rajan vuoksi. '
                'Käytä AI Search -hakua koko kirjastoon tai nosta mukautettua rajaa kohdassa '
                'Lisäosan asetukset → General.'
            ),
            'library_metadata_truncation_note': (
                'Huom: Vain ensimmäiset {included}/{total} indeksoitua kirjaa sisältyvät kehotteen rajan vuoksi. '
                'Tulokset voivat olla puutteellisia hyvin suurissa kirjastoissa, ellei mukautettua rajaa '
                'nosteta kohdassa Lisäosan asetukset → General.'
            ),
            'auth_token_required_title': 'Tekoälypalvelu vaaditaan',
            'auth_token_required_message': 'Määritä kelvollinen tekoälypalvelu lisäosan asetuksissa.',
            'open_configuration': 'Avaa asetukset',
            'error_preparing_request': 'Pyynnön valmistelu epäonnistui',
            'empty_suggestion': 'Tyhjä ehdotus',
            'process_suggestion_error': 'Ehdotuksen käsittelyvirhe',
            'unknown_error': 'Tuntematon virhe',
            'unknown_model': 'Tuntematon malli: {model_name}',
            'suggestion_error': 'Ehdotusvirhe',
            'random_question_success': 'Satunnainen kysymys luotu onnistuneesti!',
            'book_title_check': 'Kirjan nimi vaaditaan',
            'avoid_repeat_question': 'Käytä eri kysymystä',
            'empty_answer': 'Tyhjä vastaus',
            'invalid_json': 'Virheellinen JSON',
            'invalid_response': 'Virheellinen vastaus',
            'auth_error_401': 'Luvaton',
            'auth_error_403': 'Pääsy kielletty',
            'rate_limit': 'Liian monta pyyntöä',
            'empty_response': 'Vastaukseton vastaus API:lta',
            'empty_response_after_filter': 'Vastaus on tyhjä suodatuksen jälkeen',
            'no_response': 'Ei vastausta',
            'template_error': 'Mallivirhe',
            'no_model_configured': 'Tekoälymallia ei ole määritetty. Määritä tekoälymalli asetuksista.',
            'no_ai_configured_title': 'Tekoälyä ei määritetty',
            'no_ai_configured_message': 'Tervetuloa! Aloittaaksesi kirjojesi kysymysten esittämisen, sinun on ensin määritettävä tekoälypalveluntarjoaja.\n\nHyviä uutisia: Tässä lisäosassa on nyt ILMAINEN taso (Nvidia AI Free), jota voit käyttää heti ilman määrityksiä!\n\nMuita suositeltuja vaihtoehtoja:\n• Nvidia AI - Hanki 6 kuukauden ILMAINEN API-käyttöoikeus pelkällä puhelinnumerollasi (luottokorttia ei vaadita)\n• Ollama - Suorita tekoälymalleja paikallisesti tietokoneellasi (täysin ilmainen ja yksityinen)\n\nHaluatko avata lisäosan asetukset tekoälypalveluntarjoajan määrittämiseksi nyt?',
            'open_settings': 'Lisäosan asetukset',
            'ask_anyway': 'Kysy silti',
            'later': 'Myöhemmin',
            'reset_all_data': 'Nollaa kaikki tiedot',
            'reset_all_data_warning': 'Tämä poistaa kaikki API-avaimet, kehotemallit ja paikalliset historiatietueet. Kieliasetuksesi säilytetään. Ole varovainen.',
            'reset_all_data_confirm_title': 'Vahvista nollaus',
            'reset_all_data_confirm_message': 'Oletko varma, että haluat nollata lisäosan alkuperäiseen tilaan?\n\nTämä poistaa pysyvästi:\n• Kaikki API-avaimet\n• Kaikki mukautetut kehotemallit\n• Koko keskusteluhistorian\n• Kaikki lisäosan asetukset (kieliasetukset säilytetään)\n\nTätä toimintoa ei voi kumota!',
            'reset_all_data_success': 'Kaikki lisäosan tiedot on nollattu onnistuneesti. Käynnistä calibre uudelleen, jotta muutokset tulevat voimaan.',
            'reset_all_data_failed': 'Lisäosan tietojen nollaus epäonnistui: {error}',
            'random_question_error': 'Virhe satunnaisen kysymyksen luomisessa',
            'clear_history_failed': 'Historian tyhjennys epäonnistui',
            'clear_history_not_supported': 'Yhden kirjan historian tyhjennystä ei tueta vielä',
            'missing_required_config': 'Puuttuva pakollinen asetus: {key}. Tarkista asetuksesi.',
            'api_key_too_short': 'API-avain on liian lyhyt. Tarkista ja syötä koko avain.',
            
            # API response handling
            'api_request_failed': 'API-pyyntö epäonnistui: {error}',
            'api_content_extraction_failed': 'Sisällön erottaminen API-vastauksesta epäonnistui',
            'api_invalid_response': 'Kelvollista API-vastausta ei saatu',
            'api_unknown_error': 'Tuntematon virhe: {error}',
            
            # Stream response handling
            'stream_response_code': 'Striimivastauksen tilakoodi: {code}',
            'stream_continue_prompt': 'Jatka edellistä vastaustasi toistamatta jo annettua sisältöä.',
            'stream_continue_code_blocks': 'Edellisessä vastauksessasi oli sulkemattomia koodilohkoja. Jatka ja täydennä nämä koodilohkot.',
            'stream_continue_parentheses': 'Edellisessä vastauksessasi oli sulkemattomia sulkeita. Jatka ja varmista, että kaikki sulkeet ovat oikein suljettuina.',
            'stream_continue_interrupted': 'Edellinen vastauksesi näyttää keskeytyneen. Jatka viimeisen ajatuksesi tai selityksesi täydentämistä.',
            'stream_timeout_error': 'Striimiyhteys ei ole vastaanottanut uutta sisältöä 60 sekuntiin, mahdollisesti yhteysongelma.',
            
            # API error messages
            'api_version_model_error': 'API-versio tai mallinimi virhe: {message}\n\nPäivitä API:n perus-URL "{base_url}"-kohteeksi ja malli "{model}"-kohteeksi tai muuksi saatavilla olevaksi malliksi asetuksissa.',
            'api_format_error': 'API-pyynnön muotovirhe: {message}',
            'api_key_invalid': 'API-avain virheellinen tai luvaton: {message}\n\nTarkista API-avaimesi ja varmista, että API-käyttöoikeus on käytössä.',
            'api_rate_limit': 'Pyynnön nopeusrajoitus ylittynyt, yritä uudelleen myöhemmin\n\nOlet ehkä ylittänyt ilmaisen käyttökiintiön. Tämä voi johtua:\n1. Liian monesta pyynnöstä minuutissa\n2. Liian monesta pyynnöstä päivässä\n3. Liian monesta syöttötokenista minuutissa',
            
            # Configuration errors
            'missing_config_key': 'Puuttuva pakollinen konfiguraatioavain: {key}',
            'api_base_url_required': 'API:n perus-URL vaaditaan',
            'model_name_required': 'Mallinimi vaaditaan',
            
            # Model list fetching
            'fetching_models_from': 'Haetaan malleja osoitteesta {url}',
            'successfully_fetched_models': 'Haettu {count} {provider} mallia onnistuneesti',
            'failed_to_fetch_models': 'Mallien lataaminen epäonnistui: {error}',
            'api_key_empty': 'API-avain on tyhjä. Syötä kelvollinen API-avain.',
            
            # Error messages for model fetching
            'error_401': 'API-avaimen todennus epäonnistui. Tarkista: API-avain on oikea, tilillä on riittävästi saldoa, API-avain ei ole vanhentunut.',
            'error_403': 'Pääsy kielletty. Tarkista: API-avaimella on riittävät oikeudet, ei alueellisia pääsyrajoituksia.',
            'error_404': 'API-päätepistettä ei löydy. Tarkista, onko API:n perus-URL-määritys oikein.',
            'error_429': 'Liian monta pyyntöä, nopeusrajoitus saavutettu. Yritä uudelleen myöhemmin.',
            'error_5xx': 'Palvelinvirhe. Yritä uudelleen myöhemmin tai tarkista palveluntarjoajan tila.',
            'error_network': 'Verkkoyhteys epäonnistui. Tarkista verkkoyhteys, välityspalvelinasetukset tai palomuurikonfiguraatio.',
            'error_unknown': 'Tuntematon virhe.',
            'technical_details': 'Tekniset yksityiskohdat',
            'ollama_service_not_running': 'Ollama-palvelu ei ole käynnissä. Käynnistä Ollama-palvelu ensin.',
            'ollama_service_timeout': 'Ollama-palveluyhteyden aikakatkaisu. Tarkista, onko palvelu käynnissä oikein.',
            'ollama_model_not_available': 'Malli "{model}" ei ole saatavilla. Tarkista:\n1. Onko malli käynnissä? Suorita: ollama run {model}\n2. Onko mallin nimi oikein?\n3. Onko malli ladattu? Suorita: ollama pull {model}',
            'gemini_geo_restriction': 'Gemini API ei ole saatavilla alueellasi. Kokeile:\n1. Käytä VPN:ää yhdistääksesi tuetusta alueesta\n2. Käytä muita tekoälypalveluntarjoajia (OpenAI, Anthropic, DeepSeek jne.)\n3. Tarkista Google AI Studio alueellisen saatavuuden osalta',
            'model_test_success': 'Mallin testaus onnistui!',
            'test_model_prompt': 'Mallit ladattu onnistuneesti! Haluatko testata valitun mallin "{model}"?',
            'test_model_button': 'Testaa mallia',
            'skip': 'Ohita',
            
            # About information
            'author_name': 'Sheldon',
            'user_manual': 'Käyttöopas',
            'about_plugin': 'Tietoja Ask AI -lisäosasta',
            'learn_how_to_use': 'Miten käyttää',
            'email': 'iMessage',
            'about_title': 'Tietoja Ask AI -lisäosasta',
            'about_version_label': 'Versio',
            'about_description': 'Kysy calibre-kirjoista valitsemillasi tekoälypalveluilla.',
            'about_related_plugins': 'Aiheeseen liittyvät lisäosat',
            'about_markdown_title': 'Markdown calibre-ohjelmalle',
            'about_markdown_desc': 'Vie kirjat Markdown-tekstitiedostoiksi.',
            'about_tradsimp_title': 'Kiinankielisen tekstin muunnos calibre-ohjelmalle',
            'about_tradsimp_desc': 'Muunna perinteistä ja yksinkertaistettua kiinaa e-kirjoissa.',
            'about_open_mobileread': 'Avaa MobileRead',
            'about_open_nowtiny': 'Avaa Nowtiny',
            'about_nowtiny_note': 'Lisää työkaluja ja lisäosien tila löytyy Nowtiny-sivustolta.',
            
            # Model specific configurations
            'model_display_name_grok': 'Grok(x.AI)',
            'model_display_name_gemini': 'Gemini(Google)',
            'model_display_name_deepseek': 'Deepseek',
            'model_display_name_custom': 'Mukautettu',
            'model_display_name_ollama': 'Ollama(Local)',
            'model_display_name_lmstudio': 'LM Studio(Local)',
            'model_display_name_koboldcpp': 'KoboldCpp(Local)',
            'local_openai_compat_no_api_key_notice': 'Note: This local OpenAI-compatible service usually does not require an API key. Start the local server, then refresh the model list.',
            'lmstudio_no_api_key_notice': 'Note: LM Studio uses the OpenAI-compatible API locally and usually does not require an API key.',
            'koboldcpp_no_api_key_notice': 'Note: KoboldCpp uses the OpenAI-compatible API locally and usually does not require an API key.',
            'local_service_not_running': 'Cannot connect to the local AI service. Please confirm it is running and the Base URL is correct.',
            'model_enable_streaming': 'Ota suoratoisto käyttöön',
            
            # AI Switcher
            'current_ai': 'Nykyinen tekoäly',
            'no_configured_models': 'Tekoälyä ei määritetty - Määritä asetuksissa',
            
            # Provider specific info
            'nvidia_free_info': '💡 Uudet käyttäjät saavat 6 kuukauden ilmaisen API-käytön - Luottokorttia ei vaadita',
            
            # Common system messages
            'default_system_message': 'Olet kirja-analyysin asiantuntija. Tehtäväsi on auttaa käyttäjiä ymmärtämään kirjoja paremmin tarjoamalla oivaltavia kysymyksiä ja analyysejä.',
            
            # Request timeout settings
            'request_timeout_label': 'Pyynnön aikakatkaisu:',
            'seconds': 'sekuntia',
            'request_timeout_error': 'Pyynnön aikakatkaisu. Nykyinen aikakatkaisu: {timeout} sekuntia',
            'enable_custom_prompt_limit_label': 'Mukautettu kehotteen pituusraja',
            'enable_custom_prompt_limit_tooltip': (
                'Oletusrajat ovat 128 000 merkkiä (yksi kirja) ja 256 000 (useita kirjoja). '
                'Useimmat käyttäjät eivät tarvitse muutosta. Kirjastonlaajuisiin hakuun käytä AI Search -toimintoa. '
                'Ota mukautettu raja käyttöön vain, jos mallisi tukee paljon suurempaa kontekstia ja '
                'pyynnöt yhä osuvat rajaan.'
            ),
            'max_prompt_length_label': 'Kehotteen enimmäispituus:',
            'max_prompt_length_unit': 'merkkiä',
            'max_prompt_length_tooltip': (
                'Voimassa, kun mukautettu raja on käytössä. Oletussuositus: 524288 merkkiä. '
                'Karkea ohje: 1 token ≈ 3–4 merkkiä. Ollamalla aseta myös num_ctx mallipuolella.'
            ),
            'max_prompt_length_normalized_title': 'Kehotteen raja säädetty',
            'max_prompt_length_normalized': (
                'Kehotteen pituus normalisoitiin arvoon {value} merkkiä (erottimet kuten pilkut '
                'tai välilyönnit poistettiin).'
            ),
            
            # Parallel AI settings
            'parallel_ai_count_label': 'Rinnakkaisten tekoälyjen määrä:',
            'parallel_ai_count_tooltip': 'Samanaikaisesti kysyttävien tekoälymallien määrä (1-2 saatavilla, 3-4 tulossa pian)',
            'parallel_ai_notice': 'Huomautus: Tämä vaikuttaa vain kysymysten lähettämiseen. Satunnaiset kysymykset käyttävät aina yhtä tekoälyä.',
            'suggest_maximize': 'Vinkki: Maksimoi ikkuna, jotta näet paremmin 3 tekoälyllä',
            'ai_panel_label': 'Tekoäly {index}:',
            'no_ai_available': 'Tälle paneelille ei ole käytettävissä tekoälyä',
            'add_more_ai_providers': 'Lisää tekoälypalveluntarjoajia asetuksiin',
            'select_ai': '-- Valitse tekoäly --',
            'select_model': '-- Valitse malli --',
            'request_model_list': 'Pyydä mallilista',
            'coming_soon': 'Tulossa pian',
            'advanced_feature_tooltip': 'Tämä ominaisuus on kehitteillä. Pysy kuulolla päivityksistä!',
            
            # AI Manager Dialog
            'ai_manager_title': 'Hallitse tekoälypalveluntarjoajia',
            'add_ai_title': 'Lisää tekoälypalveluntarjoaja',
            'manage_ai_title': 'Hallitse määritettyä tekoälyä',
            'configured_ai_list': 'Määritetyt tekoälyt',
            'available_ai_list': 'Lisättävissä olevat',
            'ai_config_panel': 'Asetukset',
            'select_ai_to_configure': 'Valitse tekoäly luettelosta määritettäväksi',
            'select_provider': 'Valitse tekoälypalveluntarjoaja',
            'select_provider_hint': 'Valitse palveluntarjoaja luettelosta',
            'select_ai_to_edit': 'Valitse tekoäly luettelosta muokattavaksi',
            'set_as_default': 'Aseta oletukseksi',
            'save_ai_config': 'Tallenna',
            'remove_ai_config': 'Poista',
            'delete_ai': 'Poista',
            'add_ai_button': 'Lisää tekoäly',
            'ai_manager_window_hint': '“Lisää / Hallitse” avaa kokoa muutettavan ikkunan (voi maximoida). Kaksoisnapsauta määritettyä tekoälyä muokataksesi.',
            'edit_ai_button': 'Muokkaa tekoälyä',
            'manage_configured_ai_button': 'Hallitse määritettyä tekoälyä',
            'manage_ai_button': 'Hallitse tekoälyä',
            'no_configured_ai': 'Tekoälyä ei ole vielä määritetty',
            'no_configured_ai_hint': 'Tekoälyä ei ole määritetty. Lisäosa ei voi toimia. Napsauta "Lisää tekoäly" lisätäksesi tekoälypalveluntarjoajan.',
            'default_ai_label': 'Oletustekoäly:',
            'default_ai_tag': 'Oletus',
            'ai_not_configured_cannot_set_default': 'Tätä tekoälyä ei ole vielä määritetty. Tallenna asetukset ensin.',
            'ai_set_as_default_success': '{name} on asetettu oletustekoälyksi.',
            'ai_config_saved_success': '{name} asetukset tallennettu onnistuneesti.',
            'confirm_remove_title': 'Vahvista poisto',
            'confirm_remove_ai': 'Oletko varma, että haluat poistaa {name}? Tämä tyhjentää API-avaimen ja palauttaa asetukset.',
            'confirm_delete_title': 'Vahvista poisto',
            'confirm_delete_ai': 'Oletko varma, että haluat poistaa {name}?',
            'api_key_required': 'API-avain vaaditaan.',
            'configuration': 'Asetukset',
            
            # Field descriptions
            'api_key_desc': 'API-avaimesi todennusta varten. Pidä se turvassa äläkä jaa sitä.',
            'base_url_desc': 'API-päätepisteen URL. Käytä oletusta, ellei sinulla ole mukautettua päätepistettä.',
            'model_desc': 'Valitse malli luettelosta tai käytä mukautettua mallinimeä.',
            'streaming_desc': 'Ota reaaliaikainen vastausten suoratoisto käyttöön nopeamman palautteen saamiseksi.',
            'advanced_section': 'Lisäasetukset',
            
            # Provider-specific notices
            'perplexity_model_notice': 'Huomautus: Perplexity ei tarjoa julkista mallilista-API:a, joten mallit ovat kovakoodattuja.',
            'ollama_no_api_key_notice': 'Note: Ollama uses the OpenAI-compatible API locally and usually does not require an API key.',
            'nvidia_free_credits_notice': 'Huomautus: Uudet käyttäjät saavat ilmaisia API-krediittejä - Luottokorttia ei vaadita.',
            
            # Nvidia Free error messages
            'free_tier_rate_limit': 'Ilmaisen tason nopeusrajoitus ylitetty. Yritä uudelleen myöhemmin tai määritä oma Nvidia API-avaimesi.',
            'free_tier_unavailable': 'Ilmainen taso on tilapäisesti poissa käytöstä. Yritä uudelleen myöhemmin tai määritä oma Nvidia API-avaimesi.',
            'free_tier_server_error': 'Ilmaisen tason palvelinvirhe. Yritä uudelleen myöhemmin.',
            'free_tier_error': 'Ilmaisen tason virhe',
            
            # Nvidia Free provider info
            'free': 'Ilmainen',
            'nvidia_free_provider_name': 'Nvidia AI (Ilmainen)',
            'nvidia_free_display_name': 'Nvidia AI (Ilmainen)',
            'nvidia_free_api_key_info': 'Haetaan palvelimelta',
            'nvidia_free_desc': 'Tämän palvelun ylläpitäjä on kehittäjä, ja se pidetään ilmaisena, mutta se saattaa olla vähemmän vakaa. Vakaamman palvelun saamiseksi määritä oma Nvidia API-avaimesi.',
            
            # Nvidia Free first use reminder
            'nvidia_free_first_use_title': 'Tervetuloa Ask AI -lisäosaan',
            'nvidia_free_first_use_message': 'Nyt voit vain kysyä ilman mitään asetuksia! Kehittäjä ylläpitää sinulle ilmaista tasoa, mutta se ei välttämättä ole kovin vakaa. Nauti!\n\nVoit määrittää omat tekoälypalveluntarjoajasi asetuksista paremman vakauden saavuttamiseksi.',
            
            # Model buttons
            'refresh_model_list': 'Päivitä',
            'test_current_model': 'Testaa',
            'testing_text': 'Testataan',
            'refresh_success': 'Mallilista päivitetty onnistuneesti.',
            'refresh_failed': 'Mallilistan päivitys epäonnistui.',
            'test_failed': 'Mallin testaus epäonnistui.',
            
            # Tooltip
            'manage_ai_disabled_tooltip': 'Lisää tekoälypalveluntarjoaja ensin.',
            
            # PDF export section titles
            'pdf_book_metadata': 'KIRJAN METATIEDOT',
            'pdf_question': 'KYSYMYS',
            'pdf_answer': 'VASTAUS',
            'pdf_ai_model_info': 'TEKOÄLYMALLIN TIEDOT',
            'pdf_generated_by': 'GENEROITU',
            'pdf_provider': 'Palveluntarjoaja',
            'pdf_model': 'Malli',
            'pdf_api_base_url': 'API:n perus-URL',
            'pdf_panel': 'Paneeli',
            'pdf_plugin': 'Lisäosa',
            'pdf_github': 'GitHub',
            'pdf_software': 'Ohjelmisto',
            'pdf_generated_time': 'Luotu aika',
            'pdf_info_not_available': 'Tietoa ei saatavilla',

            #AI Search v1.4.2
            'library_tab': 'Haku',
            'library_search': 'AI-haku',
            'library_info': 'AI-haku on aina käytössä. Kun et valitse kirjoja, voit hakea koko kirjastostasi luonnollisella kielellä.',
            'library_enable': 'Ota AI-haku käyttöön',
            'library_enable_tooltip': 'Kun käytössä, voit hakea kirjastostasi tekoälyllä, kun kirjoja ei ole valittuna',
            'library_update': 'Päivitä kirjaston tiedot',
            'library_update_tooltip': 'Hae kirjojen nimet ja kirjailijat kirjastostasi',
            'library_updating': 'Päivitetään...',
            'library_status': 'Tila: {count} kirjaa, viimeisin päivitys: {time}',
            'library_status_empty': 'Tila: Ei tietoja. Aloita klikkaamalla "Päivitä kirjaston tiedot".',
            'library_status_error': 'Tila: Virhe ladattaessa tietoja',
            'library_update_success': 'Päivitetty onnistuneesti {count} kirjaa',
            'library_update_failed': 'Kirjaston tietojen päivitys epäonnistui',
            'library_no_gui': 'GUI ei käytettävissä',
            'library_init_title': 'Alusta AI-haku',
            'library_init_message': 'AI-haku vaatii kirjaston metatiedot toimiakseen. Haluatko alustaa ne nyt?\n\nTämä hakee kirjojen nimet ja kirjailijat kirjastostasi.',
            'library_init_required': 'AI-hakua ei voi ottaa käyttöön ilman kirjaston tietoja. Klikkaa "Päivitä kirjaston tiedot", kun olet valmis käyttämään tätä ominaisuutta.',
            'ai_search_welcome_title': 'Tervetuloa AI-hakuun',
            'ai_search_welcome_message': 'AI-haku on aktivoitu!\n\nAktivointitavat:\n• Pikanäppäin (muokattavissa asetuksissa)\n• Työkalut-valikko → AI-haku\n• Avaa Ask-dialogi valitsematta kirjoja\n\nVoit hakea koko kirjastostasi luonnollisella kielellä. Esimerkiksi:\n• "Onko sinulla kirjoja Pythonista?"\n• "Näytä Isaac Asimovin kirjoja"\n• "Etsi kirjoja koneoppimisesta"\n\nAI etsii kirjastostasi ja suosittelee sopivia kirjoja. Napsauta kirjan nimeä avataksesi sen suoraan.',
            'ai_search_not_enough_books_title': 'Ei tarpeeksi kirjoja',
            'ai_search_not_enough_books_message': 'AI-haku vaatii vähintään {min_books} kirjaa kirjastossasi.\n\nNykyisessä kirjastossasi on vain {book_count} kirja(a).\n\nLisää kirjoja käyttääksesi AI-hakua.',
            'ai_search_mode_info': 'Haetaan koko kirjastosta',
            'ai_search_feature_title': 'AI Search',
            'ai_search_feature_subtitle': 'Hae koko kirjastostasi luonnollisella kielellä',
            'ai_search_feature_description': (
                'AI Search auttaa löytämään kirjoja koko Calibre-kirjastostasi.\n\n'
                '• Käynnistys: avaa Ask valitsematta kirjoja, käytä Työkalut → AI Search tai pikanäppäin\n'
                '• Toiminta: lisäosa lähettää tiiviit metatiedot (kirja-ID, otsikko, tekijä) '
                'kaikista indeksoiduista kirjoista\n'
                '• Suuret valinnat: yli 50 kirjan valinta ehdottaa AI Search -toimintoa sen sijaan, '
                'että jokainen kirja upotettaisiin yksityiskohtaisessa muodossa\n'
                '• Pidä tiedot ajan tasalla: napsauta "Päivitä kirjastotiedot" lisättyäsi tai poistettuasi kirjoja\n\n'
                'Esimerkkejä: "Etsi kirjoja Pythonista", "Näytä Isaac Asimovin kirjoja".'
            ),
            'ai_search_usage_hint': (
                'Vinkki: AI Search sopii parhaiten koko kirjaston löytämiseen. Vertaillaksesi '
                'muutamaa kirjaa syvällisesti, valitse enintään 30 kirjaa.'
            ),
            'ai_search_data_title': 'Kirjastoindeksi',
            'ai_search_data_subtitle': 'Päivitä tekoälylle lähetettävä tiivis kirjalista, kun lisäät tai poistat kirjoja',
            'library_prompt_template': 'Sinulla on pääsy käyttäjän kirjakirjastoon. Tässä ovat kaikki kirjat: {metadata} Käyttäjän kysely: {query} Etsi vastaavat kirjat nykyisestä kirjastosta ja palauta ne tässä muodossa (**TÄRKEÄÄ**: Käytä HTML-linkkimuotoa, jotta käyttäjät voivat napsauttaa kirjojen nimiä avatakseen ne suoraan): - <a href="calibre://book/BOOK_ID">Kirjan nimi</a> - Kirjailijan nimi Esimerkki: - <a href="calibre://book/123">Opi Python</a> - Mark Lutz - <a href="calibre://book/456">Koneoppiminen käytännössä</a> - Peter Harrington Huomautus: Jotkut kirjailijat voivat olla merkitty "unknown". Tämä on normaalia dataa, palauta kaikki vastaavat tulokset normaalisti. Palauta vain kyselyä vastaavat kirjat. Enintään 5 tulosta.',
            'ai_search_privacy_title': 'Tietosuojailmoitus',
            'ai_search_privacy_alert': 'AI-haku käyttää kirjastosi metatietoja (nimet ja kirjailijat). Nämä tiedot lähetetään määrittämällesi tekoälypalvelun tarjoajalle hakukyselyidesi käsittelemiseksi.',
            'ai_search_updated_info': 'Päivitetty {count} kirjaa {time_ago}',
            'ai_search_books_info': '{count} kirjaa indeksoitu',
            'days_ago': '{n} päivää sitten',
            'hours_ago': '{n} tuntia sitten',
            'minutes_ago': '{n} minuuttia sitten',
            'just_now': 'juuri nyt',
            
            # Statistics tab (v1.4.2)
            'stat_tab': 'Tilastot',
            'stat_overview': 'Yleiskatsaus',
            'stat_overview_subtitle': 'AI-kyselyiden tilastot',
            'stat_days_unit': 'päivää',
            'stat_days_label': 'Aloitettu',
            'stat_start_at': 'Aloitus {date}',
            'stat_replies_unit': 'kertaa',
            'stat_replies_label': 'Kysy AI',
            'stat_books_unit': 'kirjaa',
            'stat_books_label': 'Kirjasto',
            'stat_no_books': 'Päivitä Haku-välilehdellä',
            'stat_trends': 'Trendit',
            'stat_curious_index': 'AI-kyselyiden jakauma tällä viikolla',
            'stat_daily_avg': 'Päivittäinen keskiarvo {n} kertaa',
            'stat_sample_data': 'Esimerkkidata näytetään. Vaihtuu oikeaan dataan 20+ pyynnön jälkeen',
            'stat_heatmap': 'Lämpökartta',
            'stat_heatmap_subtitle': 'AI-kyselyiden jakauma tässä kuussa',
            'stat_no_data_week': 'Ei dataa tällä viikolla',
            'stat_no_data_month': 'Ei dataa tässä kuussa',
            'stat_data_not_enough': 'Ei tarpeeksi dataa',
            
            # Tilastot käyttäjänimikkeet (perustuu kyselyjen määrään)
            'stat_title_curious': 'Selailija',
            'stat_title_explorer': 'Kirjametsästäjä',
            'stat_title_seeker': 'Innokas lukija',
            'stat_title_enthusiast': 'Bibliofiili',
            'stat_title_pursuer': 'Kirjatoukka',
            
            # Tilastot kirjastoarvioinnit (perustuu kokoelman kokoon, historialliset viittaukset)
            'stat_books_impressive': 'Yksityinen lukuhuone',
            'stat_books_collection': 'Oppineen työhuone',
            'stat_books_variety': 'Helsingin yliopiston kirjasto',
            'stat_books_awesome': 'Kansalliskirjasto',
            'stat_books_unbelievable': 'Aleksandrian kirjasto',
            
            # Links (v1.4.2)
            'online_tutorial': 'Online-opas',
        }