import os
import time

import backoff
import openai
from openai.error import (
    APIConnectionError,
    APIError,
    RateLimitError,
    ServiceUnavailableError,
    InvalidRequestError
)

import base64
import requests


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class Engine:
    def __init__(self) -> None:
        pass

    def tokenize(self, input):
        return self.tokenizer(input)


class OpenaiEngine(Engine):
    def __init__(
            self,
            api_key=None,
            stop=["\n\n"],
            rate_limit=-1,
            model=None,
            temperature=0,
            **kwargs,
    ) -> None:
        """Init an OpenAI GPT/Codex engine

        Args:
            api_key (_type_, optional): Auth key from OpenAI. Defaults to None.
            stop (list, optional): Tokens indicate stop of sequence. Defaults to ["\n"].
            rate_limit (int, optional): Max number of requests per minute. Defaults to -1.
            model (_type_, optional): Model family. Defaults to None.
        """
        assert (
                os.getenv("OPENAI_API_KEY", api_key) is not None
        ), "must pass on the api_key or set OPENAI_API_KEY in the environment"
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY", api_key)
        if isinstance(api_key, str):
            self.api_keys = [api_key]
        elif isinstance(api_key, list):
            self.api_keys = api_key
        else:
            raise ValueError("api_key must be a string or list")
        self.stop = stop
        self.temperature = temperature
        self.model = model
        # convert rate limit to minmum request interval
        self.request_interval = 0 if rate_limit == -1 else 60.0 / rate_limit
        self.next_avil_time = [0] * len(self.api_keys)
        self.current_key_idx = 0
        Engine.__init__(self, **kwargs)

    def encode_image(self, image_path):
        with open(self, image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    @backoff.on_exception(
        backoff.expo,
        (APIError, RateLimitError, APIConnectionError, ServiceUnavailableError, InvalidRequestError),
    )
    def generate(self, prompt: list = None, max_new_tokens=50, temperature=0, model=None, image_path=None,
                 ouput__0=None, turn_number=0, **kwargs):
        self.current_key_idx = (self.current_key_idx + 1) % len(self.api_keys)
        start_time = time.time()
        if (
                self.request_interval > 0
                and start_time < self.next_avil_time[self.current_key_idx]
        ):
            time.sleep(self.next_avil_time[self.current_key_idx] - start_time)
        openai.api_key = self.api_keys[self.current_key_idx]
        prompt0 = prompt[0]
        prompt1 = prompt[1]
        prompt2 = prompt[2]

        if turn_number == 0:
            base64_image = encode_image(image_path)
            # Assume one turn dialogue
            prompt1_input = [
                {"role": "system", "content": [{"type": "text", "text": prompt0}]},
                {"role": "user",
                 "content": [{"type": "text", "text": prompt1}, {"type": "image_url", "image_url": {"url":
                                                                                                        f"data:image/jpeg;nase64,{base64_image}",
                                                                                                    "detail": "high"},
                                                                 }]},
            ]
            response1 = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=prompt1_input,
                max_tokens=4096,
                temperature=0,
                **kwargs,
            )
            answer1 = [choice["message"]["content"] for choice in response1["choices"]][0]

            return answer1
        elif turn_number == 1:
            base64_image = encode_image(image_path)
            prompt2_input = [
                {"role": "system", "content": [{"type": "text", "text": prompt0}]},
                {"role": "user",
                 "content": [{"type": "text", "text": prompt1}, {"type": "image_url", "image_url": {"url":
                                                                                                        f"data:image/jpeg;nase64,{base64_image}",
                                                                                                    "detail": "high"}, }]},
                {"role": "assistant", "content": [{"type": "text", "text": f"\n\n{ouput__0}"}]},
                {"role": "user", "content": [{"type": "text", "text": prompt2}]}, ]
            response2 = openai.ChatCompletion.create(
                model="gpt-4-vision-preview",
                messages=prompt2_input,
                max_tokens=4096,
                temperature=0,
                **kwargs,
            )
            return [choice["message"]["content"] for choice in response2["choices"]][0]
