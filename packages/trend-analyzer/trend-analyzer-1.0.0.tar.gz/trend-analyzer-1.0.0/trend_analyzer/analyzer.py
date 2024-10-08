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

import gaarf
import langchain_community
import smart_open
from langchain import chains
from langchain.chains.sql_database import prompt as sql_prompts
from langchain_community.tools.sql_database import tool as sql_database_tool
from langchain_core import (
  language_models,
  output_parsers,
  prompts,
  runnables,
  vectorstores,
)


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
    prompt = sql_prompts.SQL_PROMPTS[self.db.dialect].partial(
      table_info=self.db.get_context()['table_info']
    )
    prompt = prompt + '\nNever do joins unless explicitly asked.'
    return (
      chains.create_sql_query_chain(llm=self.llm, db=self.db, prompt=prompt)
      | self._query_cleaner
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
    )

  def analyze(self, text: str) -> gaarf.report.GaarfReport:
    """Performs trend analysis based on a provided question.

    Args:
      text: Question to LLM.

    Returns:
      Report with trends data.
    """
    question = {'question': text}
    sql_chain = runnables.RunnablePassthrough.assign(
      query=self.write_query
    ).assign(result=operator.itemgetter('query') | self.execute_query)
    chain = (
      sql_chain | self.prompt | self.llm | output_parsers.StrOutputParser()
    )
    return chain.invoke(question)
