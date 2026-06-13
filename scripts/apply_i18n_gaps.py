#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch i18n language files with missing translation keys."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
I18N = ROOT / "i18n"

# ---------------------------------------------------------------------------
# Insertion order (matches en.py section order within each anchor group)
# ---------------------------------------------------------------------------
INSERT_AFTER = [
    ("question_too_long", [
        "question_too_long_detail",
        "question_too_long_detail_library",
        "question_too_long_hint_ai_search",
        "question_too_long_hint_library_search",
        "question_too_long_reduce_books",
        "question_too_long_hint_default",
        "question_too_long_hint_custom",
        "large_selection_dialog_title",
        "large_selection_dialog_message",
        "large_selection_use_ai_search",
        "large_selection_continue",
        "multi_book_truncation_note",
        "library_metadata_truncation_note",
    ]),
    ("empty_answer", [
        "empty_response",
        "empty_response_after_filter",
    ]),
    ("failed_to_fetch_models", [
        "error_401",
        "error_403",
        "error_404",
    ]),
    ("save_and_close", [
        "discard_changes",
    ]),
    ("metadata_publisher", [
        "metadata_pubdate",
    ]),
    ("request_timeout_error", [
        "enable_custom_prompt_limit_label",
        "enable_custom_prompt_limit_tooltip",
        "max_prompt_length_label",
        "max_prompt_length_unit",
        "max_prompt_length_tooltip",
        "max_prompt_length_normalized_title",
        "max_prompt_length_normalized",
    ]),
    ("advanced_feature_tooltip", [
        "ai_manager_title",
        "add_ai_title",
        "manage_ai_title",
        "configured_ai_list",
        "available_ai_list",
        "ai_config_panel",
        "select_ai_to_configure",
        "select_provider",
        "select_provider_hint",
        "select_ai_to_edit",
        "set_as_default",
        "save_ai_config",
        "remove_ai_config",
        "delete_ai",
        "add_ai_button",
        "edit_ai_button",
        "manage_configured_ai_button",
        "manage_ai_button",
        "no_configured_ai",
        "no_configured_ai_hint",
        "default_ai_label",
        "default_ai_tag",
        "ai_not_configured_cannot_set_default",
        "ai_set_as_default_success",
        "ai_config_saved_success",
        "confirm_remove_title",
        "confirm_remove_ai",
        "confirm_delete_title",
        "confirm_delete_ai",
        "configuration",
    ]),
    ("pdf_answer", [
        "pdf_ai_model_info",
        "pdf_generated_by",
        "pdf_provider",
        "pdf_model",
        "pdf_api_base_url",
        "pdf_panel",
        "pdf_plugin",
        "pdf_github",
        "pdf_generated_time",
    ]),
    ("ai_search_mode_info", [
        "ai_search_feature_title",
        "ai_search_feature_subtitle",
        "ai_search_feature_description",
        "ai_search_usage_hint",
        "ai_search_data_title",
        "ai_search_data_subtitle",
    ]),
]

PLUGIN_NAMES = {
    "zh": "Ask AI 插件",
    "zht": "Ask AI 插件",
    "da": "Ask AI-plugin",
    "de": "Ask AI Plugin",
    "fr": "Plugin Ask AI",
    "ja": "Ask AI プラグイン",
    "nl": "Ask AI-plugin",
}

INVALID_JSON = "Invalid JSON"

INVALID_JSON_I18N = {
    "en": "Invalid JSON",
    "da": "Ugyldig JSON",
    "es": "JSON no válido",
    "fi": "Virheellinen JSON",
    "nl": "Ongeldige JSON",
    "no": "Ugyldig JSON",
    "pt": "JSON inválido",
    "ru": "Неверный JSON",
    "sv": "Ogiltig JSON",
    "yue": "無效 JSON",
    "zh": "无效 JSON",
}

EN_PATCH = {
    "invalid_json": INVALID_JSON,
}


def _q(*parts: str) -> tuple[str, ...]:
    return parts


# Shared 26-key blocks -------------------------------------------------------

def _block_26_da() -> dict:
    return {
        "question_too_long_detail": _q(
            "Prompten er for lang ({current} tegn, grænse {limit}, overskrider med {over}). ",
            "Du har valgt {book_count} bog/bøger.",
        ),
        "question_too_long_detail_library": _q(
            "Prompten er for lang ({current} tegn, grænse {limit}, overskrider med {over}). ",
            "Dit biblioteksindeks indeholder {book_count} bog/bøger.",
        ),
        "question_too_long_hint_ai_search": _q(
            "Til biblioteksomfattende søgninger, brug AI Search (spørg uden at vælge bøger, ",
            "eller brug AI Search-menuen) i stedet for at vælge mange bøger.",
        ),
        "question_too_long_hint_library_search": _q(
            "Dit biblioteksindeks overskrider den aktuelle promptgrænse. Aktivér brugerdefineret ",
            "promptlængdegrænse under Plugin-konfiguration → General (foreslået: 524288 tegn), ",
            "eller stil et mere specifikt spørgsmål.",
        ),
        "question_too_long_reduce_books": _q(
            "For at sammenligne et mindre sæt i dybden, prøv at fravælge ca. {count} bog/bøger.",
        ),
        "question_too_long_hint_default": _q(
            "Nuværende standardgrænse: {limit} tegn ({mode}). ",
            "Standard for enkelt bog er 128.000; for flere bøger 256.000. ",
            "Avancerede brugere kan aktivere en brugerdefineret grænse under Plugin-konfiguration → General.",
        ),
        "question_too_long_hint_custom": _q(
            "Du har aktiveret en brugerdefineret promptgrænse. Hvis anmodninger får timeout, ",
            "sænk grænsen under Plugin-konfiguration → General, eller reducer valgte bøger / ",
            "brug en mere specifik forespørgsel.",
        ),
        "large_selection_dialog_title": "Mange bøger valgt",
        "large_selection_dialog_message": _q(
            "Du har valgt {count} bøger. Til biblioteksomfattende spørgsmål fungerer AI Search bedre ",
            "og søger i hele dit bibliotek med kompakte metadata.\n\n",
            "Skift til AI Search, eller fortsæt med de valgte bøger i kompakt format?",
        ),
        "large_selection_use_ai_search": "Brug AI Search",
        "large_selection_continue": "Fortsæt med valgte",
        "multi_book_truncation_note": _q(
            "Bemærk: Kun de første {included} af {total} valgte bøger er inkluderet på grund af ",
            "promptgrænsen. Brug AI Search til at søge i hele biblioteket, eller hæv den ",
            "brugerdefinerede grænse under Plugin-konfiguration → General.",
        ),
        "library_metadata_truncation_note": _q(
            "Bemærk: Kun de første {included} af {total} indekserede bøger er inkluderet på grund af ",
            "promptgrænsen. Resultater kan være ufuldstændige for meget store biblioteker, medmindre du ",
            "hæver den brugerdefinerede grænse under Plugin-konfiguration → General.",
        ),
        "enable_custom_prompt_limit_label": "Brugerdefineret promptlængdegrænse",
        "enable_custom_prompt_limit_tooltip": _q(
            "Standardgrænser er 128.000 tegn (enkelt bog) og 256.000 (flere bøger). ",
            "De fleste brugere behøver ikke ændre dette. Til biblioteksomfattende søgninger, brug AI Search. ",
            "Aktivér kun en brugerdefineret grænse, hvis din model understøtter en meget større kontekst ",
            "og anmodninger stadig rammer grænsen.",
        ),
        "max_prompt_length_label": "Maks. promptlængde:",
        "max_prompt_length_unit": "tegn",
        "max_prompt_length_tooltip": _q(
            "Gælder når brugerdefineret grænse er aktiveret. Standardforslag: 524288 tegn. ",
            "Groft estimat: 1 token ≈ 3–4 tegn. For Ollama, indstil også num_ctx på modelsiden.",
        ),
        "max_prompt_length_normalized_title": "Promptgrænse justeret",
        "max_prompt_length_normalized": _q(
            "Promptlængden blev normaliseret til {value} tegn (adskillere som kommaer ",
            "eller mellemrum blev fjernet).",
        ),
        "ai_search_feature_title": "AI Search",
        "ai_search_feature_subtitle": "Søg i hele dit bibliotek med naturligt sprog",
        "ai_search_feature_description": _q(
            "AI Search hjælper dig med at finde bøger i hele dit Calibre-bibliotek.\n\n",
            "• Udløs: åbn Ask uden at vælge bøger, brug Værktøjer → AI Search, eller en genvej\n",
            "• Sådan virker det: pluginet sender kompakte metadata (bog-ID, titel, forfatter) ",
            "for alle indekserede bøger\n",
            "• Store valg: hvis du vælger mere end 50 bøger, foreslår Ask AI Search i stedet for ",
            "at indlejre hver bog i detaljeret format\n",
            "• Hold data opdateret: klik \"Opdater biblioteksdata\" efter tilføjelse eller fjernelse af bøger\n\n",
            "Eksempler: \"Find bøger om Python\", \"Vis mig bøger af Isaac Asimov\".",
        ),
        "ai_search_usage_hint": _q(
            "Tip: AI Search fungerer bedst til biblioteksomfattende opdagelse. For dybdegående ",
            "sammenligning af få bøger, vælg op til 30 bøger i stedet.",
        ),
        "ai_search_data_title": "Biblioteksindex",
        "ai_search_data_subtitle": (
            "Opdater den kompakte bogliste sendt til AI, når du tilføjer eller fjerner bøger"
        ),
    }


