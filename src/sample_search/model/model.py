from pathlib import Path

import librosa
import torch
import torch.nn.functional as f
from transformers import ClapModel, ClapProcessor


class Model:
    _model: ClapModel
    _processor: ClapProcessor

    SAMPLE_RATE = 48000

    def __init__(self, model_name: str) -> None:
        self._model = ClapModel.from_pretrained(model_name)
        self._processor = ClapProcessor.from_pretrained(model_name)

    def audio_embedding(self, file_path: Path) -> list[float]:
        audio_data, _ = librosa.load(file_path, sr=self.SAMPLE_RATE)
        inputs = self._processor(
            audio=audio_data, return_tensors="pt", sampling_rate=self.SAMPLE_RATE
        )

        with torch.no_grad():
            audio_embedding = self._model.get_audio_features(**inputs)
        tensor = f.normalize(audio_embedding.pooler_output, p=2, dim=-1)
        return tensor[0].detach().cpu().tolist()

    def text_embedding(self, text: str) -> list[float]:
        inputs = self._processor(text=[text], return_tensors="pt")
        with torch.no_grad():
            text_embedding = self._model.get_text_features(**inputs)

        tensor = f.normalize(text_embedding.pooler_output, p=2, dim=-1)
        return tensor[0].detach().cpu().tolist()
