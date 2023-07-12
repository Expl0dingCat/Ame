import whisper

class stt:
    def __init__(self, model_name=None) -> None:
        if model_name == None:
            self.load_model()
        else:
            self.load_model(model_name)

    def load_model(self, model_name="small.en"):
        self.model = whisper.load_model(model_name)
    
    def transcribe(self, audio_path):
        print(audio_path)
        result = self.model.transcribe(audio_path)
        return result["text"]
    
if __name__ == '__main__':
    print('This is a handler, it is not meant to be run directly.')
    pass