def _block_26_es() -> dict:
    return {
        "question_too_long_detail": _q(
            "El prompt es demasiado largo ({current} caracteres, límite {limit}, excede por {over}). ",
            "Ha seleccionado {book_count} libro(s).",
        ),
        "question_too_long_detail_library": _q(
            "El prompt es demasiado largo ({current} caracteres, límite {limit}, excede por {over}). ",
            "Su índice de biblioteca contiene {book_count} libro(s).",
        ),
        "question_too_long_hint_ai_search": _q(
            "Para búsquedas en toda la biblioteca, use AI Search (pregunte sin seleccionar libros, ",
            "o use el menú AI Search) en lugar de seleccionar muchos libros.",
        ),
        "question_too_long_hint_library_search": _q(
            "Su índice de biblioteca supera el límite de prompt actual. Active el límite de longitud ",
            "de prompt personalizado en Configuración del plugin → General (sugerido: 524288 caracteres), ",
            "o formule una pregunta más específica.",
        ),
        "question_too_long_reduce_books": _q(
            "Para comparar un conjunto más pequeño en profundidad, intente deseleccionar unos {count} libro(s).",
        ),
        "question_too_long_hint_default": _q(
            "Límite predeterminado actual: {limit} caracteres ({mode}). ",
            "El predeterminado para un libro es 128.000; para varios libros, 256.000. ",
            "Los usuarios avanzados pueden activar un límite personalizado en Configuración del plugin → General.",
        ),
        "question_too_long_hint_custom": _q(
            "Ha activado un límite de prompt personalizado. Si las solicitudes agotan el tiempo de espera, ",
            "reduzca el límite en Configuración del plugin → General, o reduzca los libros seleccionados / ",
            "use una consulta más específica.",
        ),
        "large_selection_dialog_title": "Muchos libros seleccionados",
        "large_selection_dialog_message": _q(
            "Ha seleccionado {count} libros. Para preguntas sobre toda la biblioteca, AI Search funciona mejor ",
            "y busca en toda su biblioteca con metadatos compactos.\n\n",
            "¿Cambiar a AI Search o continuar con los libros seleccionados en formato compacto?",
        ),
        "large_selection_use_ai_search": "Usar AI Search",
        "large_selection_continue": "Continuar con la selección",
        "multi_book_truncation_note": _q(
            "Nota: Solo se incluyen los primeros {included} de {total} libros seleccionados debido al ",
            "límite de prompt. Use AI Search para consultar toda su biblioteca, o aumente el límite ",
            "personalizado en Configuración del plugin → General.",
        ),
        "library_metadata_truncation_note": _q(
            "Nota: Solo se incluyen los primeros {included} de {total} libros indexados debido al ",
            "límite de prompt. Los resultados pueden ser incompletos para bibliotecas muy grandes a menos ",
            "que aumente el límite personalizado en Configuración del plugin → General.",
        ),
        "enable_custom_prompt_limit_label": "Límite de longitud de prompt personalizado",
        "enable_custom_prompt_limit_tooltip": _q(
            "Los límites predeterminados son 128.000 caracteres (un libro) y 256.000 (varios libros). ",
            "La mayoría de los usuarios no necesitan cambiar esto. Para búsquedas en toda la biblioteca, use AI Search. ",
            "Active un límite personalizado solo si su modelo admite un contexto mucho mayor y ",
            "las solicitudes siguen alcanzando el límite.",
        ),
        "max_prompt_length_label": "Longitud máx. del prompt:",
        "max_prompt_length_unit": "caracteres",
        "max_prompt_length_tooltip": _q(
            "Se aplica cuando el límite personalizado está activado. Sugerencia predeterminada: 524288 caracteres. ",
            "Guía aproximada: 1 token ≈ 3–4 caracteres. Para Ollama, configure también num_ctx en el modelo.",
        ),
        "max_prompt_length_normalized_title": "Límite de prompt ajustado",
        "max_prompt_length_normalized": _q(
            "La longitud del prompt se normalizó a {value} caracteres (se eliminaron separadores ",
            "como comas o espacios).",
        ),
        "ai_search_feature_title": "AI Search",
        "ai_search_feature_subtitle": "Busque en toda su biblioteca con lenguaje natural",
        "ai_search_feature_description": _q(
            "AI Search le ayuda a descubrir libros en toda su biblioteca Calibre.\n\n",
            "• Activar: abra Ask sin seleccionar libros, use Herramientas → AI Search o un atajo\n",
            "• Funcionamiento: el plugin envía metadatos compactos (ID, título, autor) ",
            "de todos los libros indexados\n",
            "• Selecciones grandes: si selecciona más de 50 libros, Ask sugerirá AI Search en lugar de ",
            "incrustar cada libro en formato detallado\n",
            "• Mantenga los datos actualizados: haga clic en \"Actualizar datos de biblioteca\" al añadir o eliminar libros\n\n",
            "Ejemplos: \"Encuentra libros sobre Python\", \"Muéstrame libros de Isaac Asimov\".",
        ),
        "ai_search_usage_hint": _q(
            "Consejo: AI Search funciona mejor para descubrimiento en toda la biblioteca. Para comparar ",
            "pocos libros en profundidad, seleccione hasta 30 libros.",
        ),
        "ai_search_data_title": "Índice de biblioteca",
        "ai_search_data_subtitle": (
            "Actualice la lista compacta de libros enviada a la IA cuando añada o elimine libros"
        ),
    }


