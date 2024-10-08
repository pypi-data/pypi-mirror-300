# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module for defining vector store.

Vectorstore contains necessary data to improve LLM results.
"""

from __future__ import annotations

import dataclasses
import itertools
import json
import pathlib
from collections.abc import Sequence
from typing import TypeAlias, TypedDict

import chromadb
import langchain_chroma
import langchain_text_splitters
import pandas as pd
from langchain_community import document_loaders, embeddings
from langchain_core import vectorstores


class TrendDocumentDict(TypedDict):
  """Specifies fields in trends document."""

  results: dict[str, str | TrendData]


TrendData: TypeAlias = dict[str, dict[str, float]]


@dataclasses.dataclass(frozen=True)
class JsonConversionSchema:
  """Specifies conversion from CSV to JSON.

  Each field corresponds to column name in a DataFrame built from CSV.

  Attributes:
    date: Name of a column containing trend document date.
    primary_key: Name of a column with unique topic identifier.
    primary_growth_metric: Name of a column with growth metric.
    metric_volume: Name of a column with volume metric.
  """

  date: str
  # trend_type: str
  primary_key: str = 'topic'
  primary_growth_metric: str = 'qoq_growth'
  metric_volume: str = 'index'
  # optional_dimensions: list[str] = dataclasses.field(default_factory=list)
  # optional_metrics: list[str] = dataclasses.field(default_factory=list)


def get_vector_store(
  vectorstore_type: vectorstores.VectorStore = langchain_chroma.Chroma,
  vector_store_directory: str = './../assistant_db',
  embedding_function=embeddings.FakeEmbeddings(size=1352),
):
  """Loads or creates vectorstore.

  Args:
    vectorstore_type: Type of vectorstore to initialize.
    vector_store_directory: Directory with persist vectorstore.
    embedding_function: Function for document embeddings.

  Returns:
    Initialized and populated vectorstore.
  """
  if not vector_store_directory:
    return load_vectorstore(
      vectorstore_type, vector_store_directory, embedding_function
    )
  return vectorstore_type(
    persist_directory=vector_store_directory,
    embedding_function=embedding_function,
    client_settings=chromadb.config.Settings(anonymized_telemetry=False),
  )


def load_vectorstore(
  vectorstore_type: vectorstores.VectorStore = langchain_chroma.Chroma,
  samples_directory: pathlib.Path | str | None = None,
  embedding_function=embeddings.FakeEmbeddings(size=1352),
  json_conversion_schema: JsonConversionSchema = JsonConversionSchema(
    date='date',
    primary_key='topic',
    primary_growth_metric='qoq_growth',
    metric_volume='index',
  ),
) -> langchain_chroma.Chroma:
  """Creates vectorstore from documents and embeddings.

  Args:
    vectorstore_type: Type of vectorstore to initialize.
    samples_directory: Directory with trend documents.
    embedding_function: Function for document embeddings.
    json_conversion_schema: Schema for parsing CSV files to JSON.

  Returns:
    Initialized and populated vectorstore.
  """
  if not samples_directory:
    samples_directory = pathlib.Path(__file__).resolve().parent / 'files'
  if isinstance(samples_directory, str):
    samples_directory = pathlib.Path(samples_directory)
  convert_csv_to_json(json_conversion_schema, samples_directory)
  splits = []
  for file in samples_directory.iterdir():
    if file.is_file() and file.suffix == '.json':
      loader = document_loaders.JSONLoader(
        file_path=file, jq_schema='.results', text_content=False
      )
      docs = loader.load()

      text_splitter = (
        langchain_text_splitters.character.RecursiveCharacterTextSplitter(
          chunk_size=1000, chunk_overlap=200
        )
      )
    splits.append(text_splitter.split_documents(docs))
  return vectorstore_type.from_documents(
    documents=itertools.chain.from_iterable(splits),
    embedding=embedding_function,
  )


def convert_csv_to_json(
  json_conversion_schema: JsonConversionSchema,
  samples_directory: pathlib.Path,
) -> None:
  """Prepares documents according to json schema.

  Args:
    json_conversion_schema: Schema for parsing CSV file.
    samples_directory: Directory with trend documents.
  """
  for file in samples_directory.iterdir():
    if file.is_file() and file.suffix == '.csv':
      result = _transform_to_json(file, json_conversion_schema)
      with open((file.parent / file.stem).with_suffix('.json'), 'w') as f:
        json.dump(result, f)


def _transform_to_json(
  file: pathlib.Path,
  json_conversion_schema: JsonConversionSchema,
  trend_type: str = 'search trends',
) -> TrendDocumentDict:
  """Converts CSV file to Json according to schema.

  Args:
    file: Path to a CSV file.
    json_conversion_schema: Schema for parsing CSV file.
    trend_type: Type of trend document.

  Returns:
    CSV converted to dictionary.
  """
  df = pd.read_csv(file)
  if missing_fields := _is_convertable_to_json(df, json_conversion_schema):
    raise IncorrectCsvTrendInputError(f'Missing fields: {missing_fields}')
  trends_date = df[json_conversion_schema.date][0]
  result = {'results': {'date': trends_date, 'type': trend_type, 'data': {}}}
  for row in df.itertuples():
    result['results']['data'][
      getattr(row, json_conversion_schema.primary_key)
    ] = _build_trend_mapping(row, json_conversion_schema)

  return result


def _is_convertable_to_json(
  df: pd.DataFrame, json_conversion_schema: JsonConversionSchema
) -> set[str]:
  """Validates whether all fields of schema are found in DataFrame.

  Args:
    df: DataFrame with trends.
    json_conversion_schema: Schema for parsing DataFrame.

  Returns:
    Fields missing from schema are in DataFrame columns.
  """
  return set(dataclasses.asdict(json_conversion_schema).values()).difference(
    df.columns
  )


def _build_trend_mapping(
  row: pd.Series,
  json_conversion_schema: JsonConversionSchema,
  extracted_fields: Sequence[str] = ('metric_volume', 'primary_growth_metric'),
) -> dict[str, str]:
  """Extracts fields based on json conversion schema.

  Args:
    row: Row of pandas DataFrame.
    json_conversion_schema: Schema for parsing rows.
    extracted_fields: Fields to be extracted from schema.

  Returns:
    Mapping between each extracted field and its value.
  """
  return {
    getattr(json_conversion_schema, field): getattr(
      row, getattr(json_conversion_schema, field)
    )
    for field in extracted_fields
  }


class IncorrectCsvTrendInputError(Exception):
  """Raised when not all fields can be found in CSV file."""
