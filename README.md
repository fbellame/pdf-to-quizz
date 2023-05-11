# PDF to Quiz

Upload a multiple page PDF and generate a quiz with multiple options. For each page 2 questions will be generated.

This leverage Langchain library to abstract the LLM (Large Language Model) calls.

The UI is based on Streamlit

Here is an exemple PDF (sorry in french but you can get the idea...)

![PDF sample](img/PDF-sample.png)

Will generate the following interractive quiz questions:

![PDF sample](img/quiz-reponse.png)


## Pre-requisite

You need an OpenAI API key from https://platform.openai.com/account/api-keys

Keep in mind this is not free BUT the with the usage of **gpt-3.5-turbo** it's not expensive at all unless you drop really big PDF (more than 100 pages).

![Open AI key](img/OPENAI-KEY.png)

Once you have your API key you can install it in your terminal like this:

``` sh
export OPENAI_API_KEY=[Your-API-key]
```


## Instructions


To install:
``` sh
pip install -r requirements.txt
```

## Run



To run:
```sh
streamlit run ui.py
```

To run on docker
```sh
docker build -t pdf-to-quizz .
docker run -e OPENAI_API_KEY=[your-api-key] -p 8501:8501 pdf-to-quizz
```
