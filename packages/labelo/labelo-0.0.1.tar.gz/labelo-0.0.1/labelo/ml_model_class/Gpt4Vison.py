import base64
import subprocess
import numpy as np
from openai import OpenAI

try:
    import cv2
    from PIL import Image
except ImportError:
    pass

from notifications.models import Notifications

class Gpt4Vision:
    def __init__(self, vision_api_key):
        self.client = OpenAI(api_key=vision_api_key)

    def generate_desc_with_path(self, path):
        image = np.asarray(Image.open(path))
        desc = self.gen_desc("Describe this image", image)
        return desc.message.content

    def gen_desc(self, prompt, image):
        def encode_to_base64():
            if isinstance(image, np.ndarray):
                success, encoded_image = cv2.imencode('.jpg', image)
                if not success:
                    raise ValueError("Could not encode image")
                return base64.b64encode(encoded_image).decode('utf-8')

        message_content = [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encode_to_base64()}"
                }
            }
        ]
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[{"role": "user", "content": message_content}],
            max_tokens=300,
        )
        return response.choices[0]

    @classmethod
    def install(self, user):
        Notifications.create_notification(
            users=[user],
            content="Started to download packages needed for Gpt4 Vision",
            title="Downloading"
        )
        subprocess.run(['poetry', 'add', "opencv-python-headless"], check=True)
        subprocess.run(['poetry', 'add', "pillow"], check=True)
        Notifications.create_notification(
            users=[user],
            content="Gpt4 Vision is downloaded and ready.",
            title="Downloaded"
        )