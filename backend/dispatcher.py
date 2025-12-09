from groq import Groq
import json
import time
from typing import Optional
from dotenv import load_dotenv
import os

# Load .env automatically
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Pass the API key here
client = Groq(api_key=GROQ_API_KEY)

# Simple backoff helper
def _backoff_sleep(attempt: int):
    time.sleep(min(2 ** attempt, 8))


def generate_variation(prompt: str, max_retries: int = 3) -> str:
    """Send a single prompt to Groq and return the variant message.

    Returns the string inside the JSON key `variant_message` when possible,
    otherwise returns the raw model output as a fallback.
    """
    for attempt in range(max_retries):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_completion_tokens=600,
                top_p=1,
                stream=False
            )

            # groq's response shape may vary; handle common shapes
            content = None
            try:
                content = completion.choices[0].message.content
            except Exception:
                try:
                    content = completion.choices[0].text
                except Exception:
                    content = str(completion)

            # try to parse JSON from model output
            try:
                data = json.loads(content)
                if isinstance(data, dict) and "variant_message" in data:
                    return data["variant_message"]
                for key in ("variant_message", "message", "result"):
                    if key in data:
                        return data[key]
                return json.dumps(data, ensure_ascii=False)
            except Exception:
                return content

        except Exception as e:
            if attempt < max_retries - 1:
                _backoff_sleep(attempt)
                continue
            raise e


if __name__ == '__main__':
    sample_prompt = "Write a short friendly variant for this message: Hello, we have a special offer"
    print(generate_variation(sample_prompt))
