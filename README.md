# AI API Service

A REST API built with FastAPI that provides AI-powered text summarization, translation, and email generation using Groq LLM.

## Features

- **POST /summarize** — Summarize long text into concise summaries
- **POST /translate** — Translate text into any language
- **POST /generate-email** — Generate professional emails from key points
- Request validation using Pydantic
- Global exception handling
- Structured logging (console + file)
- Auto-generated API documentation via Swagger UI

## Tech Stack

- Python 3.11
- FastAPI
- Groq (LLaMA 3.3 70B)
- Pydantic
- Uvicorn
- Python-dotenv

## Project Structure

```
ai_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # App entry point, registers all routes
│   ├── config.py            # Loads environment variables
│   ├── logger.py            # Logging setup (console + file)
│   ├── exceptions.py        # Global exception handlers
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic request/response models
│   └── routes/
│       ├── __init__.py
│       ├── summarize.py     # POST /summarize
│       ├── translate.py     # POST /translate
│       └── email_gen.py     # POST /generate-email
├── .env                     # Secret keys (not pushed to GitHub)
├── .env.example             # Template for environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

## Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/DevAnas19/ai-api.git
cd ai-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file

```bash
cp .env.example .env
```

### 4. Add your Groq API key to `.env`

```env
APP_NAME="AI API Service"
APP_VERSION="1.0.0"
DEBUG=True
GROQ_API_KEY="your-groq-api-key-here"
```

> Get your free Groq API key at https://console.groq.com

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

### 6. Open API docs

```
http://127.0.0.1:8000/docs
```

## API Endpoints

### GET /
Health check endpoint.

**Response:**
```json
{
  "message": "Welcome to AI API Service",
  "version": "1.0.0"
}
```

---

### POST /summarize
Summarizes the given text into a concise summary.

**Request Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| text | string | Yes | Text to summarize (min 50 chars) |
| max_words | integer | No | Max words in summary (default: 100) |

**Request:**
```json
{
  "text": "India is a diverse country with a rich cultural heritage spanning thousands of years. It is home to over 1.4 billion people speaking hundreds of languages and dialects. The country has made significant progress in technology, space exploration, and economic growth in recent decades.",
  "max_words": 50
}
```

**Response:**
```json
{
  "summary": "India is a diverse nation with over 1.4 billion people, rich cultural heritage, and significant progress in technology and economic growth.",
  "original_word_count": 61,
  "summary_word_count": 23
}
```

---

### POST /translate
Translates text into the specified target language.

**Request Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| text | string | Yes | Text to translate |
| target_language | string | Yes | Language to translate to |
| source_language | string | No | Source language (default: auto) |

**Request:**
```json
{
  "text": "Cricket is the most popular sport in India",
  "target_language": "Hindi",
  "source_language": "English"
}
```

**Response:**
```json
{
  "translated_text": "क्रिकेट भारत में सबसे लोकप्रिय खेल है",
  "source_language": "English",
  "target_language": "Hindi"
}
```

---

### POST /generate-email
Generates a professional email based on subject, tone, and key points.

**Request Body:**

| Field | Type | Required | Description |
|---|---|---|---|
| subject | string | Yes | Email subject or topic |
| tone | string | No | Tone: professional, friendly, formal (default: professional) |
| key_points | list | Yes | List of key points to include |
| recipient_name | string | No | Name of the recipient |

**Request:**
```json
{
  "subject": "Requesting a Leave of Absence",
  "tone": "professional",
  "key_points": [
    "I need 3 days off from Monday",
    "My work is up to date",
    "I will be available on email"
  ],
  "recipient_name": "Manager"
}
```

**Response:**
```json
{
  "subject": "Requesting a Leave of Absence",
  "body": "Dear Manager,\n\nI am writing to request a leave of absence for the next three days, starting from Monday...",
  "tone": "professional"
}
```

---

## Error Handling

The API returns consistent error responses for all failure cases.

**Validation Error (422):**
```json
{
  "error": "Validation Error",
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Server Error (500):**
```json
{
  "error": "Internal Server Error",
  "detail": "Something went wrong. Please try again later."
}
```

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| APP_NAME | Name of the application | Yes |
| APP_VERSION | Version of the application | Yes |
| DEBUG | Enable debug mode (True/False) | No |
| GROQ_API_KEY | Your Groq API key | Yes |

---

## Logging

The app logs all requests and errors in two places:

- **Console** — DEBUG level and above (for development)
- **app.log** — INFO level and above (persisted on disk)

Log format:
```
2026-06-25 10:23:45 | INFO | app.routes.summarize | Summarize request received
```

---

## License

MIT