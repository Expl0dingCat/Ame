from llama_cpp import Llama

class ai:
    def __init__(self, model_pth, use_gpu=True, context=2048):
        if use_gpu:
            self.llm = Llama(model_path=model_pth, verbose=False, n_gpu_layers=20000, n_threads=5, n_ctx=context)
        else:
            self.llm = Llama(model_path=model_pth, verbose=False, n_threads=5, n_ctx=2048)
        
    def generate(self, prompt, max_tokens=128, temperature=0.85, stop=["USER: "], echo=False):
        response = self.llm(prompt, max_tokens=max_tokens, stop=stop, echo=echo, temperature=temperature)
        text = response['choices'][0]['text']
        prompt_tokens = response['usage']['prompt_tokens']
        completion_tokens = response['usage']['completion_tokens']
        return text.strip(), prompt_tokens, completion_tokens
