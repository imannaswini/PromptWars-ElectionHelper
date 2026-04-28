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

    def initialize_model(self):
        try:
            genai.configure(api_key=self.api_key)

            models = [
                "gemini-1.5-flash",
                "gemini-1.5-pro"
            ]

            for model_name in models:
                try:
                    self.model = genai.GenerativeModel(model_name)
                    self.model.generate_content(
                        "test",
                        generation_config={"max_output_tokens": 1}
                    )
                    self.active_model = model_name
                    return
                except:
                    continue

        except:
            self.model = None

    def is_configured(self):
        return self.model is not None

    def get_status(self):
        return "Live" if self.model else "Offline"

    def lookup_polling_stations(self, location):
        data = {
            "New York": "1. Central Library\n2. City Hall\n3. Community Center",
            "California": "1. Civic Center\n2. Westside High School\n3. Town Hall",
            "Texas": "1. County Courthouse\n2. Public Library\n3. Recreation Center",
            "Florida": "1. Beachside Hall\n2. City Hall\n3. North School"
        }

        return data.get(
            location,
            "Use ZIP code search on your local election website."
        )

    def translate_text(self, text, language):
        if language == "English":
            return text

        return f"[Translated to {language}]: {text}"

    def process_query(self, query, context):

        age = int(context.get("age", 25))
        location = context.get("location", "California")
        urgency = context.get("urgency", "Standard")
        first_time = context.get("is_first_time", False)

        q = query.lower()

        # Underage
        if age < 18:
            return """
You are under 18 and may not be eligible to vote yet.

Some states allow pre-registration at 16 or 17.

You can still:
• Learn voting rules
• Volunteer locally
• Prepare for first election
"""

        # Registration
        if "register" in q:
            deadline = get_deadline(location)
            state = get_state_info(location)

            return f"""
## Register to Vote in {location}

1. Visit official registration site  
2. Fill in your details  
3. Submit application  

**Deadline:** {deadline['registration_deadline']}

Website:
{state['registration']}
"""

        # First-time voter
        if first_time:
            return """
## First-Time Voter Starter Guide

1. Confirm registration  
2. Bring ID  
3. Check polling station  
4. Review ballot choices  
5. Vote confidently
"""

        # Polling
        if "poll" in q or "station" in q or "where vote" in q:
            stations = self.lookup_polling_stations(location)

            return f"""
## Polling Locations ({location})

{stations}
"""

        # Deadline
        if "deadline" in q or "date" in q or "when" in q:
            deadline = get_deadline(location)

            return f"""
## Important Dates ({location})

• Registration Deadline: {deadline['registration_deadline']}
• Election Day: {deadline['election_day']}
"""

        # Critical urgency
        if urgency == "Critical":
            return """
## Immediate Action Checklist

• Check registration now  
• Verify ID documents  
• Confirm polling place  
• Prepare before deadlines
"""

        # AI Mode
        if self.model:
            try:
                prompt = f"""
{SYSTEM_PROMPT}

User Context:
Age: {age}
Location: {location}
Urgency: {urgency}
First Time: {first_time}

User Question:
{query}
"""
                response = self.model.generate_content(prompt)

                if response and response.text:
                    return response.text

            except:
                pass

        return self.offline_fallback()

    def offline_fallback(self):
        return """
I'm in offline mode right now.

I can still help with:

• Registration
• Deadlines
• Polling stations
• Eligibility
• First-time voting
"""