#!/bin/bash


query=${1:-"what is it about?"}
doc_id=${2:-"20240905_215312"}
from=${3:-"data/embeddings.json"}

echo "query: ${query}"
echo "doc_id: ${doc_id}"
echo "from: ${from}"

python -m src.app --query="${query}" --doc_id="${doc_id}" --from="${from}"
