#based on https://github.com/aypan17/machiavelli/blob/723d76c9db388e3590703cbd7d5443f452969464/machiavelli/openai_helpers.py
import os
import time
import openai
from dotenv import load_dotenv
import pandas as pd
from typing import Dict, List, Mapping, Optional

# Set OpenAI API key
ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=ENV_PATH)
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_completion_with_retries(model: str, messages: List, max_retries: int = 5, retry_interval_sec: int = 20, max_tokens = float('inf'), api_keys=None, validation_fn=None, **kwargs) -> Mapping:
    for n_attempts_remaining in range(max_retries, 0, -1):
        try:
            res = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens = max_tokens,
                **kwargs)
            
            if validation_fn is not None:
                if not validation_fn(res):
                    print(f"VALIDATION FAILED!\nResponse:\n{res}\nTrying again.")
                    continue
            return res
        except (
            openai.error.RateLimitError,
            openai.error.ServiceUnavailableError,
            openai.error.APIError,
            openai.error.APIConnectionError,
            openai.error.Timeout,
            openai.error.TryAgain,
            openai.error.OpenAIError,
            ) as e:
            print(e)
            print(f"Hit openai.error exception. Waiting {retry_interval_sec} seconds for retry... ({n_attempts_remaining - 1} attempts remaining)", flush=True)
            time.sleep(retry_interval_sec)
    return {}

def save_labels(path, rows, columns=None, mode='a', header=False):
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(path, mode=mode, header=header, index=False)
    
def get_last_processed_row(path, default_header=None):
    try:
        df = pd.read_csv(path)
        return len(df)
    except FileNotFoundError:
        if default_header:
            with open(path, 'w') as f:
                f.write(default_header + "\n")
        return 0