def _block_26_fi() -> dict:
    return {
        "question_too_long_detail": _q(
            "Kehote on liian pitkä ({current} merkkiä, raja {limit}, yli {over}). ",
            "Olet valinnut {book_count} kirjaa.",
        ),
        "question_too_long_detail_library": _q(
            "Kehote on liian pitkä ({current} merkkiä, raja {limit}, yli {over}). ",
            "Kirjastoindeksissäsi on {book_count} kirjaa.",
        ),
        "question_too_long_hint_ai_search": _q(
            "Kirjastonlaajuisiin hakuun käytä AI Search -toimintoa (kysy valitsematta kirjoja ",
            "tai käytä AI Search -valikkoa) sen sijaan, että valitsisit monta kirjaa.",
        ),
        "question_too_long_hint_library_search": _q(
            "Kirjastoindeksisi ylittää nykyisen kehotteen rajan. Ota käyttöön mukautettu kehotteen ",
            "pituusraja kohdassa Lisäosan asetukset → General (suositus: 524288 merkkiä), ",
            "tai esitä tarkempi kysymys.",
        ),
        "question_too_long_reduce_books": _q(
            "Vertaillaksesi pienempää joukkoa syvällisesti, kokeile poistaa valinta noin {count} kirjasta.",
        ),
        "question_too_long_hint_default": _q(
            "Nykyinen oletusraja: {limit} merkkiä ({mode}). ",
            "Yhden kirjan oletus on 128 000; usean kirjan oletus on 256 000. ",
            "Edistyneet käyttäjät voivat ottaa mukautetun rajan käyttöön kohdassa Lisäosan asetukset → General.",
        ),
        "question_too_long_hint_custom": _q(
            "Olet ottanut mukautetun kehotteen rajan käyttöön. Jos pyynnöt aikakatkaistaan, ",
            "laske rajaa kohdassa Lisäosan asetukset → General tai vähennä valittuja kirjoja / ",
            "käytä tarkempaa kyselyä.",
        ),
        "large_selection_dialog_title": "Monta kirjaa valittu",
        "large_selection_dialog_message": _q(
            "Olet valinnut {count} kirjaa. Kirjastonlaajuisiin kysymyksiin AI Search sopii paremmin ",
            "ja hakee koko kirjastostasi tiiviillä metatiedoilla.\n\n",
            "Vaihdetaanko AI Searchiin vai jatketaanko valituilla kirjoilla tiiviissä muodossa?",
        ),
        "large_selection_use_ai_search": "Käytä AI Search",
        "large_selection_continue": "Jatka valinnalla",
        "multi_book_truncation_note": _q(
            "Huom: Vain ensimmäiset {included}/{total} valittua kirjaa sisältyvät kehotteen rajan vuoksi. ",
            "Käytä AI Search -hakua koko kirjastoon tai nosta mukautettua rajaa kohdassa ",
            "Lisäosan asetukset → General.",
        ),
        "library_metadata_truncation_note": _q(
            "Huom: Vain ensimmäiset {included}/{total} indeksoitua kirjaa sisältyvät kehotteen rajan vuoksi. ",
            "Tulokset voivat olla puutteellisia hyvin suurissa kirjastoissa, ellei mukautettua rajaa ",
            "nosteta kohdassa Lisäosan asetukset → General.",
        ),
        "enable_custom_prompt_limit_label": "Mukautettu kehotteen pituusraja",
        "enable_custom_prompt_limit_tooltip": _q(
            "Oletusrajat ovat 128 000 merkkiä (yksi kirja) ja 256 000 (useita kirjoja). ",
            "Useimmat käyttäjät eivät tarvitse muutosta. Kirjastonlaajuisiin hakuun käytä AI Search -toimintoa. ",
            "Ota mukautettu raja käyttöön vain, jos mallisi tukee paljon suurempaa kontekstia ja ",
            "pyynnöt yhä osuvat rajaan.",
        ),
        "max_prompt_length_label": "Kehotteen enimmäispituus:",
        "max_prompt_length_unit": "merkkiä",
        "max_prompt_length_tooltip": _q(
            "Voimassa, kun mukautettu raja on käytössä. Oletussuositus: 524288 merkkiä. ",
            "Karkea ohje: 1 token ≈ 3–4 merkkiä. Ollamalla aseta myös num_ctx mallipuolella.",
        ),
        "max_prompt_length_normalized_title": "Kehotteen raja säädetty",
        "max_prompt_length_normalized": _q(
            "Kehotteen pituus normalisoitiin arvoon {value} merkkiä (erottimet kuten pilkut ",
            "tai välilyönnit poistettiin).",
        ),
        "ai_search_feature_title": "AI Search",
        "ai_search_feature_subtitle": "Hae koko kirjastostasi luonnollisella kielellä",
        "ai_search_feature_description": _q(
            "AI Search auttaa löytämään kirjoja koko Calibre-kirjastostasi.\n\n",
            "• Käynnistys: avaa Ask valitsematta kirjoja, käytä Työkalut → AI Search tai pikanäppäin\n",
            "• Toiminta: lisäosa lähettää tiiviit metatiedot (kirja-ID, otsikko, tekijä) ",
            "kaikista indeksoiduista kirjoista\n",
            "• Suuret valinnat: yli 50 kirjan valinta ehdottaa AI Search -toimintoa sen sijaan, ",
            "että jokainen kirja upotettaisiin yksityiskohtaisessa muodossa\n",
            "• Pidä tiedot ajan tasalla: napsauta \"Päivitä kirjastotiedot\" lisättyäsi tai poistettuasi kirjoja\n\n",
            "Esimerkkejä: \"Etsi kirjoja Pythonista\", \"Näytä Isaac Asimovin kirjoja\".",
        ),
        "ai_search_usage_hint": _q(
            "Vinkki: AI Search sopii parhaiten koko kirjaston löytämiseen. Vertaillaksesi ",
            "muutamaa kirjaa syvällisesti, valitse enintään 30 kirjaa.",
        ),
        "ai_search_data_title": "Kirjastoindeksi",
        "ai_search_data_subtitle": (
            "Päivitä tekoälylle lähetettävä tiivis kirjalista, kun lisäät tai poistat kirjoja"
        ),
    }


