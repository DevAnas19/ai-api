from pydantic import BaseModel, Field
from typing import Optional

# ── Summarize ──────────────────────────────────────────
class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description="Text to summarize")
    max_words: Optional[int] = Field(100, ge=10, le=500, description="Max words in summary")

class SummarizeResponse(BaseModel):
    summary: str
    original_word_count: int
    summary_word_count: int

# ── Translate ───────────────────────────────────────────
class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to translate")
    target_language: str = Field(..., description="Language to translate to e.g. Hindi, French")
    source_language: Optional[str] = Field("auto", description="Source language, default is auto detect")

class TranslateResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str

# ── Email Generator ─────────────────────────────────────
class EmailRequest(BaseModel):
    subject: str = Field(..., min_length=3, description="Email subject or topic")
    tone: Optional[str] = Field("professional", description="Tone: professional, friendly, formal")
    key_points: list[str] = Field(..., min_length=1, description="Key points to include in the email")
    recipient_name: Optional[str] = Field(None, description="Name of the recipient")

class EmailResponse(BaseModel):
    subject: str
    body: str
    tone: str