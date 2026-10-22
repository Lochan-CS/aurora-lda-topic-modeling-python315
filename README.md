# Aurora LDA Studio — Python 3.15

A **different frontend and backend** for the LDA lab exercise: an editorial-style **light dashboard** with a navy sidebar, blue/lilac accents, metrics, topic bars, and a document affinity table.

## Requirements

- Python **3.15** (also works on recent Python 3 versions)
- VS Code or any terminal
- **No pip installs required**. The entire backend uses the Python standard library.
- Internet access is optional; Google Fonts are loaded only if available, otherwise local fonts are used.

## Run

1. Extract this ZIP.
2. In VS Code, select **File → Open Folder** and open `aurora_lda_py315`.
3. Open **Terminal → New Terminal**.
4. Run:

   ```bash
   python server.py
   ```

5. Visit **http://127.0.0.1:8000**.
6. Click **Run topic discovery** to display the top five words of each topic.
7. Stop with **Ctrl+C**.

If `python` does not select the correct interpreter on Windows, use `py -3.15 server.py`.

## Tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

## Project files

- `server.py` — dependency-free HTTP server and JSON API
- `lda_engine.py` — actual collapsed Gibbs sampling LDA algorithm
- `index.html` — application layout
- `static/style.css` — light-theme responsive design
- `static/app.js` — browser interaction and safe result rendering
- `tests/test_engine.py` — standard-library unit tests

## How the algorithm works

The application lowercases text, removes common English stopwords, and creates a token vocabulary. It then initializes topic assignments and runs 160 collapsed Gibbs sampling iterations to estimate the topic-word and document-topic distributions. It returns the top five words by topic-word probability and the dominant topic of each document.

**Important:** LDA is an unsupervised probabilistic model. Topic labels are arbitrary; topic proportions are not supervised accuracy scores. With very small corpora, mixed topics are expected.

## Python 3.15 note

This project deliberately avoids third-party packages such as scikit-learn and Flask, whose availability can vary with new Python versions. It implements LDA directly using Python's standard library. The source and unit tests were checked in the available environment; execution on an actual Python 3.15 installation should be verified locally.
