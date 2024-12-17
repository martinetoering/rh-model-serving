# TODO
import argparse

from typing import Dict, Union
import torch
import numpy as np
from kserve import Model, ModelServer
from gliner import GLiNER


class GlinerModel(Model):
    def __init__(self, name: str, model_path: str):
       super().__init__(name)
       self.name = name
       self.model_path = model_path
       self.load()

    def load(self):
        self.model = GLiNER.from_pretrained(self.model_path,
                                    load_onnx_model=True,
                                    onnx_model_file="onnx/model_q4.onnx",
                                    load_tokenizer=True,
                                    local_files_only=True)
        self.ready = True

    def predict(self, payload: Dict, headers: Dict[str, str] = None) -> Dict:
        text = payload["instances"][0]["text"]
        labels = payload["instances"][0]["labels "]
        threshold = payload["instances"][0]["threshold"]

        entities = model.predict_entities(text, labels, threshold=threshold)

        return {"predictions": entities}

if __name__ == "__main__":
    model = GlinerModel("gliner", "urchade/gliner_multi-v2.1")
    ModelServer().start([model])