import torch
import librosa
from transformers import ClapModel, ClapProcessor
import sys

# 1. Load the model (Only happens once)
print("--- Loading CLAP Model... (This takes a moment) ---")
try:
    model = ClapModel.from_pretrained("laion/clap-htsat-unfused")
    processor = ClapProcessor.from_pretrained("laion/clap-htsat-unfused")
    print("--- Model Loaded Successfully ---\n")
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

def get_audio_embedding(file_path):
    """Loads audio and returns the embedding vector."""
    try:
        # Load audio at 48kHz (standard for CLAP)
        audio_data, _ = librosa.load(file_path, sr=48000)

        # Optional: Trim to first 10s to keep it snappy
        # audio_data = audio_data[:48000*10]

        # Process audio inputs
        inputs = processor(audios=audio_data, return_tensors="pt", sampling_rate=48000)

        # Get the embedding (run only the audio branch of the model)
        with torch.no_grad():
            audio_embed = model.get_audio_features(**inputs)

        # Normalize immediately for Cosine Similarity
        # (Vector / Magnitude = Unit Vector)
        audio_embed = audio_embed / audio_embed.norm(dim=-1, keepdim=True)
        return audio_embed

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None

def get_text_embedding(text_query):
    """Converts text query to embedding vector."""
    inputs = processor(text=[text_query], return_tensors="pt")
    with torch.no_grad():
        text_embed = model.get_text_features(**inputs)

    # Normalize
    text_embed = text_embed / text_embed.norm(dim=-1, keepdim=True)
    return text_embed

# --- MAIN LOOP ---
while True:
    # 2. Get Audio File
    audio_path = input("\nEnter path to audio file (or 'quit' to exit): ").strip().strip('"').strip("'")

    if audio_path.lower() in ['quit', 'exit']:
        break

    if not audio_path:
        continue

    print(f"Processing audio: {audio_path}...")
    audio_emb = get_audio_embedding(audio_path)

    if audio_emb is None:
        continue # Ask for file again if it failed

    print("Audio indexed! You can now type multiple queries to test against this file.")
    print("(Type 'new' to load a different audio file, or 'quit' to exit script)")

    # 3. Text Query Loop
    while True:
        query = input("\n  Enter text query: ").strip()

        if query.lower() == 'new':
            break # Break inner loop, go back to asking for file
        if query.lower() in ['quit', 'exit']:
            sys.exit(0) # Kill entire script
        if not query:
            continue

        # Calculate Score
        text_emb = get_text_embedding(query)

        # Cosine Similarity = Dot Product of normalized vectors
        score = (text_emb @ audio_emb.T).item()

        # Fancy formatting for the output
        bar_len = int(score * 20) if score > 0 else 0
        bar = "█" * bar_len
        print(f"  Score: {score:.4f} | {bar}")