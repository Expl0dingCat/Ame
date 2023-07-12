import os
from aiohttp import web
from controller import controller

# Initialize controller, None will use defualt values
controller = controller(verbose=True, # Print to stdout
                        log=True, # Log to controller.log
                        memory_path=None, # Path to memory db (pickle.gz)
                        language_model_path=None, # Path to language model (GGML)
                        speech_to_text_model='base.en', # Speech-to-text model
                        text_to_speech_model_path='path/to/tts_model', # Text-to-speech model (path)
                        max_tokens=128, # Max tokens to generate
                        temperature=0.85, # Temperature (0.0-1.0)
                        use_gpu=True, # Use GPU
                        context_limit=2048, # Context limit of the model
                        virtual_context_limit=1024, # Point where short term memory drops earliest memory (long term memory persists)
                        debug=False # Debug mode (testing only)
                        )

async def handle_generate(request):
    response = await request.json()
    input = response['input']
    response = controller.generate_response(input)
    return web.json_response(response)

async def handle_listen(request):
    if request.content_type == 'multipart/form-data':
        reader = await request.multipart()
        field = await reader.next()
        with open('speech.mp3', 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                f.write(chunk)
        response = controller.listen(os.path.abspath(f.name))
        return web.json_response(response)
    else:
        response = await request.json()
        input = response['input']
        response = controller.listen(input)
        return web.json_response(response)

async def handle_speak(request):
    response = await request.json()
    input = response['input']
    response = controller.speak(input)
    return web.json_response(response)

async def handle_full(request):
    if request.content_type == 'multipart/form-data':
        reader = await request.multipart()
        field = await reader.next()
        with open('speech.mp3', 'wb') as f:
            while True:
                chunk = await field.read_chunk()
                if not chunk:
                    break
                f.write(chunk)
        response = controller.full_pipeline(os.path.abspath(f.name))
        return web.json_response(response)
    else:
        response = await request.json()
        input = response['input']
        response = controller.full_pipeline(input)
        return web.json_response(response)

async def handle_command(request):
    response = await request.json()
    input = response['input']
    if input == 'None':
        return web.json_response({'response': 'No command provided.'})
    response = controller.evaluate(input)
    return web.json_response(response)

app = web.Application()
app.add_routes([web.post('/api/v1/full', handle_full)])
app.add_routes([web.post('/api/v1/generate', handle_generate)])
app.add_routes([web.post('/api/v1/listen', handle_listen)])
app.add_routes([web.post('/api/v1/speak', handle_speak)])
app.add_routes([web.post('/api/v1/command', handle_command)])

if __name__ == '__main__':
    web.run_app(app, port=5440, host='127.0.0.1')
