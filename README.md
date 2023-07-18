# Ame (雨) Project
Ame is a fully integrated, multi-modal, open-source virtual assistant built to enhance your digital experience. She leverages the power of a custom fine-tuned* 13 billion parameter LLaMA model to provide personalized and intuitive interaction.

## Disclaimer ⚠️
Ame is in an incomplete state and is being developed by me and only me, expect progress to be slow, refer to the **[progress](#progress-v1)** section of the readme for more information. 

## Overview 📖
- **[Key features 🚀](#key-features-)**
- **[Usage 💻](#usage-%EF%B8%8F)**
- **[Development progress 🚧](#progress-v1)**
- **[About Ame 💧](#the-meaning-behind-ame-)**
- **[Contributing 🤝](#contributing-)**
- **[Acknowledgements 🙏](#acknowledgements-)**
- **[License ⚖️](#license-%EF%B8%8F)**

## Key features 🚀
**Customizable Modules**: Ame's modular design allows for easy customization and extensibility. Each module serves a specific function, such as managing calendars, providing weather updates, or assisting with personal tasks—Ame adapts to you. Developers can create their own modules or modify existing ones to tailor Ame's capabilities to their specific requirements.

**Text-to-Speech (TTS) and Speech-to-Text (STT)**: Ame's TTS and STT capabilities enable natural and effortless communication. STT is powered by OpenAI's whisper.

**Telegram Integration**: Ame seamlessly integrates with Telegram, allowing you to interact with her through text-based messaging and voice notes. Telegram provides a familiar and convenient way to interact with Ame, enabling efficient communication and access to her full range of functionalities.

**Open-Source**: Ame is entirely open-source. This allows for knowledge sharing and the continuous improvement of Ame while contributing to the open-source community and democratizing ML research in the process.

**Locally Run and Privacy-Focused**: Ame prioritizes user privacy and data control by operating entirely on the user's local machine.

**Long-term Memory**: Ame utilizes a vector database that optimizes memory storage and retrieval, enabling Ame to access data that goes beyond the context limit of her model.

## Usage ⚙️

### Install requirements
```bash
pip3 install sentence-transformers
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
set CMAKE_ARGS="-DLLAMA_CUBLAS=on"
set FORCE_CMAKE=1
pip3 install llama-cpp-python --no-cache-dir
pip3 install openai-whisper
pip3 install pyaudio
pip3 install aiohttp
pip3 install keyboard
pip3 install transformers
pip3 install git+https://github.com/suno-ai/bark.git
```
- You must use torch (and its associated packages) version 2.0.0+ or it will break
- Ame was designed on Python 3.10.11


### Server/client
Move `server.py` (interfaces/server-client/) to the root folder then run:
```bash
python server.py
```

To access the server locally make sure `Local = True` in `client.py` (interfaces/server-client/), to access it externally, modify the base URL and set `Local = False`, then run:
```bash
python client.py
```

### API
Create a Python file in the root folder:

```py
from controller import controller

# Initialize the controller, see controller.py for documentation
controller = controller()

# Generate text based on the input "Hello, World!"
response = controller.generate_response("Hello, World!")
```
For a more advanced example, see `server.py`.

## Progress (`v1`)
🔴 Planned
🟡 In progress
🟢 Finished

### Core

Component                     | Status 
----------------------------- | -----
Speech-to-text                |  🟢
Text-to-speech                |  🟢
Vision system                 |  🟡
Long-term memory              |  🟢
Primary controller            |  🟢
Module handler                |  🟡
Server/client interface       |  🟢
Client UI                     |  🔴
Telegram interface            |  🔴

### Modules

Module                        | Status 
----------------------------- | -----
Module SDK                    |  🟡
Weather                       |  🔴
Google Calendar               |  🔴
News                          |  🔴
DeepL                         |  🔴
Shell                         |  🔴

### Fine-tuning LLaMA
I am currently waiting for the second version of LLaMA to train Ame.

Step                          | Status 
----------------------------- | -----
Planning                      |  🔴
Dataset                       |  🔴
Training method               |  🔴
Hardware acquisition          |  🔴
Training                      |  🔴

## Plans for `v2` 🔵
As `v1` is still in development, this section is subject to volatile change, it currently contains features I wanted to include in `v1` but don't have time as well as brand new _concepts_ that may or may not be implemented. If you would like to suggest features for `v2`, please feel free to contact me.
- Voice identification
- Web UI
- Passive listening 

## The meaning behind "Ame" 💧
The name "Ame" originates from the Japanese word "雨" (pronounced ah-meh), which translates to "rain" in English. Like rain, Ame represents a refreshing and nourishing presence in your digital life. Just as raindrops bring life to the earth, Ame breathes life into your digital environment, providing support and efficiency.

By choosing the name Ame, I aim to embody the qualities of adaptability, and revitalization, that rain symbolizes. I hope that Ame can be the reliable companion that brings a refreshing experience to your daily digital interactions.

## Contributing 🤝
If you would like to contribute to the Ame project, please contact me.

## Acknowledgements 🙏
Ame relies on 3rd party open source software to function, this project would not have been possible without:

- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) - LLaMA GGML inference
- [HyperDB](https://github.com/jdagdelen/hyperDB) - Long term memory vector DB
- [Whisper](https://github.com/openai/whisper) and [Bark](https://github.com/suno-ai/bark) - Speech-to-text and text-to-speech
- [LLaMA](https://github.com/facebookresearch/llama) - Base LLM

## License ⚖️
Ame is released under the GNU General Public License v3, which allows you to use, modify, and distribute the software freely. Please refer to the [license file](https://github.com/Expl0dingCat/ame/blob/main/LICENSE) for more details.

## Footnotes
*likely via QLoRA, TBD, I am currently waiting on the second version of LLaMA.
