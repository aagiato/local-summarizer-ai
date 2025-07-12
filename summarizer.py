import logging
import json
from chunking import chunk_text_by_words
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# Initialize logging
logging.basicConfig(
    filename='summarizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")

def query_claude(prompt: str) -> str:
    try:
        body = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000
        }

        response = bedrock.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(response['body'].read())
        return result['content'][0]['text']

    except (BotoCoreError, ClientError) as e:
        logging.error(f"AWS error during model invocation: {e}")
        return "[ERROR: AWS model invocation failed]"
    except Exception as e:
        logging.error(f"General error during query_claude: {e}")
        return "[ERROR: Unknown summarization failure]"

def summarize_chunks(text: str) -> str:
    try:
        chunks = chunk_text_by_words(text)
        logging.info(f"Document split into {len(chunks)} chunks.")

        summaries = []
        for idx, chunk in enumerate(chunks):
            logging.info(f"Summarizing chunk {idx + 1}/{len(chunks)}...")
            summary = query_claude(f"Summarize this:\n\n{chunk}")
            summaries.append(summary)

        return "\n\n".join(summaries)

    except Exception as e:
        logging.error(f"Error during summarization process: {e}")
        return "[ERROR: Could not summarize text]"

