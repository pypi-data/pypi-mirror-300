try:
    from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
    import torch
    from PIL import Image
except ImportError:
    pass

from notifications.models import Notifications
import subprocess


class VitGpt2:
    def __init__(self):
        self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.config = {
            "max_length": 50,
            "num_beams": 4
        }

    def generate_desc_with_path(self, path):
        i_image = Image.open(path)
        if i_image.mode != "RGB":
            i_image = i_image.convert(mode="RGB")
        pixel_values = self.feature_extractor(images=[i_image], return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)
        output_ids = self.model.generate(pixel_values, **self.config)
        preds = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        return preds[0].strip()

    @classmethod
    def install(self, user):
        Notifications.create_notification(
            users=[user],
            content="Started to download packages and models needed for Vit Gpt2",
            title="Downloading"
        )
        subprocess.run(['poetry', 'add', "transformers"], check=True)
        subprocess.run(['poetry', 'add', "torch"], check=True)
        subprocess.run(['poetry', 'add', "pillow"], check=True)
        self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        Notifications.create_notification(
            users=[user],
            content="Vit Gpt2 is downloaded and ready.",
            title="Downloaded"
        )

