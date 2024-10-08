# Trend Analyzer

## Problem statement

It's time consuming to understand the changes happening in competitive /
audience / creative landscapes without relying on heave pre-processing
and data analysis techniques.

## Solution

`trend-analyzer` uses power of large language models to analyze
trends data located to SQL database and make it  available for querying
with a simple chat bot interface.

## Deliverable (implementation)

`trend-analyzer` is implemented as a:

* **library** - Use it in your projects with a help of `TrendsAnalyzer` class.
* **CLI tool** - `trend-analyzer` tool is available to be used in the terminal.
* **HTTP endpoint** - `trend-analyzer` can be easily exposed as HTTP endpoint.
* **Langchain tool**  - integrated `trend-analyzer` into your Langchain applications.

## Deployment

### Prerequisites

- Python 3.11+
- A GCP project with billing account attached
- [Service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts#creating)
  created and [service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating)
  downloaded in order to write data to BigQuery.

  - Once you downloaded service account key export it as an environmental variable

    ```
    export GOOGLE_APPLICATION_CREDENTIALS=path/to/service_account.json
    ```

  - If authenticating via service account is not possible you can authenticate with the following command:
    ```
    gcloud auth application-default login
    ```
* [API key](https://support.google.com/googleapi/answer/6158862?hl=en) to access to access Google Gemini.
  - Once you created API key export it as an environmental variable

    ```
    export GOOGLE_API_KEY=<YOUR_API_KEY_HERE>
    ```


### Installation

Install `trend-analyzer` with `pip install trend-analyzer` command.

### Usage

> This section is focused on using `trend-analyzer` as a CLI tool.
> Check [library](docs/how-to-use-trend-analyzer-as-a-library.md),
> [http endpoint](docs/how-to-use-trend-analyzer-as-a-http-endpoint.md),
> [langchain tool](docs/how-to-use-trend-analyzer-as-a-langchain-tool.md)
> sections to learn more.

Once `trend-analyzer` is installed you can call it:

```
trend-analyzer 'YOUR_QUESTION_HERE' \
  --llm gemini \
  --llm.model=gemini-1.5-flash \
  --db-uri=<DATABASE_URI> \
  --output-type csv \
  --output-destination sample_results
```
where:

* `YOUR_QUESTION_HERE` - trends related question you want to ask.
*  `--llm gemini` - type of large language model (currently only Google Gemini is supported).
*  `--llm.model=gemini-1.5-flash` - any parameters to initialize selected LLM.
*  `--db-uri=<DATABASE_URI>` - location of database with trends data.
* `--output-type csv` - type of output.
* `--output-destination sample_results` - name of output table or file.


## Disclaimer
This is not an officially supported Google product.
