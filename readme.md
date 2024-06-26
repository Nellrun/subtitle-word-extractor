# Subtitle Word Extractor and Translator

This repository contains a Python script that processes subtitle files to extract words, lemmatize them, and translate them from Spanish to English. The script outputs each word with its translation and the context in which it appeared.

## Features

- Extracts words from subtitle files
- Lemmatizes words to their base form
- Translates words from Spanish to English using Google Translate API
- Outputs each word with its translation and context

## Requirements

- Python 3.7+
- `pysrt` for reading subtitle files
- `spacy` for natural language processing
- `aiohttp` for asynchronous HTTP requests

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/nellrun/subtitle-word-extractor.git
    cd subtitle-word-extractor
    ```

2. Create a virtual environment and activate it:
    ```sh
    make install
    ```

3. Install language model:
    ```sh
    ./venv/bin/python -m spacy download es_core_news_sm # your model
    ```

## Example

Here is an example of what the output might look like:
```
Spanish: hola | English: hello | Context: Hola, ¿cómo estás?
Spanish: cómo | English: how | Context: Hola, ¿cómo estás?
Spanish: estar | English: be | Context: Hola, ¿cómo estás?
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [pysrt](https://github.com/byroot/pysrt)
- [spaCy](https://spacy.io/)
- [aiohttp](https://aiohttp.readthedocs.io/)
- [Google Translate](https://cloud.google.com/translate)
