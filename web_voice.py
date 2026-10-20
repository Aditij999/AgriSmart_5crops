"""Browser-based voice input/output for the Streamlit website.

Mirrors the mobile app's on-device speech recognition (`speech_to_text`) and
text-to-speech (`flutter_tts`, see `mobile/lib/voice/`): everything here runs
in the visitor's own browser via the standard Web Speech API. No audio is
ever sent to the server — only text that was already going to cross the
browser/Python boundary anyway (the typed-or-dictated question, and the
assistant's already-computed reply) does.

`voice_input_component()` is a real bidirectional Streamlit component (see
`web_voice_component/index.html`): the in-browser recognizer hands its
transcript straight back to Python via the normal widget-value mechanism, on
the current page, in place — no page navigation, so it works the same way
regardless of whether it's sitting inside an `st.dialog` or anywhere else.
This replaces an earlier version that wrote the transcript into the page URL
and did a full reload to get it back into Python; that reload closed any
open `st.dialog` before the transcript could be read, which is why voice
input silently went nowhere. The caller drops the returned text into the
same editable field the person types into — dictation fills the box, it
doesn't auto-send — exactly like `mobile/lib/screens/chat_screen.dart`'s
`_onSpeechResult`, so the two clients behave the same way.

`to_plain_text()` mirrors `backend/routers/chat.py`'s `_plain_text` so the
website reads answers aloud the same way the mobile app's `answer_plain`
field does.
"""

import os
import re

import streamlit as st
import streamlit.components.v1 as components

_DECORATION = re.compile(r"[•\-\*]{1,2}\s|[\U0001F300-\U0001FAFF\u2600-\u27BF]")

_COMPONENT_DIR = os.path.join(os.path.dirname(__file__), "web_voice_component")
_voice_component = components.declare_component("voice_input", path=_COMPONENT_DIR)


def to_plain_text(answer: str) -> str:
    """Strips markdown bullets/emoji so text-to-speech reads cleanly.

    Kept in sync with backend/routers/chat.py's `_plain_text`, which builds
    the mobile app's `answer_plain` field.
    """
    stripped = _DECORATION.sub("", answer)
    return re.sub(r"\s+", " ", stripped).strip()


# Reply-language choice -> BCP-47 tag the browser's speech recogniser understands.
SPEECH_LANG = {"en": "en-IN", "hi": "hi-IN", "mr": "mr-IN", "auto": "en-IN"}
_DEVANAGARI = re.compile(r"[\u0900-\u097F]")


def speech_lang_for(lang: str | None) -> str:
    return SPEECH_LANG.get((lang or "auto"), "en-IN")


def tts_lang_for_text(text: str) -> str:
    """Voice for read-aloud: Devanagari text -> Hindi/Marathi voice, else English (India)."""
    if _DEVANAGARI.search(text or ""):
        try:
            from chatbot.language import detect_language
            return {"mr": "mr-IN", "hi": "hi-IN"}.get(detect_language(text, fallback="hi"), "hi-IN")
        except Exception:
            return "hi-IN"
    return "en-IN"


def voice_input_component(key: str, lang: str = "auto"):
    """Renders a mic button; returns freshly dictated text once it arrives,
    else None. Speech recognition runs entirely in the browser; the
    transcript comes straight back through the component's normal return
    value (see `web_voice_component/index.html`) — no audio, and nothing
    routed through the URL or a page reload.

    A component keeps re-returning its last value on every later rerun (a
    button click elsewhere, typing in another field, ...), not just once —
    so a nonce sent alongside the text is what tells a genuinely fresh
    dictation apart from the same result being reported again.
    """
    raw = _voice_component(key=key, lang=speech_lang_for(lang), default=None)
    if not raw:
        return None
    seen_key = f"_voice_seen_{key}"
    if st.session_state.get(seen_key) == raw.get("nonce"):
        return None
    st.session_state[seen_key] = raw.get("nonce")
    return raw.get("text")


def speak_button(text: str, key: str):
    """Renders a Listen/Stop toggle that reads `text` aloud via the browser's
    built-in speech synthesis — the web equivalent of the app's speaker icon
    under each assistant reply. Nothing is sent to any server for this.
    """
    text = (text or "").strip()
    if not text:
        return
    safe_text = (
        text.replace("\\", "\\\\").replace("`", "'").replace("</script>", "<\\/script>")
    )
    components.html(
        f"""
        <button id="speak-btn-{key}" type="button"
          style="border:none;background:none;color:#8C6D3F;font-size:12px;
                 cursor:pointer;padding:2px 0;">🔊 Listen</button>
        <script>
        (function() {{
          const btn = document.getElementById("speak-btn-{key}");
          const text = `{safe_text}`;
          const synth = (window.parent && window.parent.speechSynthesis) || window.speechSynthesis;
          if (!synth) {{
            btn.disabled = true;
            btn.textContent = "Text-to-speech unavailable";
            return;
          }}
          btn.addEventListener("click", function() {{
            if (btn.dataset.speaking === "1") {{
              synth.cancel();
              btn.textContent = "🔊 Listen";
              btn.dataset.speaking = "0";
              return;
            }}
            synth.cancel();
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = "{tts_lang_for_text(text)}";
            utter.rate = 0.95;
            utter.onend = function() {{
              btn.textContent = "🔊 Listen";
              btn.dataset.speaking = "0";
            }};
            utter.onerror = utter.onend;
            synth.speak(utter);
            btn.textContent = "⏹ Stop";
            btn.dataset.speaking = "1";
          }});
        }})();
        </script>
        """,
        height=28,
    )
