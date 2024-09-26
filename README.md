# IconGPT 🤖

A tool to generate an emoji based on an emotion, sentence, phrase or even a single word. Implements simple RAG on the [`llm-emoji-dataset`](https://huggingface.co/datasets/badrex/llm-emoji-dataset) by using MongoDB Atlas Vector search for semantic similarity.

## Run locally on CLI

Clone the GitHub repository and navigate to the root folder.

```bash
git clone <repo-link>
cd emoGPT
```

Create a python virtual environment and install the necessary dependencies.

```bash
python -m venv .<env-name>
venv\Scripts\activate
python -m pip install -r requirements.txt
```

### Test FastAPI endpoint

Ping the `/search` endpoint by running `app.py` via FastAPI CLI or uvicorn.

```bash
fastapi dev app.py
```

Either use the interactive API docs or ping the endpoint by making a request via `cURL` or `requests`.

```bash
curl -X POST http://<host>:<port>/search -H "Content-type: application/json" -d '{"query": "<your-query>"}'
```

## Acknowledgements

I would like to acknowledge the [owner](https://huggingface.co/badrex) of the `llm-emoji-dataset`.

## Contribution

Feel free to open up a pull request or create an issue.
