from groq import Groq
from fastapi import APIRouter, HTTPException
from app.models.schemas import TranslateRequest, TranslateResponse
from app.logger import get_logger
from app.config import GROQ_API_KEY

router = APIRouter()
logger = get_logger(__name__)

client = Groq(api_key=GROQ_API_KEY)

@router.post("/translate",response_model=TranslateResponse)
async def translated_text(request: TranslateRequest):
    logger.info(f"Translate request received | traget={request.target_language}")

    try:
        prompt = f"""
        Translate the following text to {request.target_language}.
        Source language is {request.source_language}.
        Return only the translated text , nothing else.

        Text: {request.text}
        """

        logger.debug("Sending prompt to Groq")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"user","content":prompt}]
        )

        translated_text = response.choices[0].message.content.strip()

        logger.info(f"Trranslation successful | target={request.target_language}")

        return TranslateResponse(
            translated_text=translated_text,
            source_language=request.source_language,
            target_language=request.target_language
        )

    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")