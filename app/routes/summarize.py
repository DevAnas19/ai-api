from groq import Groq
from fastapi import APIRouter, HTTPException
from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.logger import get_logger
from app.config import GROQ_API_KEY

router = APIRouter()
logger = get_logger(__name__)

client = Groq(api_key=GROQ_API_KEY)

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest):
    logger.info("Summarize request received")

    try:
        prompt = f"""
        Summarize the following text in maximum {request.max_words} words.
        Return only the summary, nothing else.

        Text: {request.text}
        """

        logger.debug("Sending prompt to Groq")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content.strip()
        original_word_count = len(request.text.split())
        summary_word_count = len(summary.split())

        logger.info(f"Summary generated | original={original_word_count} words | summary={summary_word_count} words")

        return SummarizeResponse(
            summary=summary,
            original_word_count=original_word_count,
            summary_word_count=summary_word_count
        )

    except Exception as e:
        logger.error(f"Summarize failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")