def _block_26_nl() -> dict:
    return {
        "question_too_long_detail": _q(
            "Prompt is te lang ({current} tekens, limiet {limit}, {over} te veel). ",
            "U heeft {book_count} boek/boeken geselecteerd.",
        ),
        "question_too_long_detail_library": _q(
            "Prompt is te lang ({current} tekens, limiet {limit}, {over} te veel). ",
            "Uw bibliotheekindex bevat {book_count} boek/boeken.",
        ),
        "question_too_long_hint_ai_search": _q(
            "Gebruik voor bibliotheekbrede zoekopdrachten AI Search (vraag zonder boeken te selecteren ",
            "of gebruik het AI Search-menu) in plaats van veel boeken te selecteren.",
        ),
        "question_too_long_hint_library_search": _q(
            "Uw bibliotheekindex overschrijdt de huidige promptlimiet. Schakel aangepaste promptlengtelimiet in ",
            "onder Plugin-configuratie → General (aanbevolen: 524288 tekens), of stel een specifiekere vraag.",
        ),
        "question_too_long_reduce_books": _q(
            "Om een kleinere set diepgaand te vergelijken, probeer ongeveer {count} boek/boeken te deselecteren.",
        ),
        "question_too_long_hint_default": _q(
            "Huidige standaardlimiet: {limit} tekens ({mode}). ",
            "Standaard enkel boek is 128.000; meerdere boeken 256.000. ",
            "Gevorderde gebruikers kunnen een aangepaste limiet inschakelen onder Plugin-configuratie → General.",
        ),
        "question_too_long_hint_custom": _q(
            "U heeft een aangepaste promptlimiet ingeschakeld. Als verzoeken time-out krijgen, verlaag de limiet ",
            "onder Plugin-configuratie → General, of verminder geselecteerde boeken / gebruik een specifiekere query.",
        ),
        "large_selection_dialog_title": "Veel boeken geselecteerd",
        "large_selection_dialog_message": _q(
            "U heeft {count} boeken geselecteerd. Voor bibliotheekbrede vragen werkt AI Search beter ",
            "en doorzoekt uw hele bibliotheek met compacte metadata.\n\n",
            "Overschakelen naar AI Search, of doorgaan met de geselecteerde boeken in compact formaat?",
        ),
        "large_selection_use_ai_search": "AI Search gebruiken",
        "large_selection_continue": "Doorgaan met selectie",
        "multi_book_truncation_note": _q(
            "Let op: vanwege de promptlimiet zijn alleen de eerste {included} van {total} geselecteerde boeken opgenomen. ",
            "Gebruik AI Search om uw hele bibliotheek te doorzoeken, of verhoog de aangepaste limiet ",
            "onder Plugin-configuratie → General.",
        ),
        "library_metadata_truncation_note": _q(
            "Let op: vanwege de promptlimiet zijn alleen de eerste {included} van {total} geïndexeerde boeken opgenomen. ",
            "Resultaten kunnen onvolledig zijn voor zeer grote bibliotheken tenzij u de aangepaste limiet ",
            "verhoogt onder Plugin-configuratie → General.",
        ),
        "enable_custom_prompt_limit_label": "Aangepaste promptlengtelimiet",
        "enable_custom_prompt_limit_tooltip": _q(
            "Standaardlimieten zijn 128.000 tekens (enkel boek) en 256.000 (meerdere boeken). ",
            "De meeste gebruikers hoeven dit niet te wijzigen. Gebruik AI Search voor bibliotheekbrede zoekopdrachten. ",
            "Schakel alleen een aangepaste limiet in als uw model een veel grotere context ondersteunt en ",
            "verzoeken nog steeds de limiet bereiken.",
        ),
        "max_prompt_length_label": "Max. promptlengte:",
        "max_prompt_length_unit": "tekens",
        "max_prompt_length_tooltip": _q(
            "Geldt wanneer aangepaste limiet is ingeschakeld. Standaard suggestie: 524288 tekens. ",
            "Ruwe richtlijn: 1 token ≈ 3–4 tekens. Stel bij Ollama ook num_ctx in aan modelzijde.",
        ),
        "max_prompt_length_normalized_title": "Promptlimiet aangepast",
        "max_prompt_length_normalized": _q(
            "Promptlengte is genormaliseerd naar {value} tekens (scheidingstekens zoals komma's ",
            "of spaties zijn verwijderd).",
        ),
        "ai_search_feature_title": "AI Search",
        "ai_search_feature_subtitle": "Doorzoek uw hele bibliotheek met natuurlijke taal",
        "ai_search_feature_description": _q(
            "AI Search helpt u boeken te ontdekken in uw hele Calibre-bibliotheek.\n\n",
            "• Activeren: open Ask zonder boeken te selecteren, gebruik Extra → AI Search of een sneltoets\n",
            "• Werking: de plugin stuurt compacte metadata (boek-ID, titel, auteur) ",
            "van alle geïndexeerde boeken\n",
            "• Grote selecties: bij meer dan 50 boeken stelt Ask AI Search voor in plaats van ",
            "elk boek in uitgebreid formaat in te sluiten\n",
            "• Houd gegevens actueel: klik \"Bibliotheekgegevens bijwerken\" na toevoegen of verwijderen van boeken\n\n",
            "Voorbeelden: \"Vind boeken over Python\", \"Toon boeken van Isaac Asimov\".",
        ),
        "ai_search_usage_hint": _q(
            "Tip: AI Search werkt het best voor bibliotheekbrede ontdekking. Voor diepgaande vergelijking ",
            "van enkele boeken, selecteer maximaal 30 boeken.",
        ),
        "ai_search_data_title": "Bibliotheekindex",
        "ai_search_data_subtitle": (
            "Vernieuw de compacte boekenlijst die naar AI wordt gestuurd wanneer u boeken toevoegt of verwijdert"
        ),
    }


