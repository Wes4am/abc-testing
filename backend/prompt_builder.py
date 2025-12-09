# backend/prompt_builder.py

def build_prompt(original_message: str, parameters_text: str) -> str:
    """
    Builds a clean instruction prompt for Groq.

    The model must output clean JSON ONLY with:
    {
        "variant_message": ""
    }
    """

    return f"""
You are generating ONE marketing message variation.
Follow the instructions exactly.

Base Message:
{original_message}

Variation Parameters (apply them strictly):
{parameters_text}

Guidelines:
- Preserve the core meaning of the original.
- Follow the provided parameters EXACTLY.
- Do NOT introduce new claims, offers, or fake information.
- Adjust tone, style, length, or framing as needed.
- Avoid hallucinations.
- If parameters conflict with the base message, keep the meaning intact and adjust only tone/phrasing.

OUTPUT FORMAT (MANDATORY):
Return ONLY valid JSON (no explanations, no markdown, no text before or after):
{{
    "variant_message": ""
}}
"""
