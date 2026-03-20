import os
import json
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from groq import AsyncGroq

# Import core systems
from core.skill_manager import SkillManager
from core.audio_engine import LocalAudioEngine

# Initialize Environment
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    # Adding for strict error handling during initialization
    print("[Error] Missing GROQ_API_KEY in .env")

# Asynchronous NLP Setup
# Using AsyncGroq prevents blocking the FastAPI event loop
client = AsyncGroq(api_key=groq_api_key)

# Initialize Skills and Audio
skill_manager = SkillManager()
audio_engine = LocalAudioEngine()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/jarvis")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Frontend Connected to JARVIS Nexus Core!")
    
    welcome_msg = "Cloud connection established. NEXUS Core online. How may I assist?"
    # Emit welcome info
    await websocket.send_text(json.dumps({
        "role": "JARVIS", 
        "content": welcome_msg
    }))
    # Disabled server-side pyttsx3 because frontend Output Audio Streamer (Web Speech) handles it now
    # audio_engine.speak(welcome_msg)

    while True:
        try:
            # Await client payload
            data = await websocket.receive_text()
            payload = json.loads(data)
            user_input = payload.get("command", "")
            
            # Note on Voice STT integration:
            # If payload contained binary audio buffer directly,
            # you would route it to `audio_engine.stt_transcribe(audio_buffer)`
            # and use transcoded text as `user_input`.

            print(f"User: {user_input}")

            # 1. Pipeline Check: Does a local mod/skill handle this?
            # E.g., "what's my ram usage?" -> bypasses LLM overhead
            skill_response = skill_manager.handle_intent(user_input, context={"websocket": websocket})
            
            if skill_response:
                ai_response = skill_response
            else:
                # 2. Default standard LLM routing (asynchronous)
                chat_completion = await client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are J.A.R.V.I.S., a highly advanced AI system designed "
                                "for system management and general assistance. Be concise, technical "
                                "and proactive. Omit emojis. Maximize utility."
                            )
                        },
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ],
                    model="llama3-8b-8192", 
                )
                ai_response = chat_completion.choices[0].message.content
            
            # Wapas UI ko reply bhejna
            await websocket.send_text(json.dumps({
                "role": "JARVIS",
                "content": ai_response
            }))

            # Pyttsx3 server-speak disabled to prevent looping/double audio
            # audio_engine.speak(ai_response)
            
        except Exception as e:
            print(f"WebSocket closed or errored: {e}")
            break