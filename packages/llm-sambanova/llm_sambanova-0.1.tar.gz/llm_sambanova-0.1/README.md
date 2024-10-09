# llm-sambanova

[![PyPI](https://img.shields.io/pypi/v/llm-sambanova.svg)](https://pypi.org/project/llm-sambanova/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-sambanova?include_prereleases&label=changelog)](https://github.com/simonw/llm-sambanova/releases)
[![Tests](https://github.com/simonw/llm-sambanova/workflows/Test/badge.svg)](https://github.com/simonw/llm-sambanova/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-sambanova/blob/main/LICENSE)

[LLM](https://llm.datasette.io/) plugin for models hosted by [SambaNova](https://sambanova.ai/)

## Installation

First, [install the LLM command-line utility](https://llm.datasette.io/en/stable/setup.html).

Now install this plugin in the same environment as LLM.
```bash
llm install llm-sambanova
```

## Configuration

You will need an API key from SambaNova. You can [obtain one here](https://sambanova.ai/keys).

You can set that as an environment variable called `OPENROUTER_KEY`, or add it to the `llm` set of saved keys using:

```bash
llm keys set sambanova
```
```
Enter key: <paste key here>
```

## Usage

To list available models, run:
```bash
llm models list
```
You should see a list that looks something like this:
```
SambaNova: sambanova/Meta-Llama-3.2-1B-Instruct
SambaNova: sambanova/Meta-Llama-3.2-3B-Instruct
SambaNova: sambanova/Meta-Llama-3.1-8B-Instruct
SambaNova: sambanova/Meta-Llama-3.1-8B-Instruct-8k
SambaNova: sambanova/Meta-Llama-3.1-70B-Instruct
SambaNova: sambanova/Meta-Llama-3.1-70B-Instruct-8k
SambaNova: sambanova/Meta-Llama-3.1-405B-Instruct
SambaNova: sambanova/Meta-Llama-3.1-405B-Instruct-8k
SambaNova: sambanovacompletion/Meta-Llama-3.2-1B-Instruct
SambaNova: sambanovacompletion/Meta-Llama-3.2-3B-Instruct
SambaNova: sambanovacompletion/Meta-Llama-3.1-8B-Instruct
SambaNova: sambanovacompletion/Meta-Llama-3.1-8B-Instruct-8k
SambaNova: sambanovacompletion/Meta-Llama-3.1-70B-Instruct
SambaNova: sambanovacompletion/Meta-Llama-3.1-70B-Instruct-8k
SambaNova: sambanovacompletion/Meta-Llama-3.1-405B-Instruct
SambaNova: sambanovacompletion/Meta-Llama-3.1-405B-Instruct-8k
...
```
To run a prompt against a model, pass its full model ID to the `-m` option, like this:
```bash
llm -m sambanova/Meta-Llama-3.2-1B-Instruct "Five spooky names for a pet tarantula"
```
You can set a shorter alias for a model using the `llm aliases` command like so:
```bash
llm aliases set 405 sambanova/Meta-Llama-3.1-405B-Instruct
```
Now you can prompt Claude using:
```bash
cat llm_sambanova.py | llm -m 405 -s 'write some pytest tests for this'
```
## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-sambanova
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
pytest
```