def _block_26_no() -> dict:
    return {
        "question_too_long_detail": _q(
            "Prompten er for lang ({current} tegn, grense {limit}, overskrider med {over}). ",
            "Du har valgt {book_count} bok/bøker.",
        ),
        "question_too_long_detail_library": _q(
            "Prompten er for lang ({current} tegn, grense {limit}, overskrider med {over}). ",
            "Biblioteksindeksen din inneholder {book_count} bok/bøker.",
        ),
        "question_too_long_hint_ai_search": _q(
            "For bibliotekomfattende søk, bruk AI Search (spør uten å velge bøker, ",
            "eller bruk AI Search-menyen) i stedet for å velge mange bøker.",
        ),
        "question_too_long_hint_library_search": _q(
            "Biblioteksindeksen overskrider gjeldende promptgrense. Aktiver tilpasset promptlengdegrense ",
            "under Plugin-konfigurasjon → General (foreslått: 524288 tegn), ",
            "eller still et mer spesifikt spørsmål.",
        ),
        "question_too_long_reduce_books": _q(
            "For å sammenligne et mindre sett i dybden, prøv å fjerne valg av ca. {count} bok/bøker.",
        ),
        "question_too_long_hint_default": _q(
            "Gjeldende standardgrense: {limit} tegn ({mode}). ",
            "Standard for enkelt bok er 128.000; for flere bøker 256.000. ",
            "Avanserte brukere kan aktivere en tilpasset grense under Plugin-konfigurasjon → General.",
        ),
        "question_too_long_hint_custom": _q(
            "Du har aktivert en tilpasset promptgrense. Hvis forespørsler får tidsavbrudd, senk grensen ",
            "under Plugin-konfigurasjon → General, eller reduser valgte bøker / bruk en mer spesifikk forespørsel.",
        ),
        "large_selection_dialog_title": "Mange bøker valgt",
        "large_selection_dialog_message": _q(
            "Du har valgt {count} bøker. For bibliotekomfattende spørsmål fungerer AI Search bedre ",
            "og søker i hele biblioteket med kompakte metadata.\n\n",
            "Bytte til AI Search, eller fortsette med valgte bøker i kompakt format?",
        ),
        "large_selection_use_ai_search": "Bruk AI Search",
        "large_selection_continue": "Fortsett med valgte",
        "multi_book_truncation_note": _q(
            "Merk: På grunn av promptgrensen er bare de første {included} av {total} valgte bøker inkludert. ",
            "Bruk AI Search for å søke i hele biblioteket, eller øk den tilpassede grensen ",
            "under Plugin-konfigurasjon → General.",
        ),
        "library_metadata_truncation_note": _q(
            "Merk: På grunn av promptgrensen er bare de første {included} av {total} indekserte bøker inkludert. ",
            "Resultater kan være ufullstendige for svært store bibliotek med mindre du øker den tilpassede grensen ",
            "under Plugin-konfigurasjon → General.",
        ),
        "enable_custom_prompt_limit_label": "Tilpasset promptlengdegrense",
        "enable_custom_prompt_limit_tooltip": _q(
            "Standardgrenser er 128.000 tegn (enkelt bok) og 256.000 (flere bøker). ",
            "De fleste brukere trenger ikke endre dette. For bibliotekomfattende søk, bruk AI Search. ",
            "Aktiver bare en tilpasset grense hvis modellen støtter mye større kontekst og ",
            "forespørsler fortsatt treffer grensen.",
        ),
        "max_prompt_length_label": "Maks. promptlengde:",
        "max_prompt_length_unit": "tegn",
        "max_prompt_length_tooltip": _q(
            "Gjelder når tilpasset grense er aktivert. Standardforslag: 524288 tegn. ",
            "Grovt estimat: 1 token ≈ 3–4 tegn. For Ollama, sett også num_ctx på modellsiden.",
        ),
        "max_prompt_length_normalized_title": "Promptgrense justert",
        "max_prompt_length_normalized": _q(
            "Promptlengden ble normalisert til {value} tegn (skilletegn som kommaer ",
            "eller mellomrom ble fjernet).",
        ),
        "ai_search_feature_title": "AI Search",
        "ai_search_feature_subtitle": "Søk i hele biblioteket med naturlig språk",
        "ai_search_feature_description": _q(
            "AI Search hjelper deg å finne bøker i hele Calibre-biblioteket.\n\n",
            "• Utløs: åpne Ask uten å velge bøker, bruk Verktøy → AI Search eller snarvei\n",
            "• Slik fungerer det: pluginet sender kompakte metadata (bok-ID, tittel, forfatter) ",
            "for alle indekserte bøker\n",
            "• Store valg: hvis du velger mer enn 50 bøker, foreslår Ask AI Search i stedet for ",
            "å bygge inn hver bok i detaljert format\n",
            "• Hold data oppdatert: klikk \"Oppdater biblioteksdata\" etter å ha lagt til eller fjernet bøker\n\n",
            "Eksempler: \"Finn bøker om Python\", \"Vis meg bøker av Isaac Asimov\".",
        ),
        "ai_search_usage_hint": _q(
            "Tips: AI Search fungerer best for bibliotekomfattende oppdagelse. For dyptgående ",
            "sammenligning av få bøker, velg opptil 30 bøker.",
        ),
        "ai_search_data_title": "Biblioteksindeks",
        "ai_search_data_subtitle": (
            "Oppdater den kompakte boklisten som sendes til AI når du legger til eller fjerner bøker"
        ),
    }


def _block_26_ru() -> dict:
    return {
        "question_too_long_detail": _q(
            "Подсказка слишком длинная ({current} символов, лимит {limit}, превышение на {over}). ",
            "Вы выбрали {book_count} книг(и).",
        ),
        "question_too_long_detail_library": _q(
            "Подсказка слишком длинная ({current} символов, лимит {limit}, превышение на {over}). ",
            "В индексе библиотеки {book_count} книг(и).",
        ),
        "question_too_long_hint_ai_search": _q(
            "Для поиска по всей библиотеке используйте AI Search (задавайте вопрос без выбора книг ",
            "или через меню AI Search), а не выбирайте много книг сразу.",
        ),
        "question_too_long_hint_library_search": _q(
            "Индекс библиотеки превышает текущий лимит подсказки. Включите пользовательский лимит длины ",
            "в Настройках плагина → General (рекомендуется: 524288 символов) или задайте более конкретный вопрос.",
        ),
        "question_too_long_reduce_books": _q(
            "Для глубокого сравнения меньшего набора попробуйте снять выбор примерно с {count} книг(и).",
        ),
        "question_too_long_hint_default": _q(
            "Текущий лимит по умолчанию: {limit} символов ({mode}). ",
            "Для одной книги по умолчанию 128 000; для нескольких — 256 000. ",
            "Опытные пользователи могут включить пользовательский лимит в Настройках плагина → General.",
        ),
        "question_too_long_hint_custom": _q(
            "Вы включили пользовательский лимит подсказки. Если запросы завершаются по таймауту, ",
            "уменьшите лимит в Настройках плагина → General или сократите выбор книг / уточните запрос.",
        ),
        "large_selection_dialog_title": "Выбрано много книг",
        "large_selection_dialog_message": _q(
            "Вы выбрали {count} книг. Для вопросов по всей библиотеке лучше подходит AI Search — ",
            "он ищет по всей библиотеке в компактном формате метаданных.\n\n",
            "Переключиться на AI Search или продолжить с выбранными книгами в компактном формате?",
        ),
        "large_selection_use_ai_search": "Использовать AI Search",
        "large_selection_continue": "Продолжить с выбором",
        "multi_book_truncation_note": _q(
            "Примечание: из-за лимита подсказки включены только первые {included} из {total} выбранных книг. ",
            "Используйте AI Search для запроса ко всей библиотеке или увеличьте пользовательский лимит ",
            "в Настройках плагина → General.",
        ),
        "library_metadata_truncation_note": _q(
            "Примечание: из-за лимита подсказки включены только первые {included} из {total} проиндексированных книг. ",
            "Результаты могут быть неполными для очень больших библиотек, если не увеличить пользовательский лимит ",
            "в Настройках плагина → General.",
        ),
        "enable_custom_prompt_limit_label": "Пользовательский лимит длины подсказки",
        "enable_custom_prompt_limit_tooltip": _q(
            "Лимиты по умолчанию: 128 000 символов (одна книга) и 256 000 (несколько книг). ",
            "Большинству пользователей менять не нужно. Для поиска по библиотеке используйте AI Search. ",
            "Включайте пользовательский лимит только если модель поддерживает гораздо больший контекст и ",
            "запросы всё ещё упираются в лимит.",
        ),
        "max_prompt_length_label": "Макс. длина подсказки:",
        "max_prompt_length_unit": "символов",
        "max_prompt_length_tooltip": _q(
            "Применяется при включённом пользовательском лимите. Рекомендуемое значение: 524288 символов. ",
            "Ориентир: 1 токен ≈ 3–4 символа. Для Ollama также настройте num_ctx на стороне модели.",
        ),
        "max_prompt_length_normalized_title": "Лимит подсказки скорректирован",
        "max_prompt_length_normalized": _q(
            "Длина подсказки нормализована до {value} символов (удалены разделители вроде запятых ",
            "или пробелов).",
        ),
        "ai_search_feature_title": "AI Search",
        "ai_search_feature_subtitle": "Ищите по всей библиотеке на естественном языке",
        "ai_search_feature_description": _q(
            "AI Search помогает находить книги во всей библиотеке Calibre.\n\n",
            "• Запуск: откройте Ask без выбора книг, используйте Сервис → AI Search или сочетание клавиш\n",
            "• Как работает: плагин отправляет компактные метаданные (ID, название, автор) ",
            "всех проиндексированных книг\n",
            "• Большой выбор: при выборе более 50 книг Ask предложит AI Search вместо ",
            "встраивания каждой книги в подробном формате\n",
            "• Обновляйте данные: нажимайте «Обновить данные библиотеки» после добавления или удаления книг\n\n",
            "Примеры: «Найди книги о Python», «Покажи книги Айзека Азимова».",
        ),
        "ai_search_usage_hint": _q(
            "Совет: AI Search лучше всего подходит для поиска по всей библиотеке. Для глубокого сравнения ",
            "нескольких книг выберите до 30 книг.",
        ),
        "ai_search_data_title": "Индекс библиотеки",
        "ai_search_data_subtitle": (
            "Обновите компактный список книг для AI при добавлении или удалении книг"
        ),
    }


