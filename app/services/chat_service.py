# app/services/chat_service.py
from groq import Groq
from app.core.config import settings

class ChatService:
    def __init__(self):
        self.client = None
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            print("✅ Groq client initialized in service")
        else:
            print("⚠️  WARNING: GROQ_API_KEY not found")

    async def get_response(self, message: str) -> str:
        if not self.client:
            raise Exception("Chat service not configured")

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful, friendly, and concise CU Shuttle assistant for University of Chittagong students."
                    },
                    {"role": "user", "content": message},
                ],
                temperature=0.7,
                max_tokens=500,
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ Groq Error: {str(e)}")
            raise e


chat_service = ChatService()