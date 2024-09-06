---
title: How to use instructions
author: nirajkumar
description: This document provides instructions on how to use the application.
tags: how-to, instructions, usage,  guide, help, manual, reference, documentation, faq, tutorial.
---


# How to use the application

* setup python virtual environment
* Install dependencies `pip install -r requirement.txt`.
* Create a `.env` file and add the following environment variables

  ```bash
    OPENAI_API_KEY=your_openai_api_key
  ```
* Generate embeddings for the text data using the following command

  ```bash
    python generate_embeddings.py --pdf_path=path_to_pdf_file
  ```
  It will generate embeddings and give you a documents key which you can use to chat with the documents.
  example:
  ```bash
    docuemnt_id=20240905_165711
  ```

* Start the application using the following command

  ```bash
    python app.py --doc_id=20240905_165711 --query="your_query"
  ```

* The script will return the answer to your query.

