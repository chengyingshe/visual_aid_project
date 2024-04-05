import _init_path
from keyword_recognition.utils import *

def keyword_recognition():
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=parameters['model']['en'],
        lm=parameters['keyword_en']['lm'],
        dic=parameters['keyword_en']['dic']
    )
    for phrase in speech:
        if str(phrase) in parameters['keyword_en']['keywords'].keys():
            print(f"keyword: {phrase}")
            
keyword_recognition()