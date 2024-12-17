import torch
import torchvision.models as models

from s3_functions import upload_s3_file

def get_model():
    model = models.resnet50(pretrained=True)

    model.eval()

    dummy_input = torch.randn(1, 3, 224, 224)

    input_names = [ "actual_input" ]
    output_names = [ "output" ]

    # Ensure the local directory exists
    if not os.path.exists("models"):
        os.makedirs("models")

    torch.onnx.export(model, 
                    dummy_input,
                    "models/resnet50.onnx",
                    verbose=False,
                    input_names=input_names,
                    output_names=output_names,
                    export_params=True,
                    )

def main():
    get_onnx_model()

    upload_s3_file("models/resnet50.onnx", "huggingface_models_martine/Converted_ONNX_Models/resnet50.onnx")


if __name__ == "__main__":
    main()