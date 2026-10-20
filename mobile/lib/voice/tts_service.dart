import 'package:flutter/foundation.dart';
import 'package:flutter_tts/flutter_tts.dart';

/// Device text-to-speech for chatbot answers.
///
/// One utterance at a time: starting a new one stops the previous. No network
/// call is involved — the text spoken is the `answer_plain` already returned by
/// the backend.
class TtsService extends ChangeNotifier {
  TtsService({FlutterTts? tts}) : _tts = tts ?? FlutterTts();

  final FlutterTts _tts;
  bool _configured = false;
  String? _speakingId;
  String? _error;

  /// Identifier of the message currently being spoken, if any.
  String? get speakingId => _speakingId;

  bool get isSpeaking => _speakingId != null;

  /// Last failure message, cleared when a new utterance starts.
  String? get error => _error;

  bool isSpeakingMessage(String id) => _speakingId == id;

  Future<void> _configure() async {
    if (_configured) return;
    _tts.setCompletionHandler(() => _finish());
    _tts.setCancelHandler(() => _finish());
    _tts.setErrorHandler((dynamic message) {
      _finish(error: message?.toString() ?? 'Text-to-speech failed.');
    });
    await _tts.awaitSpeakCompletion(true);
    await _tts.setLanguage('en-US');
    await _tts.setSpeechRate(0.45);
    await _tts.setPitch(1.0);
    _configured = true;
  }

  /// Speaks [text] on behalf of the message identified by [id].
  Future<void> speak(String id, String text) async {
    final speech = text.trim();
    _error = null;
    if (speech.isEmpty) {
      _error = 'Nothing to read out for this response.';
      notifyListeners();
      return;
    }
    try {
      await _configure();
      if (_speakingId != null) await _tts.stop();
      _speakingId = id;
      notifyListeners();
      await _tts.speak(speech);
      // `awaitSpeakCompletion(true)` makes this return once playback ends; the
      // completion handler may not fire on every platform.
      if (_speakingId == id) _finish();
    } catch (failure) {
      _finish(error: 'Text-to-speech is unavailable on this device.');
      debugPrint('TTS speak failed: $failure');
    }
  }

  Future<void> stop() async {
    if (_speakingId == null) return;
    try {
      await _tts.stop();
    } catch (failure) {
      debugPrint('TTS stop failed: $failure');
    }
    _finish();
  }

  void _finish({String? error}) {
    if (_speakingId == null && error == null) return;
    _speakingId = null;
    if (error != null) _error = error;
    notifyListeners();
  }

  @override
  void dispose() {
    _tts.stop();
    super.dispose();
  }
}
