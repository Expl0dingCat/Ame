import requests
import pyaudio
import wave
import keyboard
import os
import shlex

# If the client and server are running locally, set this to True
local = True
base_url = 'http://127.0.0.1:5440'

def generate_response(input: str):
    return requests.post(f'{base_url}/api/v1/generate', json={'input': input})

def listen_response(input: str):
    if local:
        return requests.post(f'{base_url}/api/v1/listen', json={'input': input})
    else:
        with open(input, 'rb') as f:
            file = {'file': f}
        return requests.post(f'{base_url}/api/v1/listen', json={'input': 'file'}, files=file)

def speak_response(input: str):
    if local:
        return requests.post(f'{base_url}/api/v1/full', json={'input': input})
    else:
        request = requests.post(f'{base_url}/api/v1/speak', json={'input': input})
        with open('speak_out_audio.wav', 'wb') as f:
            f.write(request.content)
        return request, os.path.abspath('speak_out_audio.wav')

def full_response(input: str):
    if local:
        return requests.post(f'{base_url}/api/v1/full', json={'input': input})
    else:
        with open(input, 'rb') as f:
            file = {'file': f}
        request = requests.post(f'{base_url}/api/v1/full', json={'input': 'file'}, files=file)
        with open('out_audio.wav', 'wb') as f:
            f.write(request.content)
        return request.json(), os.path.abspath('out_audio.wav')

def send_command(input: str):
    return requests.post(f'{base_url}/api/v1/command', json={'input': input})

def record_voice():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = 'output.wav'

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
        user = response[0]
        ame = response[1]

        print(f'USER: {user}')
        print(f'AME: {ame}')

if __name__ == '__main__':
    inmth = input('Select an input (voice/text/cmd): ')
    if inmth == 'voice':
        print('initiating voice input...')
        pipe()
        print('Ready, press V to speak.')
    elif inmth == 'text':
        while True:
            intxt = input('USER: ')
            response = generate_response(intxt)
            response = response.json()
            print(f'AME: {response}')
    elif inmth == 'cmd':
        print('DANGER ZONE: This is for running commands on the server. Use with caution.\n\nSupported commands:\neval <input>: evaluates python code the server\n')
        while True:
            intxt = input('CMD >> ')
            cmdargs = shlex.split(intxt)
            if cmdargs[0] == 'exit':
                exit(0)
            elif cmdargs[0] == 'eval':
                try:
                    print(send_command(cmdargs[1]))
                except requests.exceptions.ConnectionError:
                    print(f'Cannot connect to server: {base_url}')      
    else:
        print('Invalid input method.')


