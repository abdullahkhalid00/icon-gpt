# emoGPT 🙂🙃

A tool to generate an emoji based on an emotion, sentence, phrase or even a single word. Implements simple RAG on the [`llm-emoji-dataset`](https://huggingface.co/datasets/badrex/llm-emoji-dataset) by using MongoDB Atlas Vector search for semantic similarity.

## Run locally on CLI

Clone the GitHub repository and navigate to the root folder.

```bash
git clone <repo-link>
cd emoGPT
```

Create a python virtual environment and install the necessary dependencies.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run the `cli.py` file from your terminal and pass your phrase as `--query "<your-query>"`.

```bash
python cli.py --query "suggest an emoji for the word: tired"
```

## Acknowledgements

I would like to acknowledge the [owner](https://huggingface.co/badrex) of the `llm-emoji-dataset`.

## Contribution

Feel free to open up a pull request or an issue.
