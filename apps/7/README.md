---
author: pallawi
title: How to use instructions
layout: page
---

## GenAI AskPDF

### setup environment variable


```bash
OPENAI_API_KEY=sk-<your-openai-api-key>
FILE_UPLOAD_PATH=<path-to-upload-file>
```

OR 
Add the following key into `export.sh` file. 
```bash
export OPENAI_API_KEY=sk-<your-open
export FILE_UPLOAD_PATH=<path-to-upload-file>
```

source the file using the following command


```bash
source export.sh
```

### Install dependency

```bash
pip install -r requirements/install.txt
```

### Run the server

```bash
python app.py
```

### API

- **URL**: `http://localhost:5000`

