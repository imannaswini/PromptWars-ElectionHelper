import os
import google.generativeai as genai
from dotenv import load_dotenv

from modules.prompts import SYSTEM_PROMPT
from modules.election_data import get_deadline, get_state_info


class ElectionEngine:

    def __init__(self, api_key=None):
        load_dotenv()

        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = None
        self.active_model = None

        if self.api_key:
            self.initialize_model()

    # -------------------------
    # GEMINI INIT
    # -------------------------
    def initialize_model(self):
        try:
            genai.configure(api_key=self.api_key)

            models = [
                "gemini-1.5-flash",
                "gemini-1.5-flash-latest",
                "gemini-1.5-pro",
                "gemini-pro"
            ]

            for model_name in models:
                try:
                    model = genai.GenerativeModel(model_name)

                    # tiny test call
                    model.generate_content(
                        "hello",
                        generation_config={"max_output_tokens": 1}
                    )

                    self.model = model
                    self.active_model = model_name
                    return

                except Exception:
                    continue

        except Exception:
            self.model = None

    # -------------------------
    # STATUS
    # -------------------------
    def is_configured(self):
        return self.model is not None

    def get_status(self):
        return "Live" if self.model else "Offline"

    # -------------------------
    # DATA HELPERS
    # -------------------------
    def lookup_polling_stations(self, location):
        data = {
            "New York": """
1. Central Library
2. City Hall
3. Community Center
""",
            "California": """
1. Civic Center
2. Westside High School
3. Town Hall
""",
            "Texas": """
1. County Courthouse
2. Public Library
3. Recreation Center
""",
            "Florida": """
1. Beachside Hall
2. City Hall
3. North School
"""
        }

        return data.get(
            location,
            "Use ZIP code search on your local election website."
        )

    def translate_text(self, text, language):
        if language == "English":
            return text

        return f"[Translated to {language}]\n\n{text}"

    # -------------------------
    # MAIN ENGINE
    # -------------------------
    def process_query(self, query, context):

        age = int(context.get("age", 25))
        location = context.get("location", "California")
        urgency = context.get("urgency", "Standard")
        first_time = context.get("is_first_time", False)

        q = query.lower().strip()

        # -------------------------
        # RULE ENGINE FIRST
        # -------------------------

        # Underage
        if age < 18:
            return f"""
## Future Voter Guide ({location})

You are currently under 18, so you may not be eligible yet.

Some states allow pre-registration at 16 or 17.

### What You Can Do Now:
• Learn how elections work  
• Check pre-registration rules  
• Volunteer locally  
• Prepare for your first vote at 18
"""

        # Registration
        if any(word in q for word in ["register", "registration", "sign up"]):
            deadline = get_deadline(location)
            state = get_state_info(location)

            return f"""
## Register to Vote in {location}

### Steps:
1. Visit your official voter registration portal  
2. Fill in name, address, ID details  
3. Submit application  

### Deadline:
**{deadline['registration_deadline']}**

### Website:
{state['registration']}
"""

        # Polling stations
        if any(word in q for word in ["poll", "station", "where vote", "booth"]):
            stations = self.lookup_polling_stations(location)

            return f"""
## Polling Locations in {location}

{stations}

### Before You Go:
• Carry valid ID  
• Check polling hours  
• Reach early if possible
"""

        # First time voter
        if first_time or "first time" in q:
            return f"""
## First-Time Voter Guide ({location})

### Start Here:
1. Confirm your registration  
2. Carry valid ID  
3. Check polling place  
4. Read ballot choices  
5. Vote confidently

### Tip:
Try visiting early to avoid queues.
"""

        # Deadlines
        if any(word in q for word in ["deadline", "date", "when", "last day"]):
            deadline = get_deadline(location)

            return f"""
## Important Dates ({location})

• Registration Deadline: **{deadline['registration_deadline']}**  
• Election Day: **{deadline['election_day']}**
"""

        # Results
        if "result" in q or "counted" in q:
            return """
## Election Results Process

1. Polls close  
2. Votes are counted  
3. Mail ballots may take longer  
4. Official certification happens later

Early numbers may change as counting continues.
"""

        # ID / documents
        if any(word in q for word in ["id", "document", "passport", "license"]):
            return """
## Voting ID Requirements

Requirements vary by state.

Usually accepted:
• Driver's License  
• Passport  
• State ID Card

Some states also allow utility bills or voter card.
"""

        # Critical urgency
        if urgency == "Critical":
            return """
## Immediate Action Checklist

• Check registration now  
• Verify your ID  
• Confirm polling station  
• Review deadlines today
"""

        # -------------------------
        # GEMINI MODE
        # -------------------------
        if self.model:
            try:
                prompt = f"""
{SYSTEM_PROMPT}

User Context:
Age: {age}
Location: {location}
Urgency: {urgency}
First Time Voter: {first_time}

User Question:
{query}

Respond clearly in bullet points.
"""

                response = self.model.generate_content(prompt)

                if response and response.text:
                    return response.text

            except Exception:
                return self.smart_fallback(query, context, quota=True)

        # -------------------------
        # FALLBACK
        # -------------------------
        return self.smart_fallback(query, context)

    # -------------------------
    # SMART FALLBACK
    # -------------------------
    def smart_fallback(self, query, context, quota=False):

        location = context.get("location", "your state")
        q = query.lower()

        prefix = "⚠️ Gemini unavailable right now.\n\n" if quota else ""

        if "register" in q:
            return prefix + f"""
## Offline Registration Help ({location})

1. Visit official state voter website  
2. Complete registration form  
3. Submit before deadline
"""

        if "poll" in q:
            return prefix + f"""
## Offline Polling Help ({location})

Use your local election website or ZIP code lookup tool to find polling locations.
"""

        if "deadline" in q:
            return prefix + """
## Offline Deadline Help

Registration usually closes before Election Day.

Please verify on your state election website.
"""

        return prefix + """
I'm in offline mode right now.

I can still help with:

• Registration  
• Deadlines  
• Polling stations  
• Eligibility  
• First-time voting
"""