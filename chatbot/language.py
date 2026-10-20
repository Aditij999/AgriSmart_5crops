import re

SUPPORTED_LANGS = ("en", "hi", "mr")

_DEVANAGARI = re.compile(r"[\u0900-\u097F]")
_LATIN = re.compile(r"[A-Za-z]")

# Distinctive tokens (whole-word-ish) to tell Hindi and Marathi apart.
_MARATHI_MARKERS = (
    "आहे", "आहेत", "काय", "कसे", "कशी", "कसा", "माझी", "माझे", "माझा",
    "तुमची", "तुमचे", "तुमचा", "तुम्ही", "तुमच्या", "आम्ही", "आमची",
    "पीक", "पिक", "खत", "माती", "सांगा", "सांग", "किती", "हवे", "हवी",
    "करा", "करू", "करायचे", "योग्य", "कमी", "जास्त", "ऊस", "कापूस",
    "शेंगदाणा", "ज्वारी", "उत्पन्न", "उपज", "कृपया", "मदत", "अॅग्री",
    "नको", "होय", "नाहीतर", "आता", "पाहिजे",
)

_HINDI_MARKERS = (
    "है", "हैं", "क्या", "कैसे", "कैसी", "मेरी", "मेरा", "मेरे",
    "आपकी", "आपका", "आपके", "आप", "फसल", "खाद", "मिट्टी", "बताओ",
    "बताइए", "कितना", "कितनी", "चाहिए", "होगा", "गेहूं", "गेहूँ",
    "गन्ना", "कपास", "मूंगफली", "उपज", "कृपया", "मदद", "एग्री",
    "नहीं", "हाँ", "अभी", "चाहिये",
)

CROP_ALIASES = {
    "wheat": "Wheat",
    "गेहूं": "Wheat",
    "गेहूँ": "Wheat",
    "गेहू": "Wheat",
    "गहू": "Wheat",
    "गहूं": "Wheat",
    "jowar": "Jowar",
    "jawar": "Jowar",
    "sorghum": "Jowar",
    "ज्वार": "Jowar",
    "ज्वारी": "Jowar",
    "sugarcane": "Sugarcane",
    "cane": "Sugarcane",
    "गन्ना": "Sugarcane",
    "गन्ने": "Sugarcane",
    "ऊस": "Sugarcane",
    "ऊसाचे": "Sugarcane",
    "ऊसाच्या": "Sugarcane",
    "उसाचे": "Sugarcane",
    "उसाच्या": "Sugarcane",
    "उस्म्याच्या": "Sugarcane",
    "उस्म्याचे": "Sugarcane",
    "ईख": "Sugarcane",
    "गव्हा": "Wheat",
    "गहू": "Wheat",
    "कापसा": "Cotton",
    "ज्वारीच": "Jowar",
    "उसा": "Sugarcane",
    "ऊसा": "Sugarcane",
    "गन्न": "Sugarcane",
    "शेंगदाण्या": "Groundnut",
    "भुईमुगा": "Groundnut",
    "भुईमुगाच": "Groundnut",
    "मूंगफली": "Groundnut",
    "cotton": "Cotton",
    "कपास": "Cotton",
    "कापूस": "Cotton",
    "कपाशी": "Cotton",
    "groundnut": "Groundnut",
    "peanut": "Groundnut",
    "ground nut": "Groundnut",
    "मूंगफली": "Groundnut",
    "मूँगफली": "Groundnut",
    "मुंगफली": "Groundnut",
    "शेंगदाणा": "Groundnut",
    "भुईमूग": "Groundnut",
}

_RECOMMENDED_HINTS = (
    "recommend", "recommended", "best fit", "top crop", "suggested",
    "शिफारस", "सुझा", "सिफारिश", "सर्वोत्तम", "सबसे उपयुक्त",
)
_TARGET_HINTS = (
    "target", "selected crop", "chosen crop", "i selected", "i chose",
    "लक्ष्य", "निवडलेली", "चुनी हुई", "चुनी हुयी",
)
_GROWN_HINTS = (
    "grew", "grown", "cultivated", "actually grew",
    "लागवड", "उगाया", "पिकवले", "वाढवले",
)


def extract_mentioned_crop(text):
    """Return a supported crop named in the user's message, or None.

    Matches English, Hindi and Marathi names, including inflected forms
    such as उस्म्याच्या / ऊसाच्या for Sugarcane.
    """
    if not text:
        return None

    lowered = text.casefold()
    matches = []
    for alias, crop in sorted(CROP_ALIASES.items(), key=lambda item: -len(item[0])):
        if _DEVANAGARI.search(alias):
            if alias in text:
                matches.append((len(alias), crop))
        else:
            if re.search(rf"\b{re.escape(alias)}\b", lowered):
                matches.append((len(alias), crop))

    if matches:
        matches.sort(reverse=True)
        return matches[0][1]
    return None


def _has_any(text, phrases):
    lowered = (text or "").casefold()
    return any(phrase in lowered or phrase in (text or "") for phrase in phrases)


def crop_role_from_message(text):
    """Which crop role the question is about, independent of a named crop."""
    if _has_any(text, _GROWN_HINTS):
        return "grown"
    if _has_any(text, _TARGET_HINTS):
        return "target"
    if _has_any(text, _RECOMMENDED_HINTS):
        return "recommended"
    return None


def normalize_lang(lang):
    # No preference given at all (None, "", omitted) means "figure it out
    # from what the user typed" — NOT "force English". Forcing English here
    # would make resolve_language() below always return "en" for any
    # caller that doesn't explicitly pass lang="auto", silently breaking
    # auto-detection for every message.
    if not lang:
        return "auto"
    lang = str(lang).strip().lower()
    if lang in ("auto", "detect"):
        return "auto"
    if lang in ("hindi", "hin", "hi"):
        return "hi"
    if lang in ("marathi", "mar", "mr"):
        return "mr"
    if lang in ("english", "eng", "en"):
        return "en"
    return "auto"


def detect_language(text, fallback="en"):
    """Detect en / hi / mr from script and distinctive words."""
    if not text:
        return fallback

    devanagari_count = len(_DEVANAGARI.findall(text))
    latin_count = len(_LATIN.findall(text))

    if devanagari_count == 0:
        return "en"
    if latin_count > devanagari_count * 2:
        return "en"

    mr_score = sum(1 for word in _MARATHI_MARKERS if word in text)
    hi_score = sum(1 for word in _HINDI_MARKERS if word in text)

    if mr_score > hi_score:
        return "mr"
    if hi_score > mr_score:
        return "hi"

    # Default Devanagari without clear markers to Hindi.
    return fallback if fallback in ("hi", "mr") else "hi"


def resolve_language(user_message, preferred="auto"):
    preferred = normalize_lang(preferred)
    if preferred in SUPPORTED_LANGS:
        return preferred
    return detect_language(user_message, fallback="en")

_YIELD_WORDS = (
    "yield", "production", "harvest", "output", "tonnes", "tons per",
    "उत्पादन", "उत्पन्न", "उपज", "पैदावार", "उतारा", "उत्पादकता",
)


def is_yield_question(text):
    """True when the message is plainly asking about yield/production."""
    lowered = (text or "").casefold()
    return any(word in lowered or word in (text or "") for word in _YIELD_WORDS)

