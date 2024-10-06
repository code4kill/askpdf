"""CLI tool using Click for interacting with PDF queries."""

import os
import click
import logging
import json
from .app import main

log = logging.getLogger(__name__)
this_dir = os.path.dirname(__file__)

def echo(d):
  """Echo logs for debugging."""
  log.info("__main__: default_root: {}".format(d))


@click.command()
@click.option('--query', type=str, required=True, help='Query to search in the document.')
@click.option('--doc_id', type=str, required=True, help='Document ID to search within.')
@click.option('--threshold', default=0.5, show_default=True, help='Threshold for search relevance.')
@click.option('--from_path', type=click.Path(exists=True), required=True, help='Embedding path for the document.')
def askpdf(query, doc_id, threshold, from_path):
  """Command to query PDFs with specified parameters."""
  kwargs = {
    'query': query,
    'doc_id': doc_id,
    'threshold': threshold,
    'from_path': from_path
  }
  main(kwargs)


@click.command()
def welcome():
  """Simple welcome command."""
  click.echo('Welcome to the PDF Query CLI!')
