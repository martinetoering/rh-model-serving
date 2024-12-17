# TODO
import argparse
from kserve import Model, ModelServer, model_server, InferInput, InferRequest, logging
from typing import Dict
import logging
import io
import base64
import kserve
from gliner import GLiNER


class GlinerTransformer(kserve.Model):
    def __init__(self, name: str, predictor_host: str, headers: Dict[str, str] = None):
        super().__init__(name)
        self.predictor_host = predictor_host
        print("pr host", self.predictor_host)
        self.model = GLiNER.from_pretrained("urchade/gliner_multi-v2.1",
                                            load_onnx_model=True,
                                            onnx_model_file="onnx/model_q4.onnx",
                                            load_tokenizer=True,
                                            local_files_only=True)

        self.ready = True

    def preprocess(self, inputs: Dict, headers: Dict[str, str] = None) -> Dict:
        text, label, threshold

        return {'instances': [image_transform(instance) for instance in inputs['instances']]}

    def postprocess(self, inputs: Dict, headers: Dict[str, str] = None) -> Dict:
        return inputs

parser = argparse.ArgumentParser(parents=[model_server.parser])
args, _ = parser.parse_known_args()

if __name__ == "__main__":
    model = GlinerTransformer(
        args.model_name,
        predictor_host=args.predictor_host,
    )
    ModelServer().start([model])