def _block_26_sv() -> dict:
    return {
        "question_too_long_detail": _q(
            "Prompten är för lång ({current} tecken, gräns {limit}, överskrider med {over}). ",
            "Du har valt {book_count} bok/böcker.",
        ),
        "question_too_long_detail_library": _q(
            "Prompten är för lång ({current} tecken, gräns {limit}, överskrider med {over}). ",
            "Ditt biblioteksindex innehåller {book_count} bok/böcker.",
        ),
        "question_too_long_hint_ai_search": _q(
            "För biblioteksomfattande sökningar, använd AI Search (fråga utan att välja böcker ",
            "eller använd AI Search-menyn) i stället för att välja många böcker.",
        ),
        "question_too_long_hint_library_search": _q(
            "Ditt biblioteksindex överskrider den aktuella promptgränsen. Aktivera anpassad promptlängdsgräns ",
            "under Plugin-konfiguration → General (föreslaget: 524288 tecken), ",
            "eller ställ en mer specifik fråga.",
        ),
        "question_too_long_reduce_books": _q(
            "För att jämföra ett mindre urval på djupet, prova att avmarkera cirka {count} bok/böcker.",
        ),
        "question_too_long_hint_default": _q(
            "Aktuell standardgräns: {limit} tecken ({mode}). ",
            "Standard för en bok är 128 000; för flera böcker 256 000. ",
            "Avancerade användare kan aktivera en anpassad gräns under Plugin-konfiguration → General.",
        ),
        "question_too_long_hint_custom": _q(
            "Du har aktiverat en anpassad promptgräns. Om förfrågningar får timeout, sänk gränsen ",
            "under Plugin-konfiguration → General, eller minska valda böcker / använd en mer specifik fråga.",
        ),
        "large_selection_dialog_title": "Många böcker valda",
        "large_selection_dialog_message": _q(
            "Du har valt {count} böcker. För biblioteksomfattande frågor fungerar AI Search bättre ",
            "och söker i hela biblioteket med kompakt metadata.\n\n",
            "Byta till AI Search, eller fortsätta med valda böcker i kompakt format?",
        ),
        "large_selection_use_ai_search": "Använd AI Search",
        "large_selection_continue": "Fortsätt med valda",
        "multi_book_truncation_note": _q(
            "Obs: Endast de första {included} av {total} valda böcker ingår på grund av promptgränsen. ",
            "Använd AI Search för att söka i hela biblioteket, eller höj den anpassade gränsen ",
            "under Plugin-konfiguration → General.",
        ),
        "library_metadata_truncation_note": _q(
            "Obs: Endast de första {included} av {total} indexerade böcker ingår på grund av promptgränsen. ",
            "Resultat kan vara ofullständiga för mycket stora bibliotek om du inte höjer den anpassade gränsen ",
            "under Plugin-konfiguration → General.",
        ),
        "enable_custom_prompt_limit_label": "Anpassad promptlängdsgräns",
        "enable_custom_prompt_limit_tooltip": _q(
            "Standardgränser är 128 000 tecken (en bok) och 256 000 (flera böcker). ",
            "De flesta användare behöver inte ändra detta. För biblioteksomfattande sökningar, använd AI Search. ",
            "Aktivera bara en anpassad gräns om din modell stöder mycket större kontext och ",
            "förfrågningar fortfarande når gränsen.",
        ),
        "max_prompt_length_label": "Max. promptlängd:",
        "max_prompt_length_unit": "tecken",
        "max_prompt_length_tooltip": _q(
            "Gäller när anpassad gräns är aktiverad. Standardförslag: 524288 tecken. ",
            "Ungefärlig regel: 1 token ≈ 3–4 tecken. För Ollama, ställ även in num_ctx på modellsidan.",
        ),
        "max_prompt_length_normalized_title": "Promptgräns justerad",
        "max_prompt_length_normalized": _q(
            "Promptlängden normaliserades till {value} tecken (avgränsare som kommatecken ",
            "eller mellanslag togs bort).",
        ),
        "ai_search_feature_title": "AI Search",
        "ai_search_feature_subtitle": "Sök i hela biblioteket med naturligt språk",
        "ai_search_feature_description": _q(
            "AI Search hjälper dig hitta böcker i hela ditt Calibre-bibliotek.\n\n",
            "• Utlös: öppna Ask utan att välja böcker, använd Verktyg → AI Search eller genväg\n",
            "• Så fungerar det: pluginet skickar kompakt metadata (bok-ID, titel, författare) ",
            "för alla indexerade böcker\n",
            "• Stora val: om du väljer fler än 50 böcker föreslår Ask AI Search i stället för ",
            "att bädda in varje bok i detaljerat format\n",
            "• Håll data uppdaterad: klicka \"Uppdatera biblioteksdata\" efter att ha lagt till eller tagit bort böcker\n\n",
            "Exempel: \"Hitta böcker om Python\", \"Visa böcker av Isaac Asimov\".",
        ),
        "ai_search_usage_hint": _q(
            "Tips: AI Search fungerar bäst för biblioteksomfattande upptäckt. För djupgående ",
            "jämförelse av få böcker, välj upp till 30 böcker.",
        ),
        "ai_search_data_title": "Biblioteksindex",
        "ai_search_data_subtitle": (
            "Uppdatera den kompakta boklistan som skickas till AI när du lägger till eller tar bort böcker"
        ),
    }


