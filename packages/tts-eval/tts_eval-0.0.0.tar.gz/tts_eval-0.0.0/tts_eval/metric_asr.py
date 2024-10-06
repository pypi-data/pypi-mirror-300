import logging
from typing import Optional, Union, List, Callable, Dict
from collections import defaultdict

import torch
import numpy as np
from transformers import pipeline
from transformers.models.whisper.english_normalizer import BasicTextNormalizer, EnglishTextNormalizer
from transformers import WhisperTokenizer
from evaluate import load


class ASRMetric:

    def __init__(self,
                 model_id: str = "kotoba-tech/kotoba-whisper-v2.0",
                 torch_dtype: Optional[torch.dtype] = torch.bfloat16,
                 device: Optional[torch.device] = None,
                 attn_implementation: str = "sdpa",
                 device_map: str = "auto",
                 metrics: Union[str, List[str]] = "wer"):
        logging.info("setup pipeline")
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model_id,
            torch_dtype=torch_dtype,
            device=device,
            device_map=device_map,
            model_kwargs={"attn_implementation": attn_implementation}
        )
        logging.info("setup metric")
        metrics = [metrics] if type(metrics) is str else metrics
        self.metrics = {i: load(i) for i in metrics}
        logging.info("setup normalizer")
        basic_normalizer: Callable = BasicTextNormalizer()
        en_normalizer: Callable = EnglishTextNormalizer(WhisperTokenizer.from_pretrained(model_id).english_spelling_normalizer)
        ja_normalizer: Callable = lambda x: basic_normalizer(x).replace(" ", "").replace("。.", "。")
        self.normalizer = defaultdict(lambda: basic_normalizer, {"en": en_normalizer, "ja": ja_normalizer})

    def __call__(self,
                 audio: Union[np.ndarray, bytes, str],
                 transcripts: List[str],
                 language: str = "ja",
                 task: str = "transcribe",
                 normalize_text: bool = True) -> Dict[str, List[float]]:
        text = self.pipe(audio, generate_kwargs={"language": language, "task": task})["text"]
        if normalize_text:
            text = self.normalizer[language](text)
            transcripts = [self.normalizer[language](t) for t in transcripts]
        result = {}
        for k, metric in self.metrics.items():
            result[k] = [100 * metric.compute(predictions=[text], references=[t]) for t in transcripts]
        return result
