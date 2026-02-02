import torch
from transformers import ClapModel

if __name__ == "__main__":
    model = ClapModel.from_pretrained("laion/clap-htsat-unfused")

    model.eval()

    # Audio model export
    # Shape Explanation: (Batch_Size, Channels, Time_Steps, Frequency_Bins)
    # - Batch: 1
    # - Channels: 1 (Mono)
    # - Time: 1001 (This corresponds to exactly 10.01 seconds of audio at 48kHz)
    # - Freq: 64 (The number of Mel bins CLAP was trained on)
    dummy_audio_spectrogram = torch.randn(1, 1, 1001, 64)

    torch.onnx.export(
        model.audio_model,
        dummy_audio_spectrogram,
        "clap_audio.onnx",
        input_names=["input_features"], # This matches the HuggingFace argument name
        output_names=["audio_embeds"],
        dynamic_axes={
            "input_features": {0: "batch_size", 2: "time_steps"}, # Allow variable time lengths
            "audio_embeds": {0: "batch_size"}
        },
        opset_version=18
    )
    print("Audio model exported (Expects Spectrogram: [B, 1, T, 64])")


    # Text model export
    # Shape: (Batch_Size, Sequence_Length)
    # CLAP uses a fixed sequence length of 77 (like CLIP)
    dummy_text_ids = torch.randint(0, 1000, (1, 77))
    dummy_mask = torch.ones(1, 77)

    torch.onnx.export(
        model.text_model,
        (dummy_text_ids, dummy_mask),
        "clap_text.onnx",
        input_names=["input_ids", "attention_mask"],
        output_names=["text_embeds"],
        dynamic_axes={
            "input_ids": {0: "batch_size"},
            "attention_mask": {0: "batch_size"},
            "text_embeds": {0: "batch_size"}
        },
        opset_version=18
    )
    print("Text model exported")