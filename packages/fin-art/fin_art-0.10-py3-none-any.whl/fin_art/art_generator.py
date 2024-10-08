import tqdm
tqdm.tqdm.__init__ = lambda *args, **kwargs: None

import warnings
warnings.filterwarnings("ignore")

from transformers import logging
logging.set_verbosity_error()

from diffusers import logging
logging.set_verbosity_error()

import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from diffusers import StableDiffusionPipeline
import matplotlib.pyplot as plt

class ImageGenerator:
    def __init__(self, model_name='k1tub/gpt2_prompts', tokenizer_name='distilbert/distilgpt2', 
                 stable_diff_model='stable-diffusion-v1-5/stable-diffusion-v1-5', lora_weights='madvasik/pixel-art-lora',
                 device='cuda'):
        # Initialize GPT-2 model and tokenizer
        self.tokenizer = GPT2Tokenizer.from_pretrained(tokenizer_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token  # Ensure padding uses eos_token
        self.model = GPT2LMHeadModel.from_pretrained(model_name).to(device)
        self.device = device
        
        # Initialize Stable Diffusion pipeline
        self.text2img_pipe = StableDiffusionPipeline.from_pretrained(stable_diff_model,
                                                                     torch_dtype=torch.float16, safety_checker=True).to(device)
        self.text2img_pipe.load_lora_weights(lora_weights)

    def generate_images(self, input_prompt, num_images=1, num_inference_steps=100, show_prompt=False):
        # Generate GPT-2 based prompts
        prompts = []
        input_ids = self.tokenizer.encode(input_prompt, return_tensors="pt").to(self.device)
        
        # Create attention mask for the input_ids
        attention_mask = torch.ones(input_ids.shape, device=self.device)  # All tokens are attended to

        for _ in range(num_images):
            # Pass attention_mask explicitly and ensure pad_token_id is eos_token_id
            out = self.model.generate(input_ids, attention_mask=attention_mask, 
                                      max_length=70, num_return_sequences=1, pad_token_id=self.tokenizer.eos_token_id)
            generated_text = self.tokenizer.decode(out[0], skip_special_tokens=True)
            prompts.append(generated_text)

        # Generate images using Stable Diffusion
        images = []
        for prompt in prompts:
            image = self.text2img_pipe(prompt, num_inference_steps=num_inference_steps).images[0]
            images.append((image, prompt))

        # Display images one by one
        for img, prompt in images:
            if show_prompt:
                print(f"Generated prompt: {prompt}")  # Print the prompt before showing the image

            plt.figure(figsize=(6, 6))
            plt.imshow(img)
            plt.axis("off")
            plt.show()