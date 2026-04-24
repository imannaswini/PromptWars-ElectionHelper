import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class ElectionLogicEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None

    def get_system_prompt(self):
        try:
            with open("prompts.txt", "r") as f:
                return f.read()
        except FileNotFoundError:
            return "You are an election education assistant."

    def process_query(self, query, context):
        """
        Decision Engine:
        - Checks age, first-time status, and location to tailor the prompt.
        """
        system_prompt = self.get_system_prompt()
        
        # Build logical context string
        context_str = f"""
        USER CONTEXT:
        - Age: {context.get('age', 'Unknown')}
        - First-time Voter: {context.get('is_first_time', 'No')}
        - Location: {context.get('location', 'USA')}
        - Urgency: {context.get('urgency', 'Normal')}
        - Language: {context.get('language', 'English')}
        """

        # Logical Decision Branches
        logic_hints = ""
        if context.get('age') and int(context.get('age')) < 18:
            logic_hints += " RULE: User is underage. Focus on education and future eligibility."
        elif context.get('is_first_time'):
            logic_hints += " RULE: User is a first-time voter. Provide a step-by-step beginner guide."
        
        if context.get('urgency') == "High":
            logic_hints += " RULE: High urgency. Focus on immediate deadlines and polling locations."

        full_prompt = f"{system_prompt}\n\n{context_str}\n\n{logic_hints}\n\nUser Query: {query}"

        if not self.model:
            return "Error: Google API Key not configured. Please check your .env file."

        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error communicating with Gemini: {str(e)}"

    def translate_text(self, text, target_language):
        """
        Mock Google Translate Integration
        In a real app, this would use the Google Cloud Translation API.
        """
        if target_language == "English":
            return text
        # Mocking translation for demo purposes
        return f"[Translated to {target_language}]: {text}"

    def lookup_polling_stations(self, location):
        """
        Mock Google Maps Integration
        In a real app, this would use Google Maps Places API.
        """
        # Static mock data based on common locations
        mock_data = {
            "New York": "1. Central Library, 2. City Hall, 3. PS 101 Community Center",
            "California": "1. Downtown Civic Center, 2. Westside High School, 3. Community Hall",
            "Texas": "1. County Courthouse, 2. Northside Recreation Center, 3. Public Library"
        }
        return mock_data.get(location, "1. Local Community Center, 2. Nearest Public School, 3. City Hall")

def get_election_timeline():
    return {
        "Registration Deadline": "October 10, 2026",
        "Mail-in Ballot Request": "October 20, 2026",
        "Early Voting Starts": "October 25, 2026",
        "Election Day": "November 3, 2026"
    }