def _block_26_yue() -> dict:
    return {
        "question_too_long_detail": _q(
            "提示詞太長（目前 {current} 字，限制 {limit} 字，超出 {over} 字）。",
            "你揀咗 {book_count} 本書。",
        ),
        "question_too_long_detail_library": _q(
            "提示詞太長（目前 {current} 字，限制 {limit} 字，超出 {over} 字）。",
            "書庫索引共有 {book_count} 本書。",
        ),
        "question_too_long_hint_ai_search": _q(
            "書庫級搜尋請用 AI Search（唔揀書直接問，或者用 AI Search 選單），",
            "唔好一次揀太多書。",
        ),
        "question_too_long_hint_library_search": _q(
            "書庫索引超出目前提示詞限制。請喺「插件配置 → General」啟用自訂提示詞長度限制",
            "（建議 524288 字），或者問得具體啲。",
        ),
        "question_too_long_reduce_books": _q(
            "如果想深入比較少啲書，試下取消揀大約 {count} 本書。",
        ),
        "question_too_long_hint_default": _q(
            "目前預設限制：{limit} 字（{mode}）。",
            "單書預設 128,000 字，多書預設 256,000 字。",
            "進階用戶可以喺「插件配置 → General」啟用自訂提示詞長度限制。",
        ),
        "question_too_long_hint_custom": _q(
            "你已啟用自訂提示詞長度限制。如果請求超時，請喺「插件配置 → General」調低限制，",
            "或者減少揀嘅書 / 問得具體啲。",
        ),
        "large_selection_dialog_title": "揀咗太多書",
        "large_selection_dialog_message": _q(
            "你揀咗 {count} 本書。書庫級問題用 AI Search 更啱，",
            "會用緊湊格式搜尋成個書庫。\n\n",
            "要切換去 AI Search，定係繼續用而家揀嘅書（緊湊格式）？",
        ),
        "large_selection_use_ai_search": "用 AI Search",
        "large_selection_continue": "繼續用而家揀嘅",
        "multi_book_truncation_note": _q(
            "注意：因提示詞長度限制，只包含頭 {included} / {total} 本揀咗嘅書。",
            "請用 AI Search 搜尋成個書庫，或者喺「插件配置 → General」提高自訂限制。",
        ),
        "library_metadata_truncation_note": _q(
            "注意：因提示詞長度限制，只包含頭 {included} / {total} 本已索引書籍。",
            "超大書庫嘅結果可能唔完整，可以喺「插件配置 → General」提高自訂限制。",
        ),
        "enable_custom_prompt_limit_label": "自訂提示詞長度限制",
        "enable_custom_prompt_limit_tooltip": _q(
            "預設限制係單書 128,000 字、多書 256,000 字，大多數用戶唔使改。",
            "書庫級搜尋請用 AI Search。只有模型支援更大上下文而且仍然撞限制時先啟用自訂。",
        ),
        "max_prompt_length_label": "最大提示詞長度：",
        "max_prompt_length_unit": "字",
        "max_prompt_length_tooltip": _q(
            "啟用自訂限制後生效。建議預設值：524288 字。",
            "粗略參考：1 token ≈ 3–4 字。用 Ollama 時仲要喺模型側設定 num_ctx。",
        ),
        "max_prompt_length_normalized_title": "提示詞長度已調整",
        "max_prompt_length_normalized": _q(
            "提示詞長度已規範為 {value} 字（已移除逗號、空格等分隔符）。",
        ),
        "ai_search_feature_title": "AI 搜尋",
        "ai_search_feature_subtitle": "用自然語言搜尋成個書庫",
        "ai_search_feature_description": _q(
            "AI 搜尋幫你喺成個 Calibre 書庫搵書。\n\n",
            "• 觸發：唔揀書開 Ask、用「工具 → AI 搜尋」或者快捷鍵\n",
            "• 原理：插件以緊湊格式（書籍 ID、書名、作者）發送已索引嘅全部書籍元數據\n",
            "• 大量揀書：揀超過 50 本時，Ask 會建議用 AI 搜尋，而唔係把每本書詳細元數據塞入提示詞\n",
            "• 保持數據新鮮：加書或刪書之後，請撳「更新書庫數據」\n\n",
            "示例：「有冇 Python 相關嘅書？」「俾我睇阿西莫夫嘅書」。",
        ),
        "ai_search_usage_hint": _q(
            "提示：AI 搜尋最啱書庫級發現。如果想深入比較少少書，直接揀唔超過 30 本就得。",
        ),
        "ai_search_data_title": "書庫索引",
        "ai_search_data_subtitle": "加書或刪書之後，請刷新發送畀 AI 嘅緊湊書單",
    }


def _block_de_ai_manager() -> dict:
    return {
        "ai_manager_title": "KI-Anbieter verwalten",
        "add_ai_title": "KI-Anbieter hinzufügen",
        "manage_ai_title": "Konfigurierte KI verwalten",
        "configured_ai_list": "Konfigurierte KI",
        "available_ai_list": "Verfügbar zum Hinzufügen",
        "ai_config_panel": "Konfiguration",
        "select_ai_to_configure": "Wählen Sie eine KI aus der Liste zum Konfigurieren",
        "select_provider": "KI-Anbieter auswählen",
        "select_provider_hint": "Wählen Sie einen Anbieter aus der Liste",
        "select_ai_to_edit": "Wählen Sie eine KI aus der Liste zum Bearbeiten",
        "set_as_default": "Als Standard festlegen",
        "save_ai_config": "Speichern",
        "remove_ai_config": "Entfernen",
        "delete_ai": "Löschen",
        "add_ai_button": "KI hinzufügen",
        "edit_ai_button": "KI bearbeiten",
        "manage_configured_ai_button": "Konfigurierte KI verwalten",
        "manage_ai_button": "KI verwalten",
        "no_configured_ai": "Noch keine KI konfiguriert",
        "no_configured_ai_hint": (
            "Keine KI konfiguriert. Plugin kann nicht funktionieren. "
            'Bitte klicken Sie auf "KI hinzufügen", um einen KI-Anbieter hinzuzufügen.'
        ),
        "default_ai_label": "Standard-KI:",
        "default_ai_tag": "Standard",
        "ai_not_configured_cannot_set_default": (
            "Diese KI ist noch nicht konfiguriert. Bitte speichern Sie zuerst die Konfiguration."
        ),
        "ai_set_as_default_success": "{name} wurde als Standard-KI festgelegt.",
        "ai_config_saved_success": "Konfiguration von {name} erfolgreich gespeichert.",
        "confirm_remove_title": "Entfernen bestätigen",
        "confirm_remove_ai": (
            "Sind Sie sicher, dass Sie {name} entfernen möchten? "
            "Dies löscht den API-Schlüssel und setzt die Konfiguration zurück."
        ),
        "confirm_delete_title": "Löschen bestätigen",
        "confirm_delete_ai": "Sind Sie sicher, dass Sie {name} löschen möchten?",
        "configuration": "Konfiguration",
        "metadata_pubdate": "Erscheinungsdatum",
        "max_prompt_length_normalized_title": "Prompt-Limit angepasst",
        "max_prompt_length_normalized": _q(
            "Die Prompt-Länge wurde auf {value} Zeichen normalisiert (Trennzeichen wie Kommas ",
            "oder Leerzeichen wurden entfernt).",
        ),
    }


def _block_fr() -> dict:
    return {
        "discard_changes": "Abandonner les modifications",
        "empty_response": "Réponse vide reçue de l'API",
        "empty_response_after_filter": (
            "La réponse est vide après filtrage des balises think"
        ),
        "error_401": (
            "Échec de l'authentification de la clé API. Veuillez vérifier : la clé API est correcte, "
            "le compte a un solde suffisant, la clé API n'a pas expiré."
        ),
        "error_403": (
            "Accès refusé. Veuillez vérifier : la clé API a des permissions suffisantes, "
            "aucune restriction d'accès régional."
        ),
        "error_404": (
            "Point de terminaison API introuvable. Veuillez vérifier si la configuration de l'URL de base API est correcte."
        ),
        "metadata_pubdate": "Date de publication",
        "max_prompt_length_normalized_title": "Limite de prompt ajustée",
        "max_prompt_length_normalized": _q(
            "La longueur du prompt a été normalisée à {value} caractères (des séparateurs tels que des virgules ",
            "ou des espaces ont été supprimés).",
        ),
        "pdf_ai_model_info": "INFORMATIONS SUR LE MODÈLE IA",
        "pdf_generated_by": "GÉNÉRÉ PAR",
        "pdf_provider": "Fournisseur",
        "pdf_model": "Modèle",
        "pdf_api_base_url": "URL de base API",
        "pdf_panel": "Panneau",
        "pdf_plugin": "Plugin",
        "pdf_github": "GitHub",
        "pdf_generated_time": "Heure de génération",
    }


