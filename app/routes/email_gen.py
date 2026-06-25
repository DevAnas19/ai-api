from groq import Groq
from fastapi import APIRouter, HTTPException
from app.models.schemas import EmailRequest, EmailResponse
from app.logger import get_logger
from app.config import GROQ_API_KEY

router = APIRouter()
logger = get_logger(__name__)

client = Groq(api_key=GROQ_API_KEY)

@router.post("/generate-email", response_model=EmailResponse)
async def generate_email(request: EmailRequest):
    logger.info(f"Email generation request received | tone={request.tone}")

    try:
        key_points_formatted = "\n".join([f"- {point}" for point in request.key_points])
        recipient = request.recipient_name if request.recipient_name else "the recipient"

        prompt = f"""
        Write a {request.tone} email to {recipient} about: {request.subject}

        Include these key points:
        {key_points_formatted}

        Return only the email body, nothing else. No subject line.
        """

        logger.debug("Sending prompt to Groq")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )

        body = response.choices[0].message.content.strip()

        logger.info("Email generated successfully")

        return EmailResponse(
            subject=request.subject,
            body=body,
            tone=request.tone
        )

    except Exception as e:
        logger.error(f"Email generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Email generation failed: {str(e)}")