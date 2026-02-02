import librosa
import torch
from transformers import ClapModel, ClapProcessor


class Model:
    model: ClapModel
    processor: ClapProcessor

    SAMPLE_RATE = 48000

    def __init__(self, model_name: str) -> None:
        self.model = ClapModel.from_pretrained(model_name)
        self.processor = ClapProcessor.from_pretrained(model_name)

    def audio_embedding(self, file_path: str) -> torch.Tensor:
        audio_data, _ = librosa.load(file_path, sr=self.SAMPLE_RATE)
        inputs = self.processor(
            audios=audio_data, return_tensors="pt", sampling_rate=self.SAMPLE_RATE
        )

        with torch.no_grad():
            audio_embedding = self.model.get_audio_features(**inputs)
        tensor: torch.Tensor = audio_embedding / audio_embedding.norm(
            dim=-1, keepdim=True
        )

        return tensor
