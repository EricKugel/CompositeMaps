"""
General llm agent code. Using a local llm right now but eventually I'll need to use an API likely
"""

from huggingface_hub import login
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

with open("data/keys/keys.json", "r") as file:
    keys = eval(file.read())
login(keys["hugging_face_login"])

# cuda opt
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
torch.set_float32_matmul_precision("high")

quantization_config = BitsAndBytesConfig(load_in_8bit=True)
model_name = "meta-llama/Llama-3.1-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=quantization_config
)

model.eval()

class Agent():
    def __init__(self, sys_message=None, history=[]):
        self.sys_message = sys_message
        self.history = history
        self.max_new_tokens = 256
        self.chat_length = 32

    def query(self, prompt):
        self.history.append({"role": "user", "content": prompt})
        
        history = self.history[-self.chat_length:]
        if self.sys_message:
            history = [{"role": "system", "content": self.sys_message}] + history

        inputs = tokenizer.apply_chat_template(
            history,
            # [{"role": "system", "content": self.sys_message}, {"role": "user", "content": prompt}],
            return_tensors="pt",
            add_generation_prompt=True,
            return_dict=True
        )

        inputs = inputs.to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                input_ids=inputs["input_ids"].to(model.device),
                attention_mask=inputs["attention_mask"].to(model.device),
                max_new_tokens=self.max_new_tokens,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id,
            )

        response = tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[-1]:],
            skip_special_tokens=True
        )
        
        history.append({"role": "assistant", "content": response})

        return response.strip()