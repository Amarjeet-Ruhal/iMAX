
# AI Cold-Calling Agent


## Project Description

The AI Cold-Calling Agent is an interactive voice-based assistant that helps automate customer interactions, such as scheduling ERP demos, conducting interview screenings, and following up on payments/orders. It leverages speech recognition, text-to-speech synthesis, and AI-generated responses to handle conversations dynamically.


## Setup and Installation

### Prerequisites
* Python 3.8+
* A working microphone
* An OpenAI or Google Gemini API key

### Installation Steps
#### 1. Clone the repository:
git clone https://github.com/your-repo/ai-cold-calling.git
cd ai-cold-calling

#### 2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

#### 4. Set up API Key:
* Create a .env file in the project directory.
* Add your API key:
```bash
GOOGLE_API_KEY="AIzaSyDznXOghv-5RmRYXXiAkgIb1O6rF3DWFzQ"
```

#### 5. Run the agent:
python test5.py

## Models and Datasets Used
* Speech Recognition: Google Speech Recognition API for converting spoken input to text.
* AI Response Generation: Gemini 2.0 Flash (Google Generative AI) for dynamically generating responses based on user input.
* Text-to-Speech: Google Text-to-Speech (gTTS) for converting AI-generated responses into audio.

## Agent Architecture
* The AI Cold-Calling Agent follows a modular architecture with the following key components:
* Speech Recognition Module (SpeechRecognition & PyAudio) → Captures user input via microphone.
* Intent Detection Module → Determines the task (Demo Scheduling, Interview, or Payment Follow-up).
* AI Response Generation Module (Google Gemini API) → Generates appropriate responses based on context.
* Text-to-Speech Module (gTTS & Pygame) → Converts text responses to speech and plays them.
* Task Switching Mechanism → Allows users to switch tasks dynamically during conversations.
* Demo Scheduling Storage → Saves confirmed demos in demo_schedule.txt


## Demonstration Video

Watch a demonstration of the AI Cold-Calling Agent in action:
👉 Loom Video


## Features and Implementation Status


| Features | Status |
|---------  | -------- |
| Speech Recognition | ✅ Completed |
|AI Response Generation (Gemini API)|✅ Completed|
|Text-to-Speech (gTTS & Pygame)| ✅ Completed|
|Task Switching |✅ Completed|
|Demo Scheduling Storage| ✅ Completed|
|Error Handling & Robustness |⚠️ Partially - Implemented
|Multi-Language Support |✅ Complete|


## Future Improvements
* Improve speech recognition accuracy with noise filtering.
* Enhance error handling for better user experience.
* Support additional languages apart from Hindi.


## License

This project is open-source and available under the [![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/).


## 🚀 About Me
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/amarjeet-ruhal/)
