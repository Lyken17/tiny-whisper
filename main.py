import torch
import sys, os
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


fname = "output_audio_full.mp3"
if len(sys.argv) >= 2:
    print(sys.argv)
    fname = sys.argv[-1]
    
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
model_id = "distil-whisper/distil-large-v2"

model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model.to(device)

processor = AutoProcessor.from_pretrained(model_id)
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=15,
    batch_size=4,
    torch_dtype=torch_dtype,
    device=device,
)


result = pipe(fname, return_timestamps=True)

from utils import hf_pipeline_to_srt

output_srt = fname.replace(".mp3", ".srt")
hf_pipeline_to_srt(result, output_file=output_srt)
