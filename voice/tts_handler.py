import nltk
import numpy as np
import os
from bark.generation import generate_text_semantic, preload_models
from bark.api import semantic_to_waveform
from bark import SAMPLE_RATE
from scipy.io.wavfile import write as write_wav

# Almost all of this is stolen from the Bark repo.

class tts:
    def __init__(self, model_name='v2/en_speaker_9', temperature=0.6) -> None:
        self.model = model_name
        self.temp = temperature
        preload_models()
        
    def generate(self, prompt):
        GEN_TEMP = self.temp
        SPEAKER = self.model
        sentences = nltk.sent_tokenize(prompt)
        silence = np.zeros(int(0.25 * SAMPLE_RATE))

        pieces = []
        for sentence in sentences:
            semantic_tokens = generate_text_semantic(
                sentence,
                history_prompt=SPEAKER,
                temp=GEN_TEMP,
                min_eos_p=0.05, 
            )

            audio_array = semantic_to_waveform(semantic_tokens, history_prompt=SPEAKER,)
            pieces += [audio_array, silence.copy()]

        audio_array = np.concatenate(pieces)
        write_wav('ame_speech.wav', SAMPLE_RATE, audio_array)
        return os.path.abspath('ame_speech.wav')

if __name__ == '__main__':
    print('This is a handler, it is not meant to be run directly.')
    pass
