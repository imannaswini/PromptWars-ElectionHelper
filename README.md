# 🗳️ VoteWise AI – Election Assistant

**VoteWise AI** is a smart, context-aware election guidance assistant built for the **PromptWars Hackathon**.

It helps citizens understand voter registration, eligibility, election deadlines, polling logistics, and first-time voting through a clean interactive experience powered by intelligent decision logic.

---

# 🚀 Challenge Vertical

**Election Process Education**

---

# 🎯 Problem Statement

Many citizens face confusion around:

* How to register to vote
* Whether they are eligible
* Important deadlines
* What documents are required
* Where to vote
* How the process works for first-time voters

This confusion can reduce participation and create avoidable barriers.

---

# 💡 Solution

VoteWise AI simplifies the election process through a personalized assistant that adapts responses based on user context.

The system uses:

* Age
* First-time voter status
* State / location
* Urgency level
* Language preference

This creates practical, user-specific guidance instead of generic answers.

---

# ✨ Key Features

## Smart Election Assistant

Interactive chatbot for election-related questions.

## Eligibility Guidance

Age-aware support for voting readiness.

## Registration Help

Step-by-step voter registration instructions.

## First-Time Voter Mode

Beginner-friendly election walkthrough.

## Polling Guidance

Polling location and voting-day preparation support.

## Deadline Awareness

Election timelines and action reminders.

## Multilingual Ready

Expandable translation support for broader accessibility.

## Smart Offline Mode

Reliable fallback guidance when live AI services are unavailable.

---

# 🧠 Google Services Integration

## Gemini API

Used for conversational intelligence and natural-language responses.

## Google Ecosystem Ready Architecture

Designed for future expansion with:

* Google Translate
* Google Maps / Places
* Google Cloud services

## Reliability Layer

Fallback civic guidance engine ensures uninterrupted usability.

---

# 🏗️ Project Architecture

```text
assets/
data/
modules/
app.py
logic.py
README.md
requirements.txt
```

## Modular Design

* `app.py` → Streamlit frontend
* `logic.py` → compatibility layer
* `modules/engine.py` → decision engine
* `modules/election_data.py` → data access
* `modules/prompts.py` → prompt logic

---

# ⚙️ How It Works

1. User enters profile context
2. User asks election-related question
3. Decision engine checks intent + context
4. Personalized answer is generated
5. Offline fallback activates if needed

---

# 🛡️ Security & Responsible Design

* Non-partisan informational guidance only
* No candidate persuasion
* Minimal data handling
* Safe educational assistant behavior

---

# ♿ Accessibility

* Clear readable UI
* Beginner-friendly responses
* Guided workflows
* Expandable multilingual support

---

# 💻 Run Locally

```bash
git clone <repository-url>
cd PromptWars-ElectionHelper
pip install -r requirements.txt
streamlit run app.py
```

Create `.env`

```env
GOOGLE_API_KEY=your_api_key_here
```

---

# 📝 Example Prompts

* I just turned 18. What should I do first?
* How do I register to vote in California?
* Where is my polling station?
* What documents do I need to vote?
* I’m a first-time voter. Help me prepare.

---

# 🔮 Future Improvements

* Real-time polling APIs
* Verified registration systems
* Deadline notifications
* Voice assistant support
* Expanded multilingual translation

---

# ❤️ Built for PromptWars Hackathon

VoteWise AI aims to make the election process more understandable, accessible, and practical for every citizen.
