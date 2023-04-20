import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

class Generator:
    def __init__(self, model_name, **kwargs):
        self.kwargs = kwargs
        print('Loading tokenizer...')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="left")
        print('Loading model...')
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", offload_folder='offload', torch_dtype=torch.bfloat16).to('cuda')
        print('Done loading!')

    def __call__(self, instruction):
        input_text = f'Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:{instruction}\n\n### Response:\n'
        with torch.cuda.amp.autocast(enabled=True, dtype=torch.float16):
            input_ids = self.tokenizer.encode(input_text, return_tensors='pt').to('cuda')
            output_ids = self.model.generate(input_ids, **self.kwargs)
            output_text = self.tokenizer.decode(output_ids[0])

        return output_text

modelPath = 'C:\\Users\\kulac\\Coding\\Projects\\AIModels\\Dolle'

ai = Generator(modelPath, temperature=0.7, max_length=128, do_sample=True)

while True:
    response = ai(input('Q: '))
    print('A:', response, '\n')
