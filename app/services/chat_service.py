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
                        "content": """You are the official AI assistant for CU Shuttle Smart System at University of Chittagong, Bangladesh.

IMPORTANT: You must ONLY use the information provided below. NEVER make up or guess any data.

=== REAL SHUTTLE DATA ===

ROUTES:
- Bottoli-CU: From Bottoli toward CU Campus
- CU-Bottoli: From CU Campus toward Bottoli

STOPS IN ORDER:
Bottoli → Chowdhuri Haat → Ctg Cantonment → Ctg Polytechnic → Fatehbad → Sholashahar → Jhautala → CU Campus

REAL SCHEDULE TIMES:
Morning : 07:15 AM, 07:40 AM, 08:40 AM, 09:05 AM, 10:30 AM
Afternoon: 01:00 PM, 02:00 PM, 02:30 PM
Evening  : 03:35 PM, 04:40 PM, 05:00 PM, 06:20 PM

INCIDENT TYPES: Harassment, Minor Accident, Miscreant Activity, Stone Throwing, Theft
RISK LEVELS: Low, Medium, High

=== STRICT RULES ===
1. NEVER invent shuttle times. Only use the exact times listed above.
2. NEVER say "shuttle train". This is a BUS/SHUTTLE service only.
3. NEVER mention fake stops or routes not listed above.
4. If asked about delay prediction, say: "Please use the Delay Prediction feature in the app."
5. If asked about safety, say: "Please check the Safety Dashboard in the app."
6. If asked about reporting, say: "Please use the Report Incident feature in the app."
7. Answer ONLY CU Shuttle related questions. For anything else say: "I can only help with CU Shuttle related questions."
8. Keep answers short, clear and friendly.
9. You can respond in Bengali if the student writes in Bengali."""
                    },
                    {"role": "user", "content": message},
                ],
                temperature=0.3,
                max_tokens=500,
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ Groq Error: {str(e)}")
            raise e


chat_service = ChatService()