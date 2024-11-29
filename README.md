# IconGPT 🤖

A tool to generate an emoji based on an emotion, sentence, phrase or even a single word. Implements simple RAG on the [`llm-emoji-dataset`](https://huggingface.co/datasets/badrex/llm-emoji-dataset) by using MongoDB Atlas Vector search for semantic similarity.

## Usage and Setup

Clone the GitHub repository and navigate to the root folder.

Install the necessary dependencies.

```bash
python -m pip install -r requirements.txt
```

Now run [`app.py`](./app.py) using this command.

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Open a browser and go to <http://localhost:8000/docs> to test the endpoint.

### CPU Inference

Just install torch for CPU to get started.

```bash
python -m pip install torch
```

### Setting up CUDA (Optional)

`cuda` is recommended for a faster inference if you have a GPU available.

Install the NVIDIA CUDA Toolkit (version greater than or equal to 11.8) and `torch >= 11.8`.

> Note: Make sure the toolkit and `torch` have same versions (i.e., 11.8)

```bash
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Now run the following command in a Python shell to confirm installation.

```python
>> import torch
>> print(torch.cuda.is_available())
True
```

## Acknowledgements

I would like to acknowledge the [owner](https://huggingface.co/badrex) of the `llm-emoji-dataset`.

## Contribution

Feel free to open up a pull request or create an issue.
