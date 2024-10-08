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
"""Provides HTTP endpoint for trend analysis."""

import os

import fastapi

from trend_analyzer import analyzer, llms, vectorstore

app = fastapi.FastAPI()

trend_analyzer_llm = llms.create_trend_analyzer_llm(
  llm_type=os.getenv('TRENDS_LLM', 'gemini'),
  llm_parameters={'model': 'gemini-1.5-flash'},
)
trend_analyze_handler = analyzer.TrendsAnalyzer(
  vect_store=vectorstore.get_vector_store(),
  llm=trend_analyzer_llm,
  db_uri=os.getenv('TRENDS_DATABASE_URI'),
)


@app.post('/')
def analyze(
  data: dict[str, str] = fastapi.Body(embed=True),
) -> dict[str, str]:
  """Answers question on trends.

  Args:
    data: Contains trends related question.

  Returns:
    Mapping with answer to the question.
  """
  response = trend_analyze_handler.analyze(data.get('question'))
  return {'response': response}
