# Ame (あめ) Project
Ame is a fully integrated, open-source virtual assistant built to enhance your digital experience. She leverages the power of a custom fine-tuned 13 billion parameter LLaMA model to provide personalized and intuitive interaction.

## Key features 
**Customizable Modules**: Ame's modular design allows for easy customization and extensibility. Each module serves a specific function, such as managing calendars, providing weather updates, or assisting with personal tasks—Ame adapts to you. Developers can create their own modules or modify existing ones to tailor Ame's capabilities to their specific requirements.

**Text-to-Speech (TTS) and Speech-to-Text (STT)**: Ame's TTS and STT capabilities enable natural and effortless communication. STT is powered by OpenAI's whisper.

**Telegram Integration**: Ame seamlessly integrates with Telegram, allowing you to interact with her through text-based messaging and voice notes. Telegram provides a familiar and convenient way to interact with Ame, enabling efficient communication and access to her full range of functionalities.

**Open-Source**: Ame will be entirely open-source. This allows for knowledge sharing and the continuous improvement of Ame while contributing to the open-source community and democratizing ML research in the process.

**Locally Run and Privacy-Focused**: Ame prioritizes user privacy and data control by operating entirely on the user's local machine.

**Long-term Memory**: Ame utilizes a vector database that optimizes memory storage and retrieval, enabling Ame to access data that goes beyond the context limit of her model.

## The meaning behind "Ame"
The name "Ame" originates from the Japanese word "あめ" (pronounced ah-meh), which translates to "rain" in English. Like rain, Ame represents a refreshing and nourishing presence in your digital life. Just as raindrops bring life to the earth, Ame breathes life into your digital environment, providing support and efficiency.

By choosing the name Ame, I aim to embody the qualities of adaptability, and revitalization, that rain symbolizes. I hope that Ame can be the reliable companion that brings a refreshing experience to your daily digital interactions.

## Progress (`v1`)
🔴 Planned
🟡 In progress
🟢 Finished

### Core

Component                     | Status 
----------------------------- | -----
Speech-to-text                |  🟢
Text-to-speech                |  🟡
Voice identification          |  🔴
Vision system                 |  🔴
Long-term memory              |  🟢
Primary controller            |  🟢
Module handler                |  🟡
Server/client interface       |  🟢
Client UI                     |  🔴
Telegram interface            |  🔴

### Fine-tuning LLaMA

Step                          | Status 
----------------------------- | -----
Planning                      |  🟢
Dataset                       |  🟢
Training method               |  🟡
Hardware acquisition          |  🟡
Training                      |  🔴

### Out-of-the-box modules

Module                        | Status 
----------------------------- | -----
Weather                       |  🟡
Google Calendar               |  🔴
News                          |  🔴
DeepL                         |  🔴
Discord                       |  🔴
Shell                         |  🔴

## Contributing
If you would like to contribute to the Ame project, please contact me.

## Acknowledgements 
Ame relies on 3rd party open source software to function, this project would not have been possible without:

- [HyperDB](https://github.com/jdagdelen/hyperDB) - Long term memory vector DB
- [Whisper](https://github.com/openai/whisper) - Speech to text
- [LLaMA](https://github.com/facebookresearch/llama) and [Wizard-Vicuna Uncensored](https://huggingface.co/ehartford/Wizard-Vicuna-13B-Uncensored) - Base LLM

## License
Ame will be released under the GNU General Public License v3, which allows you to use, modify, and distribute the software freely. Please refer to the [license file](https://github.com/Expl0dingCat/ame/blob/main/LICENSE) for more details.
