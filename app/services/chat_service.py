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

STRICT RULE 1: ONLY use the exact data below. NEVER invent or guess any times, stops, or routes.
STRICT RULE 2: ALWAYS respond in the SAME language the student used. English question = English answer. Bengali question = Bengali answer.
STRICT RULE 3: When listing shuttle times, ALWAYS show ALL shuttles for that route or direction, never just one.

=== CU CAMPUS → BOTTOLI (CU-Bottoli direction) ===
Shuttle 132 | On day only | CU 08:40 AM → Fatehbad 08:50 AM → Ctg Cantonment 09:02 AM → Sholashahar 09:10 AM → Bottoli 09:10 AM
Shuttle 134 | Every day   | CU 09:05 AM → Fatehbad 09:15 AM → Ctg Cantonment 09:27 AM → Sholashahar 09:43 AM → Bottoli 09:55 AM
Shuttle 136 | On day only | CU 10:30 AM → Fatehbad 10:38 AM → Ctg Cantonment 10:48 AM → Sholashahar 10:55 AM → Bottoli 11:05 AM
Shuttle 138 | On day only | CU 01:00 PM → Fatehbad 01:08 PM → Chowdhuri Haat 01:10 PM → Ctg Cantonment 01:18 PM → Sholashahar 01:25 PM → Ctg Polytechnic 01:38 PM → Jhautala 01:44 PM → Bottoli 02:00 PM
Shuttle 140 | On day only | CU 02:00 PM → Fatehbad 02:08 PM → Chowdhuri Haat 02:10 PM → Ctg Cantonment 02:18 PM → Sholashahar 02:25 PM → Ctg Polytechnic 02:38 PM → Jhautala 02:44 PM → Bottoli 03:00 PM
Shuttle 142 | On day only | CU 03:35 PM → Fatehbad 03:43 PM → Chowdhuri Haat 03:45 PM → Ctg Cantonment 03:53 PM → Sholashahar 04:02 PM → Ctg Polytechnic 04:14 PM → Jhautala 04:20 PM → Bottoli 04:35 PM
Shuttle 144 | Every day   | CU 04:40 PM → Fatehbad 04:48 PM → Chowdhuri Haat 04:50 PM → Ctg Cantonment 04:58 PM → Sholashahar 05:04 PM → Ctg Polytechnic 05:17 PM → Jhautala 05:22 PM → Bottoli 05:40 PM
Shuttle 146 | On day only | CU 06:20 PM → Fatehbad 06:28 PM → Chowdhuri Haat 06:34 PM → Ctg Cantonment 06:41 PM → Sholashahar 06:45 PM → Ctg Polytechnic 06:56 PM → Jhautala 07:02 PM → Bottoli 07:15 PM
Shuttle 148 | Every day   | CU 09:45 PM → Chowdhuri Haat 09:52 PM → Ctg Cantonment 09:57 PM → Sholashahar 10:01 PM → Ctg Polytechnic 10:12 PM → Jhautala 10:15 PM → Bottoli 10:30 PM

=== BOTTOLI → CU CAMPUS (Bottoli-CU direction) ===
Shuttle 131 | On day only | Bottoli 07:15 AM → Jhautala 07:25 AM → Sholashahar 07:29 AM → Ctg Cantonment 07:35 AM → Chowdhuri Haat 07:48 AM → Fatehbad 07:55 AM → CU 08:15 AM
Shuttle 133 | Every day   | Bottoli 07:40 AM → Jhautala 07:50 AM → Sholashahar 07:54 AM → Ctg Cantonment 08:00 AM → Chowdhuri Haat 08:13 AM → Fatehbad 08:20 AM → CU 08:35 AM
Shuttle 135 | On day only | Sholashahar 09:30 AM → Ctg Cantonment 09:41 AM → Chowdhuri Haat 09:48 AM → Fatehbad 09:50 AM → CU 10:05 AM
Shuttle 137 | On day only | Sholashahar 10:15 AM → Ctg Cantonment 10:25 AM → Chowdhuri Haat 10:33 AM → Fatehbad 10:35 AM → CU 10:50 AM
Shuttle 139 | On day only | Sholashahar 11:30 AM → Ctg Cantonment 11:40 AM → Chowdhuri Haat 11:46 AM → Fatehbad 11:50 AM → CU 12:00 PM
Shuttle 141 | On day only | Bottoli 02:30 PM → Jhautala 02:37 PM → Ctg Polytechnic 02:40 PM → Sholashahar 02:45 PM → Ctg Cantonment 02:53 PM → Chowdhuri Haat 03:00 PM → Fatehbad 03:06 PM → CU 03:15 PM
Shuttle 143 | Every day   | Bottoli 03:30 PM → Jhautala 03:37 PM → Ctg Polytechnic 03:39 PM → Sholashahar 03:45 PM → Ctg Cantonment 03:47 PM → Chowdhuri Haat 03:07 PM → Fatehbad 03:13 PM → CU 04:20 PM
Shuttle 145 | On day only | Bottoli 05:00 PM → Jhautala 05:07 PM → Ctg Polytechnic 05:09 PM → Sholashahar 05:15 PM → Ctg Cantonment 05:17 PM → Chowdhuri Haat 05:25 PM → Fatehbad 05:30 PM → CU 05:50 PM
Shuttle 147 | Every day   | Bottoli 08:30 PM → Jhautala 08:40 PM → Ctg Polytechnic 08:42 PM → Sholashahar 08:45 PM → Ctg Cantonment 08:52 PM → Chowdhuri Haat 09:00 PM → Fatehbad 09:06 PM → CU 09:25 PM

=== IMPORTANT NOTES ===
- "On day" = University working days only
- "Every day" = Runs on both working and off days
- This is a BUS/SHUTTLE service. It is NOT a train. Never call it a train.
- Incident types: Harassment, Minor Accident, Miscreant Activity, Stone Throwing, Theft
- Risk levels: Low, Medium, High

=== STRICT RESPONSE RULES ===
1. NEVER invent times or stops. Only use exact data above.
2. NEVER call it a train. Always say shuttle or bus.
3. ALWAYS show ALL relevant shuttles when listing times, not just one.
4. For delay prediction questions → say: Use the Delay Prediction feature in the app.
5. For safety questions → say: Check the Safety Dashboard in the app.
6. For reporting questions → say: Use the Report Incident feature in the app.
7. Answer ONLY CU Shuttle related questions. For anything else say: I can only help with CU Shuttle related questions.
8. Keep answers clear, complete and friendly.
9. ALWAYS respond in the SAME language as the student's question."""
                    },
                    {"role": "user", "content": message},
                ],
                temperature=0.2,
                max_tokens=800,
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ Groq Error: {str(e)}")
            raise e


chat_service = ChatService()