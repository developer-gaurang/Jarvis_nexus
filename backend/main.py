import os
import json
import asyncio
import traceback
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from google import genai
import numpy as np
import sounddevice as sd

# Import core systems
from core.skill_manager import SkillManager
from core.audio_engine import LocalAudioEngine

# Initialize Environment
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    # Adding for strict error handling during initialization
    print("[Error] Missing GEMINI_API_KEY in .env")

# Initialize Gemini Client (Modern SDK)
gemini_client = genai.Client(api_key=gemini_api_key) if gemini_api_key else None

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
            print("\n[Backend] Awaiting data from frontend...")
            # Await client payload
            data = await websocket.receive_text()
            print(f"[Backend] Raw data received: {data}")
            
            payload = json.loads(data)
            print(f"[Backend] Parsed JSON Payload: {payload}")
            
            user_input = payload.get("command", "")
            user_lang = payload.get("langName", "English")  # Detected language from frontend
            user_lang_code = payload.get("lang", "en-US")
            print(f"[Backend] Extracted command: '{user_input}' | Language: {user_lang} ({user_lang_code})")

            # 1. Pipeline Check: Does a local mod/skill handle this?
            print("[Backend] Checking SkillManager for intents...")
            skill_response = skill_manager.handle_intent(user_input, context={"websocket": websocket})
            print(f"[Backend] SkillManager response: {skill_response}")
            
            if skill_response:
                ai_response = skill_response
                print("[Backend] Using local skill response.")
            else:
                # 2. Default standard LLM routing
                print("[Backend] Routing to LLM (Google Gemini) via gemini-2.5-flash model...")
                try:
                    if not gemini_api_key or not gemini_client:
                        raise ValueError("GEMINI_API_KEY is missing. Please add it to your .env file.")
                    
                    # Build a multilingual-aware prompt
                    lang_instruction = (
                        f"CRITICAL LANGUAGE RULE: The user has written their message in {user_lang}. "
                        f"You MUST reply ENTIRELY in {user_lang} only. "
                        f"Do NOT use English unless the user specifically asked in English. "
                        f"Match the user's language exactly.\n\n"
                    )
                    full_prompt = (
                        "System Instruction: You are J.A.R.V.I.S., an incredibly smart, friendly, and helpful AI assistant. "
                        "You should answer warmly, naturally, and intelligently. "
                        "Engage in normal conversation, be empathetic if needed, and give detailed, helpful answers. Use emojis if you want.\n"
                        + lang_instruction +
                        f"User Request: {user_input}"
                    )
                    
                    # Modern google.genai async generation using the 2.5 flash model
                    response = await gemini_client.aio.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=full_prompt
                    )
                    ai_response = response.text
                except Exception as ex:
                    ai_response = f"Gemini API Error: {ex}"
                print(f"[Backend] LLM generation complete. Content length: {len(ai_response)} characters")
            
            # Wapas UI ko reply bhejna
            response_data = {
                "role": "JARVIS",
                "content": ai_response,
                "imageUrl": None
            }
            
            # Check if this is a special image generation payload
            if ai_response.startswith("[IMAGE_PAYLOAD]"):
                try:
                    payload_json = json.loads(ai_response.replace("[IMAGE_PAYLOAD]", "", 1))
                    response_data["content"] = payload_json.get("text", "I have generated the image.")
                    response_data["imageUrl"] = payload_json.get("image_url")
                    print(f"[Backend] Extracted image generation payload: {response_data['imageUrl']}")
                except Exception as e:
                    print(f"Error parsing image payload: {e}")
                    
            response_json = json.dumps(response_data)
            print(f"[Backend] Sending response back to WebSocket: {response_json[:100]}...")
            
            await websocket.send_text(response_json)
            print("[Backend] Successfully sent response payload to WebSocket! Waiting for next input.")

        except Exception as e:
            print(f"!!! [Backend ERROR] WebSocket loop crashed !!!")
            print(f"Exception Type: {type(e).__name__}")
            print(f"Exception Detail: {e}")
            traceback.print_exc()
            break

@app.websocket("/ws/audio_amplitude")
async def audio_amplitude_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Frontend Connected to Audio Amplitude Stream!")
    
    loop = asyncio.get_running_loop()
    audio_queue = asyncio.Queue(maxsize=10) # Prevent queue buildup

    def audio_callback(indata, frames, time, status):
        # Calculate RMS amplitude
        rms = np.sqrt(np.mean(indata**2))
        try:
            loop.call_soon_threadsafe(audio_queue.put_nowait, float(rms))
        except asyncio.QueueFull:
            pass # Drop frame if sending is too slow

    try:
        # Start microphone input stream
        stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=16000)
        with stream:
            while True:
                volume = await audio_queue.get()
                # Multiply by an arbitrary scalar (e.g., 500) to make the volume changes prominent for UI reactivity
                await websocket.send_text(json.dumps({"type": "amplitude", "value": volume * 500}))
    except Exception as e:
        print(f"Audio stream closed or errored: {e}")

# force reload