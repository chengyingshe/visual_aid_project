import _init_path
from keyword_recognition.utils import *

def keyword_recognition():
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=parameters['model']['zh'],
        lm=parameters['keyword_zh']['lm'],
        dic=parameters['keyword_zh']['dic']
    )
    for phrase in speech:
        if str(phrase) in parameters['keyword_zh']['keywords'].keys():
            print(f"keyword: {phrase}")
            
keyword_recognition()