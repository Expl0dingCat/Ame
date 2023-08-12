import os
import logging
import json
from datetime import datetime

class controller:
    def __init__(self, config_src='config.json', verbose=True, log=True, memory_path=None, language_model_path=None, speech_to_text_model=None, text_to_speech_model=None, tts_temperature=0.6, vision_model=None, max_tokens=128, temperature=0.85, personality_prompt=None, context_limit=2048, virtual_context_limit=1024, weeb=False, use_gpu=True, debug=False):
        # Initialize variables
        with open('config.json') as config_file:
            config = json.load(config_file)
        if config_src == 'config.json':
            self.verbose = config['verbose']
            self.log = config['log']
            self.memory_enabled = config['memory']['enabled']
            if self.memory_enabled:
                self.memory_path = config['memory']['path']
            self.language_enabled = config['language']['enabled']
            if self.language_enabled:
                self.language_model_path = config['language']['model_path']
                self.max_tokens = config['language']['max_tokens']
                self.temperature = config['language']['temperature']
                self.context_limit = config['language']['context_limit']
                self.virtual_context_limit = config['language']['temperature']
                self.personality_prompt = config['language']['personality_prompt']
            self.vision_enabled = config['vision']['enabled']
            if self.vision_enabled:
                self.vision_model = config['vision']['model']
            self.tts_enabled = config['tts']['enabled']
            if self.tts_enabled:
                self.text_to_speech_model = config['tts']['model']
                self.tts_temperature = config['tts']['temperature']
            self.stt_enabled = config['stt']['enabled']
            if self.stt_enabled:
                self.speech_to_text_model = config['stt']['model']
            self.modules_enabled = config['modules']['enabled']
            if self.modules_enabled:
                self.modules = config['modules']['path']
            self.weeb = config['weeb']
            self.use_gpu = config['use_gpu']
            self.debug = config['debug']
        elif config_src == 'var':
            self.memory_enabled = config['memory']['enabled']
            self.language_enabled = config['language']['enabled']
            self.vision_enabled = config['vision']['enabled']
            self.tts_enabled = config['tts']['enabled']
            self.stt_enabled = config['stt']['enabled']
            self.modules_enabled = config['modules']['enabled']
            self.verbose = verbose
            self.log = log
            self.memory_path = memory_path
            self.max_tokens = max_tokens
            self.temperature = temperature
            self.context_limit = context_limit
            self.virtual_context_limit = virtual_context_limit
            self.language_model_path = language_model_path
            self.personality_prompt = personality_prompt
            self.vision_model = vision_model
            self.text_to_speech_model = text_to_speech_model
            self.tts_temperature = tts_temperature
            self.speech_to_text_model = speech_to_text_model
            self.weeb = weeb
            self.use_gpu = use_gpu
            self.debug = debug
        else:
            raise Exception(f'Invalid config source: {config_src}')
            
        if self.log:
            logging.basicConfig(filename='controller.log', level=logging.INFO)
            self.log = True
        else:
            self.vprint('LOGGING IS DISABLED, THIS IS NOT RECOMMENDED.')
        if self.debug:
            self.vprint('DEBUG MODE ENABLED, USE ONLY FOR TESTING.')
        self.vprint(f'Loading configuration from {config_src}')
        self.vprint('Initializing controller...')
        self.current = []
        file_path = os.path.abspath(__name__)
        parent_dir = os.path.dirname(file_path)

        if self.memory_enabled:
            self.vprint('Initializing memory...')
            from memory_handler import memory
            self.memory = memory()
            if self.memory_path == None:
                if os.path.exists(f'{parent_dir}/memories/ame.pickle.gz'):
                    self.vprint(f'No memory db path specified, found existing memory db, loading: {parent_dir}/memories/ame.pickle.gz')
                    self.memory.load_memory(f'{parent_dir}/memories/ame.pickle.gz')
                else:
                    self.vprint(f'No memory db path specified, could not find any existing memory db, creating new one: {parent_dir}/memories/ame.pickle.gz', logging.WARNING)
                    self.memory.memorize(['USER: Hey, Ame!'])
                    self.memory.save_memory(f'{parent_dir}/memories/ame.pickle.gz')
                self.memory_path = f'{parent_dir}/memories/ame.pickle.gz'
            else:
                self.memory.load_memory(self.memory_path)
        else:
            self.vprint('Memory disabled. Renable memory in the config file.')
        
        if self.debug == False:
            if self.modules_enabled:
                from module_handler import modules
                self.vprint('Initializing modules...')
                self.modules = modules()
            else:
                self.vprint('Modules disabled. Renable modules in the config file.')
        else:
            self.vprint('Debug mode is enabled, modules disabled.')
        
        if self.language_enabled:
            from language.llm_handler import ai
            self.vprint('Initializing language model...')
            if self.language_model_path == None:
                if os.path.exists(f'{parent_dir}/language/model/ame.bin'):
                    self.vprint(f'No language model path specified, using default, loading: {parent_dir}/language/model/ame.bin')
                    self.ai = ai(f'{parent_dir}/language/model/ame.bin', use_gpu=self.use_gpu, context=self.context_limit)
                else:
                    self.vprint(f'No language model path specified, could not find any existing language model, please verify installation integrity, place a model file named ame.bin in {parent_dir}/language/model/ or specify the model path in the arguments when initalizing the controller.', logging.ERROR)
                    raise Exception(f'No language model path specified, could not find any existing language model, please verify installation integrity, place a model file named ame.bin in {parent_dir}/language/model/ or specify the model path in the arguments when initalizing the controller.')
            else:
                self.ai = ai(self.language_model_path)
            if self.personality_prompt == None:
                self.vprint('No personality prompt specified, not using any.')
            else:
                self.vprint(f'Using personality prompt:\n"{self.personality_prompt}"')
        else:
            self.vprint('CORE COMPONENT DISABLED. Language model disabled. Ame will not function.', logging.WARNING)

        if self.stt_enabled:
            self.vprint('Initializing speech-to-text engine...')
            from voice.stt_handler import stt
            if self.speech_to_text_model == None:
                self.vprint('No speech-to-text model specified, using default: base.en')
                self.stt = stt('base.en')
            else:
                self.stt = stt(self.speech_to_text_model)
        else:
            self.vprint('Speech-to-text disabled. Renable speech-to-text in the config file.')

        if self.tts_enabled:
            from voice.tts_handler import tts
            self.vprint('Initializing text-to-speech engine...')
            if self.text_to_speech_model == None:
                self.vprint('No text-to-speech model specified, using default: v2/en_speaker_9')
                self.tts = tts('v2/en_speaker_9', self.tts_temperature)
            else:    
                self.tts = tts(self.text_to_speech_model, self.tts_temperature)
        else:
            self.vprint('Text-to-speech disabled. Renable text-to-speech in the config file.')
        
        if self.vision_enabled:
            from vision.vision_handler import vision
            self.vprint('Initializing vision engine...')
            if self.vision_model == None:
                self.vprint('No vision model specified, using default: default vision model')
                self.vision = vision('default vision model')
            else:    
                self.vision = vision(self.vision_model)

        if self.weeb:
            self.vprint('Weeb mode enabled, overriding personality prompt and enabling vtuber.')
            self.personality_prompt = "Warm and Approachable: Ame has an inviting aura, making everyone feel comfortable around her. She greets others with a friendly smile and genuine interest in their well-being.\nPlayfully Flirtatious: She's not afraid to show her affectionate side, playfully teasing and flirting with her crush or close friends, all while blushing in an endearing manner.\nBright and Optimistic: Ame's positive outlook on life is infectious. She encourages others during tough times and cheers them up with her cheerful demeanor.\nRespectful and Empathetic: Ame treats everyone with kindness and respect, genuinely listening to their thoughts and feelings. She's a great confidante due to her empathetic nature.\nNature Enthusiast: Whether it's stargazing on a clear night or enjoying a peaceful walk in the woods, Ame finds solace and wonder in the beauty of nature.\nCharming Animal Whisperer: Animals seem drawn to Ame, and she communicates with them through gentle gestures and a soothing voice, creating an almost magical bond.\nAppearance:\nAme stands at an average height with a petite and delicate frame. Her eyes are big and sparkling, resembling twinkling stars, while her long hair flows like a cascade of cherry blossom petals. She dresses in pastel-colored, frilly dresses adorned with cute accessories, often matching her appearance to her surroundings.\nBackground:\nAme comes from a small, picturesque town surrounded by lush forests and enchanting landscapes. Growing up in harmony with nature, she developed her deep appreciation for the beauty that surrounds her. Her caring nature and ability to connect with animals earned her many friends, both human and furry alike."

        self.vprint('All initialized. Controller ready and on standby.')

    def __call__(self):
        self.vprint('Controller called, re-initializing...')
        self.__init__()

    def vprint(self, print_content, log_type=logging.INFO):
        if self.verbose or self.debug:
            print(f'controller: {print_content}')
        if self.log or self.debug:
            logging.log(log_type, f'controller: {print_content}')
    
    def evaluate(self, input):
        self.vprint(f'Recieved evaluation request: {input}')
        output = eval(str(input))
        return output

    def user_cmds(self, input):
        if input == 'clear_conversation':
            self.current = []
            return True
        if input == 'shutdown':
            self.vprint('User sent shutdown command.', logging.WARNING)
            exit()
        else:
            return False

    def full_pipeline(self, listen_input, img=None):
        self.vprint(f'Full system initiated, processing speech input...')
        user_input = self.listen(listen_input)
        if self.user_cmds(user_input):
            return f"User command detected: {user_input}"
        self.vprint(f'Speech input: {user_input}')
        if img:
            self.vprint(f'Processing image input...')
            desc = self.see(img)
            output = self.generate_response(f'{user_input} [user sent an image: {desc}]')
        output = self.generate_response(user_input)
        audio_output = self.speak(output)
        self.vprint(f'Full system completed, returning response: {output}')
        return user_input, output, audio_output
    
    def text_pipeline(self, input, img=None):
        self.vprint(f'Text pipeline initiated, processing input: {input}')
        if self.user_cmds(input):
            return f"User command detected: {input}"
        if img:
            self.vprint(f'Processing image input...')
            desc = self.see(img)
            output = self.generate_response(f'{input} [user sent an image: {desc}]')
        output = self.generate_response(input)
        audio_output = self.speak(output)
        self.vprint(f'Text pipeline completed, returning response: {output}')
        return input, output, audio_output

    def generate_response(self, user_input):
        self.vprint(f'Generating response: {user_input}')
        past = self.memory.remember(user_input)
        self.vprint(f'Past conversation chosen: {past}')
        prompt = '\n'.join([
        self.personality_prompt if self.personality_prompt else '',
        'Ame may use any of the following information to aid her in her responses:',
        f'Current time: {datetime.now().strftime("%H:%M:%S")}',
        f'Current date: {datetime.now().strftime("%d/%m/%Y")}',
        'Past conversation:',
        *past,
        'Utilities available to Ame, she can use these at any time by placing them at the end of her response:',
        '[end] - Ends the conversation'
        '### Assistant',
        *self.current,
        f'USER: {user_input}',
        'AME:'
        ])

        if self.ai.get_token_amt(prompt) > self.virtual_context_limit:
            self.vprint(f'Prompt usage exceeded virtual context limit of {self.virtual_context_limit} ({prompt_usage}). Earliest message ("{str(self.current[0])}") in conversation dropped from short-term memory.')
            self.current.pop(0)

        self.vprint(f'Starting response generation...')
        text, prompt_usage, response_usage = self.ai.generate(prompt, max_tokens=self.max_tokens, temperature=self.temperature)

        self.vprint(f'Response generated: {text}, prompt usage: {prompt_usage}, response usage: {response_usage}')

        if prompt_usage > self.virtual_context_limit:
            self.current.pop(0)
            self.vprint(f'Prompt usage exceeded virtual context limit of {self.virtual_context_limit} ({prompt_usage}). Earliest message ("{str(self.current[0])}") in conversation dropped from short-term memory.')

        if text == None:
            self.vprint('No response generated.', logging.WARNING)
        elif text == '[end]':
            self.current = []
            self.vprint('Conversation ended. Short-term memory cleared.')
        else:
            self.memory.memorize([f'USER: {user_input}', f'AME: {text}'])
            self.current.append(f'USER: {user_input}')
            self.current.append(f'AME: {text}')

        self.memory.save_memory(self.memory_path)

        self.vprint('Response and prompt saved to long term memory. Returning response.')

        return text

    def speak(self, input):
        if input == None:
            self.vprint('No input text given.', logging.ERROR)
            return "No input text given."
        self.vprint('Generating audio output...')
        output = self.tts.generate(input)
        self.vprint('Audio output generated.')

        return output
    
    def listen(self, input):
        if input == None:
            self.vprint('No input audio file specified.', logging.ERROR)
            return "No input audio file specified."
        self.vprint('Listening to audio input...')
        output = self.stt.transcribe(input)
        self.vprint(f'Transcription received: {output}')

        return output

    def see(self, input):
        if input == None:
            self.vprint('No input image specified.', logging.ERROR)
            return "No input image specified."
        self.vprint('Analyzing image...')
        output = self.vision.describe(input)
        self.vprint(f'Image analysis complete: {output}')

        return output

    def run_module(self, module, *args, **kwargs):
        self.vprint(f'Module system initiated, processing module: {module}')
        output = self.modules.use_module(module, *args, **kwargs)
        self.vprint(f'Module output: {output}')

        return output

if __name__ == '__main__':
    print('The controller is not meant to be run directly, use one of the interfaces to interact with Ame.')
    pass
