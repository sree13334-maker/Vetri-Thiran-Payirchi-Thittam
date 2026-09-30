import os

from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None


class GeminiDocumentGenerator:

    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()

        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        ).strip()

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. "
                "Add your Gemini API key to the .env file."
            )

        if genai is None:
            raise RuntimeError(
                "google-genai is not installed. "
                "Run: pip install -r requirements.txt"
            )

        self.client = genai.Client(
            api_key=self.api_key
        )

    def build_prompt(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        prompt = f"""
You are LegalEase, an AI assistant that drafts
professional legal document templates.

IMPORTANT RULES:

1. Generate a DRAFT only.
2. Do not provide legal advice.
3. Do not invent information.
4. Do not invent names, dates, addresses,
   amounts, laws or legal citations.
5. Use only information supplied by the user.
6. If information is missing, use:
   [NOT PROVIDED]
7. Keep the document professional and editable.
8. Use clear headings and paragraphs.
9. At the end include an Important Notice
   explaining that the document should be
   reviewed by a qualified legal professional.

DOCUMENT TYPE:

{document_type}

PARTIES:

{parties}

TERMS AND CONDITIONS:

{terms}

EFFECTIVE DATE:

{dates}

Create the legal document draft.

Use the following structure when appropriate:

TITLE

PARTIES

EFFECTIVE DATE

RECITALS / PURPOSE

DEFINITIONS

MAIN TERMS / OBLIGATIONS

PAYMENT OR CONSIDERATION

CONFIDENTIALITY

TERM AND TERMINATION

REPRESENTATIONS

DISPUTE / GOVERNING LAW

SIGNATURES

IMPORTANT NOTICE

Return only the document.
"""

        return prompt.strip()

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        prompt = self.build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            dates=dates
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        generated_text = getattr(
            response,
            "text",
            None
        )

        if not generated_text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return generated_text.strip()