def _block_normalized_pt() -> dict:
    return {
        "max_prompt_length_normalized_title": "Limite de prompt ajustado",
        "max_prompt_length_normalized": _q(
            "O comprimento do prompt foi normalizado para {value} caracteres (separadores como vírgulas ",
            "ou espaços foram removidos).",
        ),
    }


def _block_normalized_ja() -> dict:
    return {
        "metadata_pubdate": "出版日",
        "max_prompt_length_normalized_title": "プロンプト制限を調整しました",
        "max_prompt_length_normalized": _q(
            "プロンプト長を {value} 文字に正規化しました（カンマやスペースなどの区切り文字を削除しました）。",
        ),
    }


def _block_normalized_zht() -> dict:
    return {
        "metadata_pubdate": "出版日期",
        "max_prompt_length_normalized_title": "提示詞長度已調整",
        "max_prompt_length_normalized": _q(
            "提示詞長度已規範為 {value} 字元（已移除逗號、空格等分隔符）。",
        ),
    }


PATCHES: dict[str, dict] = {
    "en": EN_PATCH,
    "da": _block_26_da(),
    "es": _block_26_es(),
    "fi": _block_26_fi(),
    "nl": _block_26_nl(),
    "no": _block_26_no(),
    "ru": _block_26_ru(),
    "sv": _block_26_sv(),
    "yue": _block_26_yue(),
    "de": _block_de_ai_manager(),
    "fr": _block_fr(),
    "ja": _block_normalized_ja(),
    "pt": _block_normalized_pt(),
    "zht": _block_normalized_zht(),
}


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

KEY_RE = re.compile(r"""^\s+(['"])([^'"]+)\1\s*:""")


def extract_keys(content: str) -> set[str]:
    keys: set[str] = set()
    for line in content.splitlines():
        m = KEY_RE.match(line)
        if m:
            keys.add(m.group(2))
    return keys


def detect_indent(content: str) -> str:
    for line in content.splitlines():
        m = re.match(r"^(\s+)'plugin_name':", line)
        if m:
            return m.group(1)
    for line in content.splitlines():
        m = re.match(r"^(\s+)'plugin_name':", line.replace("\t", "    "))
        if m:
            return m.group(1)
    return "            "


def find_anchor_end(lines: list[str], anchor_key: str) -> int | None:
    pattern = re.compile(r"""^\s+(['"])""" + re.escape(anchor_key) + r"""\1\s*:""")
    for idx, line in enumerate(lines):
        if not pattern.match(line):
            continue
        if "(" in line and line.rstrip().endswith("("):
            end = idx + 1
            while end < len(lines) and not lines[end].strip().startswith("),"):
                end += 1
            return end + 1
        return idx + 1
    return None


def format_entry(key: str, value: str | tuple[str, ...], indent: str) -> str:
    inner = indent + "    "
    if isinstance(value, tuple):
        joined = "".join(value)
        if len(joined) <= 88 and "\n" not in joined:
            return f"{indent}'{key}': {joined!r},\n"
        parts = [f"{indent}'{key}': ("]
        for part in value:
            parts.append(f"{inner}{part!r}")
        parts.append(f"{indent}),")
        return "\n".join(parts) + "\n"
    return f"{indent}'{key}': {value!r},\n"


def apply_patches(content: str, patches: dict) -> tuple[str, list[str]]:
    existing = extract_keys(content)
    missing = {k: v for k, v in patches.items() if k not in existing}
    if not missing:
        return content, []

    indent = detect_indent(content)
    lines = content.splitlines(keepends=True)
    insertions: list[tuple[int, str]] = []

    for anchor, key_order in INSERT_AFTER:
        pos = find_anchor_end(lines, anchor)
        if pos is None:
            continue
        block_keys = [k for k in key_order if k in missing]
        if not block_keys:
            continue
        block = "".join(format_entry(k, missing[k], indent) for k in block_keys)
        insertions.append((pos, block))
        for k in block_keys:
            del missing[k]

    if missing:
        print(f"  warning: unanchored keys remain: {sorted(missing)}", file=sys.stderr)

    for pos, block in sorted(insertions, key=lambda x: x[0], reverse=True):
        lines.insert(pos, block)

    return "".join(lines), [k for k in patches if k not in existing]


def update_plugin_name(content: str, lang: str) -> tuple[str, bool]:
    if lang not in PLUGIN_NAMES:
        return content, False
    new_name = PLUGIN_NAMES[lang]
    new_content, n = re.subn(
        r"((['\"])plugin_name\2:\s*['\"]).*?(['\"])",
        rf"\g<1>{new_name}\3",
        content,
        count=1,
    )
    return new_content, n > 0


def patch_invalid_json(content: str, lang: str) -> tuple[str, bool]:
    if "invalid_json" in extract_keys(content):
        return content, False
    if lang not in INVALID_JSON_I18N:
        return content, False
    if "'invalid_response':" not in content:
        return content, False
    indent = detect_indent(content)
    entry = format_entry("invalid_json", INVALID_JSON_I18N[lang], indent)
    return content.replace(
        f"{indent}'invalid_response':",
        entry + f"{indent}'invalid_response':",
        1,
    ), True


def verify_keys() -> dict[str, dict]:
    en_keys = extract_keys((I18N / "en.py").read_text(encoding="utf-8"))
    report: dict[str, dict] = {"en_count": len(en_keys), "languages": {}}
    for path in sorted(I18N.glob("*.py")):
        if path.name in ("__init__.py", "base.py", "en.py"):
            continue
        lang = path.stem
        keys = extract_keys(path.read_text(encoding="utf-8"))
        report["languages"][lang] = {
            "count": len(keys),
            "missing": sorted(en_keys - keys),
            "extra": sorted(keys - en_keys),
            "ok": en_keys == keys,
        }
    return report


def main() -> int:
    patched_summary: dict[str, list[str]] = {}
    plugin_updates: list[str] = []

    all_langs = sorted({p.stem for p in I18N.glob("*.py") if p.name not in ("__init__.py", "base.py")})

    for lang in all_langs:
        path = I18N / f"{lang}.py"
        content = path.read_text(encoding="utf-8")
        added_keys: list[str] = []

        if lang in PATCHES:
            content, added_keys = apply_patches(content, PATCHES[lang])
        content, added_json = patch_invalid_json(content, lang)
        if added_json:
            added_keys.append("invalid_json")
        content, renamed = update_plugin_name(content, lang)
        if renamed:
            plugin_updates.append(lang)
        if added_keys:
            patched_summary[lang] = added_keys
        path.write_text(content, encoding="utf-8")

    print("=== apply_i18n_gaps.py results ===\n")
    print("Patched keys by language:")
    for lang in sorted(patched_summary):
        keys = patched_summary[lang]
        print(f"  {lang}: {len(keys)} keys — {', '.join(keys)}")

    if plugin_updates:
        print(f"\nplugin_name updated: {', '.join(sorted(set(plugin_updates)))}")

    print("\n=== Verification (AST key comparison vs en.py) ===")
    report = verify_keys()
    print(f"en.py: {report['en_count']} keys\n")
    all_ok = True
    for lang, info in sorted(report["languages"].items()):
        status = "OK" if info["ok"] else "MISMATCH"
        if not info["ok"]:
            all_ok = False
        print(f"  {lang}: {info['count']} keys [{status}]")
        if info["missing"]:
            print(f"    missing ({len(info['missing'])}): {info['missing']}")
        if info["extra"]:
            print(f"    extra ({len(info['extra'])}): {info['extra']}")

    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
