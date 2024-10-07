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
"""Module for performing trends analysis.

Exposes a single class TrendAnalyzer that allows to get extract trends from
vector store based on provided LLM.
"""

from __future__ import annotations

import operator
import pathlib
import re
from collections.abc import Mapping, MutableSequence

import gaarf
import langchain_community
import smart_open
from langchain import chains
from langchain_community.tools.sql_database import tool as sql_database_tool
from langchain_core import (
  language_models,
  output_parsers,
  prompts,
  pydantic_v1,
  runnables,
  vectorstores,
)


class Trend(pydantic_v1.BaseModel):
  """Defines structured output for LLM.

  Attributes:
    name: Name of the trend.
    growth: Relative growth associated with trend.
  """

  name: str = pydantic_v1.Field(description='topic name')
  growth: float = pydantic_v1.Field(description='topic growth or qoq_growth')


def _format_docs(docs):
  return '\n\n'.join(doc.page_content for doc in docs)


class TrendsAnalyzer:
  """Handles prompts related to analyzing trends.

  Attributes:
    vect_store: Vector store containing data on trends.
    llm: LLM responsible to handle prompts.
    db_uri: SqlAlchemy based uri for creating DB connection.
  """

  def __init__(
    self,
    vect_store: vectorstores.VectorStore,
    llm: language_models.BaseLanguageModel,
    db_uri: str,
  ) -> None:
    """Initializes TrendsAnalyzer.

    Args:
      vect_store: Vector store containing data on trends.
      llm: LLM responsible to handle prompts.
      db_uri: SqlAlchemy based uri for creating DB connection.
    """
    self.vect_store = vect_store
    self.llm = llm
    self.db_uri = db_uri

  @property
  def db(self) -> langchain_community.utilities.SQLDatabase:
    """Creates db from saved uri."""
    return langchain_community.utilities.SQLDatabase.from_uri(self.db_uri)

  @property
  def execute_query(self) -> sql_database_tool.QuerySQLDataBaseTool:
    """Tool responsible for executing SQL queries."""
    return sql_database_tool.QuerySQLDataBaseTool(db=self.db)

  def _query_cleaner(self, text: str) -> str:
    """Ensures that queries is extracted correctly from response."""
    if 'sqlquery' in text.lower() and (
      query_match := re.search('sqlquery: select .+$', text, re.IGNORECASE)
    ):
      return query_match.group(0).split(': ')[1]
    return text.split('\n')[1]

  @property
  def write_query(self):
    """Tool responsible for generating and cleaning SQL queries."""
    return (
      chains.create_sql_query_chain(self.llm, self.db) | self._query_cleaner
    )

  @property
  def prompt(self) -> prompts.PromptTemplate:
    """Builds correct prompt to send to LLM.

    Prompt contains format instructions to get output result.
    """
    with smart_open.open(
      pathlib.Path(__file__).resolve().parent / 'prompt_template.txt',
      'r',
      encoding='utf-8',
    ) as f:
      template = f.readlines()
    return prompts.PromptTemplate(
      template=' '.join(template),
      input_variables=['question'],
      # partial_variables={
      #   'format_instructions': self.output_parser.get_format_instructions(),
      # },
    )

  @property
  def output_parser(self) -> output_parsers.BaseOutputParser:
    """Defines how LLM response should be formatted."""
    return output_parsers.JsonOutputParser(pydantic_object=Trend)

  def analyze(self, text: str) -> gaarf.report.GaarfReport:
    """Performs trend analysis based on a provided question.

    Args:
      text: Question to LLM.

    Returns:
      Report with trends data.
    """
    chain = (
      runnables.RunnablePassthrough.assign(query=self.write_query).assign(
        result=operator.itemgetter('query') | self.execute_query
      )
      | self.prompt
      | self.llm
      | output_parsers.StrOutputParser()


    )
    return chain.invoke({'question': text})

  def _format_llm_response(
    self, response: Mapping[str, str] | MutableSequence[Mapping[str, str] | str]
  ) -> gaarf.report.GaarfReport:
    """Ensures that response from LLM is properly formatted to GaarfReport."""
    if isinstance(response, Mapping):
      results = [list(response.values())]
    else:
      results = []
      for row in response:
        if isinstance(row, Mapping):
          results.append([*row.values()])
        else:
          results.append([row])
    column_names = list(
      self.output_parser.pydantic_object.__annotations__.keys()
    )
    return gaarf.report.GaarfReport(results=results, column_names=column_names)
