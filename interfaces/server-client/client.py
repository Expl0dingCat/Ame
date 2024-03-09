import requests
import pyaudio
import wave
import keyboard
import os
import shlex

# If the client and server are running locally, set this to True
local = False
base_url = 'http://127.0.0.1:6166'  # Update the port to match the server

def generate_response(input: str):
    return requests.post(f'{base_url}/api/v1/generate', json={'input': input})

def listen_response(input: str):
    if local:
        return requests.post(f'{base_url}/api/v1/listen', json={'input': input})
    else:
        with open(input, 'rb') as f:
            file = {'file': f}
            return requests.post(f'{base_url}/api/v1/listen', files=file)

def speak_response(input: str):
    request = requests.post(f'{base_url}/api/v1/speak', json={'input': input})
    if local:
        return request
    else:
        with open('ame_speech.wav', 'wb') as f:
            f.write(request.content)
            return request, os.path.abspath('ame_speech.wav')

def full_response(input: str):
    if local:
        return requests.post(f'{base_url}/api/v1/full', json={'input': input})
    else:
        with open(input, 'rb') as f:
            file = {'file': f}
            request = requests.post(f'{base_url}/api/v1/full', files=file)
        with open('ame_speech.wav', 'wb') as f:
            f.write(request.content)
        return request, os.path.abspath('ame_speech.wav')

def send_command(input: str):
    return requests.post(f'{base_url}/api/v1/command', json={'input': input})

def text_input_response(input: str):
    return requests.post(f'{base_url}/api/v1/text', json={'input': input})

def record_voice():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = 'user_speech.wav'
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=1,
                    frames_per_buffer=CHUNK)
    frames = []
    while True:
        if keyboard.is_pressed('v'):
            while keyboard.is_pressed('v'):
                data = stream.read(CHUNK)
                frames.append(data)
            break
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    full_path = os.path.join(os.getcwd(), WAVE_OUTPUT_FILENAME)
    return str(rf'{full_path}')

def pipe():
    while True:
        input = record_voice()
        response, audio = full_response(input)
        response_data = response.json()
        user = response_data['userinput']
        ame = response_data['output']
        print(f'USER: {user}')
        print(f'AME: {ame}')

if __name__ == '__main__':
    inmth = input('Select an input (voice/text/cmd): ')
    if inmth == 'voice':
        while True:
            try:
                print('initiating voice input... (hold v to record)')
                pipe()
            except Exception as e:
                print(f'Error: {e}')
    elif inmth == 'text':
        while True:
            try:
                intxt = input('USER: ')
                response = text_input_response(intxt)
                response_data = response.json()
                print(f'AME: {response_data["output"]}')
            except Exception as e:
                print(f'Error: {e}')
    elif inmth == 'cmd':
        print('DANGER ZONE: This is for running commands on the server. Use with caution.\n\nSupported commands:\neval <input>: evaluates python code on the server\n')
        while True:
            intxt = input('CMD >> ')
            cmdargs = shlex.split(intxt)
            if cmdargs[0] == 'exit':
                exit(0)
            elif cmdargs[0] == 'eval':
                try:
                    response = send_command(cmdargs[1])
                    print(response.json())
                except requests.exceptions.ConnectionError:
                    print(f'Cannot connect to server: {base_url}')
    else:
        print('Invalid input method.')