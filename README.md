
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
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

#### 3. Install dependencies:
pip install -r requirements.txt

#### 4. Set up API Key:
* Create a .env file in the project directory.
* Add your API key:
GOOGLE_API_KEY=your_api_key_here

#### 5. Run the agent:
python main.py

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



- Speech Recognition ✅ Completed
- AI Response Generation (Gemini API) ✅ Completed
- Text-to-Speech (gTTS & Pygame) ✅ Completed
- Task Switching ✅ Completed
- Demo Scheduling Storage ✅ Completed
- Error Handling & Robustness ⚠️ Partially - Implemented
- Multi-Language Support ✅ Complete


## Future Improvements
* Improve speech recognition accuracy with noise filtering.
* Enhance error handling for better user experience.
* Support additional languages apart from Hindi.


## License

This project is open-source and available under the MIT License.
