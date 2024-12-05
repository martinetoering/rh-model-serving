# Model serving

# Single model

## token-classifcation-onnx-gliner

```python
python call_endpoint_text.py --url https://onnx-gliner-martine-demo-single-model.apps.rosa.rosa-jxx8z.wlcq.p3.openshiftapps.com --model token-classification-onnx-gliner
```

# Multi-model

## token-classifcation-onnx-gliner

```python
python call_endpoint_text.py --url http://modelmesh-serving.martine-demo-project:8008 --model token-classification-onnx-gliner
```

## object-detection-tensorflow-efficientdet-d0

Download data; 

```python
python download_huggingface_dataset.py
```

```python
python call_endpoint_image.py --url http://modelmesh-serving.martine-demo-project:8008 --model object-detection-tensorflow-efficientdet-d0
```