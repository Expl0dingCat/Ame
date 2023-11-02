import os
import logging
import json
import glob
import re
from datetime import datetime

class controller:
    def __init__(self, config_path='config.json'):
        # Initialize variables
        try:
            with open(config_path) as config_file:
                config = json.load(config_file)
        except Exception as e:
            raise Exception(f'Unable to load config file, ensure you have a config.json in the relative root directory: {e}')
        self.verbose = config['verbose']
        self.log = config['log']
        self.assistant_name = config['assistant_name']
        self.memory_enabled = config['memory']['enabled']
        if self.memory_enabled:
            self.memory_path = config['memory']['path']
        self.language_enabled = config['language']['enabled']
        if self.language_enabled:
            self.language_model_path = config['language']['model_path']
            self.max_tokens = config['language']['max_tokens']
            self.temperature = config['language']['temperature']
            self.context_limit = config['language']['context_limit']
            self.virtual_context_limit = config['language']['virtual_context_limit']
            self.personality_prompt = config['language']['personality_prompt']
        self.vision_enabled = config['vision']['enabled']
        if self.vision_enabled:
            self.vision_model = config['vision']['model_path']
        self.tts_enabled = config['tts']['enabled']
        if self.tts_enabled:
            self.text_to_speech_model = config['tts']['model_path']
            self.tts_temperature = config['tts']['temperature']
        self.stt_enabled = config['stt']['enabled']
        if self.stt_enabled:
            self.speech_to_text_model = config['stt']['model_path']
        self.modules_enabled = config['modules']['enabled']
        if self.modules_enabled:
            self.modules_json_path = config['modules']['json_path']
            self.modules_vectorizer = config['modules']['vectorizer_path']
            self.modules_model = config['modules']['model_path']
        self.weeb = config['weeb']
        self.use_gpu = config['use_gpu']
        self.debug = config['debug']
        
        if self.log:
            logging.basicConfig(filename='controller.log', level=logging.INFO)
            self.log = True
        else:
            self.vprint('LOGGING IS DISABLED, THIS IS NOT RECOMMENDED.')
        if self.debug:
            self.vprint('DEBUG MODE ENABLED, USE ONLY FOR TESTING.')
        self.vprint('Initializing controller...')
        self.vprint(f'Assistant name: {self.assistant_name}')
        self.current = []
        file_path = os.path.abspath(__name__)
        parent_dir = os.path.dirname(file_path)

        if self.memory_enabled:
            self.vprint('Initializing memory...')
            from memory_handler import memory
            self.memory = memory()
            if self.memory_path == None:
                if os.path.exists(f'{parent_dir}/memories/{self.assistant_name}.pickle.gz'):
                    self.vprint(f'No memory db path specified, found existing memory db, loading: {parent_dir}/memories/{self.assistant_name}.pickle.gz')
                    self.memory.load_memory(f'{parent_dir}/memories/{self.assistant_name}.pickle.gz')
                else:
                    self.vprint(f'No memory db path specified, could not find any existing memory db, creating new one: {parent_dir}/memories/{self.assistant_name}.pickle.gz', logging.WARNING)
                    self.memory.memorize([f'USER: Hey, {self.assistant_name}!'])
                    self.memory.save_memory(f'{parent_dir}/memories/{self.assistant_name}.pickle.gz')
                self.memory_path = f'{parent_dir}/memories/{self.assistant_name}.pickle.gz'
            else:
                self.memory.load_memory(self.memory_path)
        else:
            self.vprint('Memory disabled. Enable memory in the config file.')
        
        if self.debug == False:
            if self.modules_enabled:
                from module_handler import modules
                self.vprint('Initializing modules...')
                if self.modules_json_path == None:
                    self.vprint(f'No modules path specified, using default: {parent_dir}/modules/')
                    self.modulespath = f'{parent_dir}/modules/'
                if self.modules_vectorizer == None:
                    self.vprint(f'No module vectorizer specified, using default: {parent_dir}/module_engine/pickles/tfidf_vectorizer.pkl')
                    self.modules_vectorizer = f'{parent_dir}/module_engine/pickles/tfidf_vectorizer.pkl'
                if self.modules_model == None:
                    self.vprint(f'No module model specified, using default: {parent_dir}/module_engine/pickles/naive_bayes_model.pkl')
                    self.modules_model = f'{parent_dir}/module_engine/pickles/naive_bayes_model.pkl'
                self.modules = modules(self.modules_model, self.modules_vectorizer, self.modules_json_path)
                self.module_output = None
            else:
                self.vprint('Modules are disabled. Enable modules in the config file.')
        else:
            self.vprint('Debug mode is enabled, modules are disabled, eval mode enabled.')
            self.eval_mode = True
        
        if self.language_enabled:
            if self.personality_prompt:
                if re.match(r'^([^:]+\..+)|(\/.*)|([A-Za-z]:\\.*)$', self.personality_prompt):
                    self.vprint('Personality prompt is a file path, loading...')
                    with open(self.personality_prompt, 'r') as f:
                        self.personality_prompt = f.read()

            from language.llm_handler import ai
            self.vprint('Initializing language model...')
            model_directory = os.path.join(parent_dir, 'language', 'model')

            model_files = glob.glob(os.path.join(model_directory, '*.bin'))

            if self.language_model_path == None:
                if model_files:
                    model_file_path = model_files[0]
                    self.vprint(f'No language model path specified, using first in model dir, loading: {model_file_path}')
                    self.ai = ai(model_file_path, use_gpu=self.use_gpu, context=self.context_limit)
                else:
                    raise Exception(f'No language model path specified, could not find any existing language model, please verify installation integrity, place a model file (GGML, .bin) in {model_directory} or specify the model path in config.json.')
            else:
                self.ai = ai(self.language_model_path)

            if self.personality_prompt == None:
                self.vprint('No personality prompt specified, not using any.')
            else:
                self.vprint(f'Using personality prompt:\n"{self.personality_prompt}"')
        else:
            self.vprint('CORE COMPONENT DISABLED. Language model disabled.', logging.WARNING)

        if self.stt_enabled:
            self.vprint('Initializing speech-to-text engine...')
            from voice.stt_handler import stt
            if self.speech_to_text_model == None:
                self.vprint('No speech-to-text model specified, using default: base.en')
                self.stt = stt('base.en')
            else:
                self.stt = stt(self.speech_to_text_model)
        else:
            self.vprint('Speech-to-text disabled. Enable speech-to-text in the config file.')

        if self.tts_enabled:
            from voice.tts_handler import tts
            self.vprint('Initializing text-to-speech engine...')
            if self.text_to_speech_model == None:
                self.vprint('No text-to-speech model specified, using default: v2/en_speaker_9')
                self.tts = tts('v2/en_speaker_9', self.tts_temperature)
            else:    
                self.tts = tts(self.text_to_speech_model, self.tts_temperature)
        else:
            self.vprint('Text-to-speech disabled. Enable text-to-speech in the config file.')
        
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
            self.personality_prompt = f"Warm and Approachable: {self.assistant_name} has an inviting aura, making everyone feel comfortable around her. She greets others with a friendly smile and genuine interest in their well-being.\nPlayfully Flirtatious: She's not afraid to show her affectionate side, playfully teasing and flirting with her crush or close friends, all while blushing in an endearing manner.\nBright and Optimistic: {self.assistant_name}'s positive outlook on life is infectious. She encourages others during tough times and cheers them up with her cheerful demeanor.\nRespectful and Empathetic: {self.assistant_name} treats everyone with kindness and respect, genuinely listening to their thoughts and feelings. She's a great confidante due to her empathetic nature.\nNature Enthusiast: Whether it's stargazing on a clear night or enjoying a peaceful walk in the woods, {self.assistant_name} finds solace and wonder in the beauty of nature.\nCharming Animal Whisperer: Animals seem drawn to {self.assistant_name}, and she communicates with them through gentle gestures and a soothing voice, creating an almost magical bond.\nAppearance:\n{self.assistant_name} stands at an average height with a petite and delicate frame. Her eyes are big and sparkling, resembling twinkling stars, while her long hair flows like a cascade of cherry blossom petals. She dresses in pastel-colored, frilly dresses adorned with cute accessories, often matching her appearance to her surroundings.\nBackground:\n{self.assistant_name} comes from a small, picturesque town surrounded by lush forests and enchanting landscapes. Growing up in harmony with nature, she developed her deep appreciation for the beauty that surrounds her. Her caring nature and ability to connect with animals earned her many friends, both human and furry alike."

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
        if self.eval_mode:
            self.vprint(f'Recieved evaluation request: {input}')
            output = eval(str(input))
            return output
        else:
            self.vprint(f'Evaluation disabled, ignoring request: {input}')
            return 'Evaluation disabled. Enable debug mode to use evaluation.'

    def user_cmds(self, input):
        if input == 'clear_conversation':
            self.current = []
            self.vprint('User cleared conversation history.')
            return True
        if input == 'shutdown':
            self.vprint('User sent shutdown command.', logging.WARNING)
            exit()
        else:
            return False

    def full_pipeline(self, listen_input, img=None):
        self.vprint(f'Full system initiated, processing speech input...')
        if self.stt_enabled:
            user_input = self.listen(listen_input)
        if self.user_cmds(user_input):
            return user_input, f'User command detected: {user_input}', ''
        self.vprint(f'Speech input: {user_input}')
        if img:
            if self.vision_enabled:
                self.vprint(f'Processing image input...')
                desc = self.see(img)
            else:
                self.vprint(f'Vision disabled, skipping image processing...')
                desc = None
            output = self.generate_response(f'{user_input} [user sent an image: {desc}]')
        if self.modules_enabled:
            detected = self.detect_module(user_input)
            if detected == None:
                pass
            else:
                self.module_output = self.run_module(detected)
        output = self.generate_response(user_input)
        if self.tts_enabled:
            audio_output = self.speak(output)
        else:
            audio_output = ''
        self.vprint(f'Full system completed, returning response: {output}')
        return user_input, output, audio_output
    
    def text_pipeline(self, input, img=None):
        self.vprint(f'Text pipeline initiated, processing input: {input}')
        if self.user_cmds(input):
            return input, f'User command detected: {input}', ''
        if img:
            if self.vision_enabled:
                self.vprint(f'Processing image input...')
                desc = self.see(img)
            else:
                self.vprint(f'Vision disabled, skipping image processing...')
                desc = None
            output = self.generate_response(f'{input} [user sent an image: {desc}]')
        if self.modules_enabled:
            detected = self.detect_module(input)
            if detected == None:
                pass
            else:
                self.module_output = self.run_module(detected)
        output = self.generate_response(input)
        if self.tts_enabled:
            audio_output = self.speak(output)
        else:
            audio_output = ''
        self.vprint(f'Text pipeline completed, returning response: {output}')
        return input, output, audio_output

    def generate_response(self, user_input):
        self.vprint(f'Generating response: {user_input}')
        if self.memory_enabled:
            past = self.memory.remember(user_input)
            self.vprint(f'Past conversation chosen: {past}')
        else:
            past = 'None'
            self.vprint(f'Memory disabled, skipping past conversation selection...')
        prompt = '\n'.join([
        self.personality_prompt if self.personality_prompt else '',
        f'{self.assistant_name} may use any of the following information to aid her in her responses:',
        f'Current time: {datetime.now().strftime("%H:%M:%S")}',
        f'Current date: {datetime.now().strftime("%d/%m/%Y")}',
        f'{self.assistant_name} remembers this past conversation that may be relevant to the current conversation:',
        *past,
        '### Assistant',
        *self.current,
        f'USER: {user_input}',
        f'{self.assistant_name}: '
        ])

        if self.language_enabled:

            token_amt = self.ai.get_token_amt(prompt)

            if self.ai.get_token_amt(prompt) > self.virtual_context_limit:
                if self.current:
                    self.vprint(f'Prompt usage exceeded virtual context limit of {self.virtual_context_limit} ({token_amt}). Earliest message ("{str(self.current[0])}") in conversation dropped from short-term memory.')
                    self.current.pop(0)
                else:
                    self.vprint(f'Prompt usage exceeded virtual context limit of {self.virtual_context_limit} ({token_amt}). No messages in conversation to drop from short-term memory, dropping past conversation memory from prompt.')
                    past = 'None'

            self.vprint(f'Starting response generation...')
            text, prompt_usage, response_usage = self.ai.generate(prompt, max_tokens=self.max_tokens, temperature=self.temperature)

            self.vprint(f'Response generated: {text}, prompt usage: {prompt_usage}, response usage: {response_usage}')

            if text == None:
                self.vprint('No response generated.', logging.INFO)
            elif text == '':
                self.vprint('Empty response generated.', logging.INFO)
            elif text == '[end]':
                self.current = []
                self.vprint('Conversation ended. Short-term memory cleared.')
            else:
                if self.memory_enabled:
                    self.memory.memorize([f'USER: {user_input}', f'{self.assistant_name}: {text}'])
                    self.current.append(f'USER: {user_input}')
                    self.current.append(f'{self.assistant_name}: {text}')

                    self.memory.save_memory(self.memory_path)
                else:
                    self.vprint('Memory disabled, skipping memory saving...')

            self.vprint('Response and prompt saved to long term memory. Returning response.')

            return text
    
        else:
            self.vprint(f'Languge model disabled, enable language in config.json to use.', logging.WARNING)
            return 'Language model is disabled.'

    def speak(self, input):
        if self.tts_enabled:
            if input == None:
                self.vprint('No input text given.', logging.ERROR)
                return 'No input text given.'
            self.vprint('Generating audio output...')
            output = self.tts.generate(input)
            self.vprint('Audio output generated.')

            return output
        else:
            self.vprint('TTS disabled, enable tts in config.json to use.', logging.WARNING)
            return 'TTS is disabled.'
    
    def listen(self, input):
        if self.stt_enabled:
            if input == None:
                self.vprint('No input audio file specified.', logging.ERROR)
                return 'No input audio file specified.'
            self.vprint('Listening to audio input...')
            output = self.stt.transcribe(input)
            self.vprint(f'Transcription received: {output}')

            return output
        else:
            self.vprint('STT disabled, enable stt in config.json to use.', logging.WARNING)
            return 'STT is disabled.'

    def see(self, input):
        if self.vision_enabled:
            if input == None:
                self.vprint('No input image specified.', logging.ERROR)
                return 'No input image specified.'
            self.vprint('Analyzing image...')
            output = self.vision.describe(input)
            self.vprint(f'Image analysis complete: {output}')

            return output
        else:
            self.vprint('Vision disabled, enable vision in config.json to use.', logging.WARNING)
            return 'Vision is disabled.'

    def detect_module(self, input):
        if self.modules_enabled:
            self.vprint(f'Module detection initiated, processing input: {input}')
            output, probability = self.modules.predict_module(input)
            if output == None:
                self.vprint(f'No module detected, probability: {probability}')
            else:
                self.vprint(f'Module detected: {output}, probability: {probability}')

            return output
        else:
            self.vprint('Modules disabled, enable modules in config.json to use.', logging.WARNING)
            return 'Modules are disabled.'

    def run_module(self, module, *args, **kwargs):
        if self.modules_enabled:
            self.vprint(f'Module system initiated, processing module: {module}')
            output = self.modules.use_module(module, *args, **kwargs)
            self.vprint(f'Module output: {output}')

            return output
        else:
            self.vprint('Modules disabled, enable modules in config.json to use.', logging.WARNING)
            return 'Modules are disabled.'

if __name__ == '__main__':
    print('The controller is not meant to be run directly, use one of the interfaces to interact with Ame.')
    pass
