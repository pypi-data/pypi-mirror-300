try:
    from PIL import Image
    from transformers import BlipForConditionalGeneration, BlipProcessor
except ImportError:
    pass

from notifications.models import Notifications
import subprocess

class Blip:
    def __init__(self):
        self.model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        self.processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")


    def generate_desc_with_path(self, path):
        raw_image = Image.open(path).convert('RGB')
        inputs = self.processor(raw_image, return_tensors="pt")
        out = self.model.generate(**inputs)
        return self.processor.decode(out[0], skip_special_tokens=True)

    @classmethod
    def install(self, user):
        Notifications.create_notification(
            users=[user],
            content="Started to download packages and models needed for Blip",
            title="Downloading"
        )
        subprocess.run(['poetry', 'add', "transformers"], check=True)
        subprocess.run(['poetry', 'add', "pillow"], check=True)
        subprocess.run(['poetry', 'add', "torch"], check=True)
        BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
        BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
        Notifications.create_notification(
            users=[user],
            content="Blip is downloaded and ready.",
            title="Downloaded"
        )
