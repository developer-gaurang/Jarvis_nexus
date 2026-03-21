import re
import time
import json
import urllib.parse
import requests
import os
from skills.base_skill import BaseSkill


class ImageGeneratorSkill(BaseSkill):
    name = "ImageGeneration"
    description = "Generates an image using Nano Banana API (nanobananaapi.ai) with Pollinations.ai fallback."

    NANO_BANANA_GENERATE_URL = "https://api.nanobananaapi.ai/api/v1/nanobanana/generate"
    NANO_BANANA_STATUS_URL   = "https://api.nanobananaapi.ai/api/v1/nanobanana/record-info"

    def can_handle(self, user_input: str) -> bool:
        trigger_words = [
            "generate image", "create image", "draw", "make a picture",
            "generate a photo", "generate picture", "generate an image",
            "generate a image", "create a picture", "create an image",
            "image banao", "tasveer banao", "photo banao",
            "ek tasveer", "ek image"
        ]
        return any(word in user_input.lower() for word in trigger_words)

    def _extract_prompt(self, user_input: str) -> str:
        """Remove trigger phrases and return clean image prompt."""
        prompt = user_input
        trigger_words = [
            "generate an image of", "generate a image of", "generate image of",
            "generate an image", "generate a image", "generate image",
            "create an image of", "create a image of", "create image of", "create image",
            "draw a picture of", "draw an image of", "draw",
            "make a picture of", "make a picture",
            "generate a photo of", "generate a photo", "generate picture",
            "image banao", "tasveer banao", "photo banao",
            "ek tasveer", "ek image"
        ]
        for word in sorted(trigger_words, key=len, reverse=True):
            if word in prompt.lower():
                prompt = re.split(re.escape(word), prompt, flags=re.IGNORECASE, maxsplit=1)[-1].strip()
                break

        return prompt if prompt else "a dynamic futuristic glowing AI core"

    def _nano_banana_generate(self, prompt: str, api_key: str) -> str | None:
        """
        Submit image generation task to Nano Banana API.
        Returns the image URL on success, None on failure.
        
        Flow:
          1. POST /generate  → get taskId
          2. GET  /record-info?taskId=xxx  → poll until done → extract image URL
        """
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Step 1 — Submit task
        body = {
            "prompt": prompt,
            "type": "TEXTTOIAMGE",   # exact spelling as per Nano Banana docs
            "numImages": 1,
            "callBackUrl": None,
            "watermark": False
        }

        print(f"[NanoBanana] Submitting image task for prompt: '{prompt[:60]}...'")
        resp = requests.post(
            self.NANO_BANANA_GENERATE_URL,
            headers=headers,
            json=body,
            timeout=30
        )
        resp.raise_for_status()
        resp_data = resp.json()
        print(f"[NanaBanana] Generate response: {resp_data}")

        task_id = (
            resp_data.get("data", {}).get("taskId")
            or resp_data.get("taskId")
        )
        if not task_id:
            print("[NanaBanana] ERROR: No taskId in response.")
            return None

        # Step 2 — Poll for result (max 60s, every 3s)
        print(f"[NanaBanana] Polling taskId={task_id} for result...")
        for attempt in range(20):
            time.sleep(3)
            poll_resp = requests.get(
                self.NANO_BANANA_STATUS_URL,
                headers=headers,
                params={"taskId": task_id},
                timeout=15
            )
            poll_resp.raise_for_status()
            poll_data = poll_resp.json()
            print(f"[NanaBanana] Poll attempt {attempt + 1}: {poll_data}")

            status = (
                poll_data.get("data", {}).get("status")
                or poll_data.get("status", "")
            )

            # Success statuses
            if status in ("SUCCESS", "COMPLETED", "DONE", "success", "completed"):
                # Try multiple possible response shapes
                image_url = (
                    poll_data.get("data", {}).get("imageUrl")
                    or poll_data.get("data", {}).get("url")
                    or poll_data.get("data", {}).get("outputImageUrls", [None])[0]
                    or poll_data.get("imageUrl")
                )
                if image_url:
                    print(f"[NanaBanana] ✅ Image ready: {image_url[:80]}")
                    return image_url
                else:
                    print("[NanaBanana] Status SUCCESS but no imageUrl found.")
                    return None

            # Failure status
            if status in ("FAILED", "ERROR", "failed", "error"):
                print(f"[NanaBanana] ❌ Task failed with status: {status}")
                return None

            # Still processing — continue
            print(f"[NanaBanana] Still processing (status={status}), waiting...")

        print("[NanaBanana] ⏰ Timeout: image not ready after 60s.")
        return None

    def _pollinations_fallback(self, prompt: str) -> str:
        """Free fallback — Pollinations.ai (no API key needed)."""
        encoded_prompt = urllib.parse.quote(prompt.strip())
        return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={int(time.time())}"

    def execute(self, user_input: str, context: dict) -> str:
        prompt = self._extract_prompt(user_input)
        nano_banana_key = os.getenv("NANO_BANANA_API_KEY", "").strip()

        image_url = None
        source = "Pollinations.ai"

        # Try Nano Banana first if API key is configured
        if nano_banana_key and nano_banana_key != "your_nano_banana_api_key_here":
            try:
                image_url = self._nano_banana_generate(prompt, nano_banana_key)
                if image_url:
                    source = "Nano Banana AI"
            except Exception as e:
                print(f"[NanaBanana ERROR]: {e} → Falling back to Pollinations.ai")

        # Fallback to Pollinations.ai
        if not image_url:
            print("[ImageGenerator] Using Pollinations.ai fallback...")
            image_url = self._pollinations_fallback(prompt)
            source = "Pollinations.ai"

        payload = {
            "text": f"Here is your generated image for: **{prompt}** ✨ _(Powered by {source})_",
            "image_url": image_url
        }

        return f"[IMAGE_PAYLOAD]{json.dumps(payload)}"
