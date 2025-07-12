# insight-summarizer-ai# Insight Summarizer AI

Insight Summarizer AI is a fully AWS-hosted application designed to automatically parse, chunk, and summarize long-form financial documents using Anthropic's Claude 3 Sonnet via Amazon Bedrock. The tool is built with scalability and robustness in mind and is ideal for summarizing startup financials, investor memos, and operational reports.

## Project Overview

This tool performs the following:

- Accepts PDF or plain text documents
- Breaks down large text into manageable chunks using a word-based strategy
- Sends each chunk to Claude 3 Sonnet via Amazon Bedrock for summarization
- Returns and compiles the summarized output for user review

## Directory Structure

insight-summarizer-ai/
├── chunking.py # Handles splitting text into word-based chunks
├── load_and_chunk.py # Loads documents and applies chunking
├── summarizer.py # Orchestrates chunking and summarization
├── bedrock_claude_client.py # Connects to Amazon Bedrock and calls Claude
├── data/ # Directory for input documents
├── .gitignore # Ignores unnecessary or sensitive files
└── README.md # Project documentation


## Technology Stack

- **Language**: Python 3.10
- **Core AWS Services**:
  - Amazon Bedrock (Claude 3 Sonnet)
  - Amazon SageMaker (Notebook environment)
  - AWS IAM (for permissions and roles)
- **Libraries**:
  - `boto3` for AWS interaction
  - `pandas` for data handling
  - `langchain` for potential LLM tooling
  - `unstructured` for text extraction from files

## Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/aagiato/insight-summarizer-ai.git
   cd insight-summarizer-ai

    (Optional) Create a new Python environment:

conda create -n insight-summarizer-ai python=3.10
conda activate insight-summarizer-ai

Install dependencies:

pip install boto3 pandas langchain unstructured

Configure AWS credentials if running locally:

    aws configure

    If using SageMaker, ensure your IAM role has the necessary permissions.

    Run the notebook or script depending on your environment:

        In SageMaker: run the cells in the notebook version of summarizer.py

        In local development: run summarizer.py via the command line or IDE

IAM Permissions Required

Ensure that the executing user or SageMaker role has the following permissions:

    bedrock:InvokeModel

    sagemaker:* (if using SageMaker fully)

    logs:* (if logging is enabled)

    Optional: s3:GetObject, s3:PutObject if using S3 for storage

Budget and Cost Controls

A budget has been configured in AWS to trigger alerts once spending reaches $100. This is monitored via AWS Budgets and (optionally) SNS. You can also stop the SageMaker instance when not in use to limit compute costs.
Next Steps

    Add persistent output storage (e.g., S3)

    Enable batch processing of documents

    Implement a user interface or API endpoint

    Support more document types and automatic metadata extraction

Author

Andrew Agiato
GitHub: @aagiato
