# 🗳️ VoteWise: AI Election Assistant

**VoteWise** is a smart, context-aware AI assistant designed to simplify the election process for citizens. Built for the **PromptWars** hackathon, it leverages Google Gemini and other services to provide personalized guidance based on user demographics and location.

## 🚀 Problem Statement
Navigating the complexities of voter registration, eligibility rules, and election timelines can be overwhelming, especially for first-time voters and minority groups. Misinformation or lack of clarity often leads to lower voter turnout.

## 🎯 Chosen Vertical
**Election Process Education**

## ✨ Features
- **Context-Aware Intelligence**: Tailors advice based on user age, first-time status, and location.
- **Logical Decision Engine**:
  - Automatically identifies underage users and provides educational paths.
  - Generates specialized guides for first-time voters.
  - Prioritizes urgent tasks as election day approaches.
- **Multilingual Support**: Integration (mocked) with Google Translate for diverse language preferences.
- **Polling Station Finder**: Quick lookup for voting centers (mocked via Maps logic).
- **Interactive Timeline**: Real-time tracking of critical election dates.
- **Simplified Mode**: Break down complex legal jargon into easy-to-understand steps.

## 🛠️ Google Services Used
1.  **Gemini API**: Powers the core conversational intelligence and logical reasoning.
2.  **Google Translate (Mocked)**: Provides architectural layout for multilingual support.
3.  **Google Maps (Mocked)**: Logic structure for location-based polling station retrieval.

## 💻 How to Run Locally

1.  **Clone the repository**:
    ```bash
    git clone [repository-url]
    cd PromptWars-ElectionHelper
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables**:
    Create a `.env` file in the root directory and add your Gemini API Key:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    ```

4.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## 📝 Example Prompts
- "I'm 17, how can I prepare for the next election?"
- "What documents do I need to register in California?"
- "Is it too late to request a mail-in ballot?"
- "Explain the voting process like I'm 5."

## 🔮 Future Improvements
- **Live Google Maps Integration**: Real-time polling station navigation.
- **Verified Voter APIs**: Integration with official state registration databases.
- **Push Notifications**: SMS/Email alerts for upcoming deadlines.
- **Voice Support**: Hands-free interaction for accessibility.

---
Built with ❤️ for **PromptWars Hackathon**.
