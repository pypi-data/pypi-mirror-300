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
"""Command line entry point for calling trend_analyzer."""

import argparse

import langchain_google_genai
from gaarf.cli import utils as gaarf_utils
from gaarf.io import writer

from trend_analyzer import analyzer, llms, vectorstore


def main():  # noqa: D103
  parser = argparse.ArgumentParser()
  parser.add_argument('question')
  parser.add_argument('--llm', dest='llm')
  parser.add_argument('--output-type', dest='output', default='console')
  parser.add_argument(
    '--output-destination', dest='destination', default='results'
  )
  parser.add_argument('--samples-directory', dest='samples_directory')
  parser.add_argument('--db-path', dest='db')
  args, kwargs = parser.parse_known_args()
  params = gaarf_utils.ParamsParser(['llm', args.output]).parse(kwargs)

  trend_analyzer_llm = llms.create_trend_analyzer_llm(
    args.llm, params.get('llm')
  )
  trend_analyze_handler = analyzer.TrendsAnalyzer(
    vect_store=vectorstore.load_vectorstore(
      samples_directory=args.samples_directory,
      embedding_function=langchain_google_genai.GoogleGenerativeAIEmbeddings(
        model='models/embedding-001'
      ),
    ),
    llm=trend_analyzer_llm,
    db_uri=args.db,
  )
  result = trend_analyze_handler.analyze(args.question)
  writer.create_writer(args.output, **params.get(args.output)).write(
    result, args.destination
  )


if __name__ == '__main__':
  main()
