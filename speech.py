import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    try:
        with microphone as source:
            # recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source,timeout=3)
    except sr.WaitTimeoutError:
        response["success"] = False
        response['error'] = "Please speak in the mic, no audio was identified"
        return response

    #try recognizing the speech in the recording
    #if a RequestError or UnknownValueError exception is caught,
    #    update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response