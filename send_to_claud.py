import boto3
import json

# Load your chunks
from load_and_chunk import chunk_text_by_words, load_file

# Constants
model_id = "anthropic.claude-3-sonnet-20240229-v1:0"  # Claude 3.7 Sonnet
region = "us-east-1"  # Adjust if needed
file_path = "PATH/TO/YOUR/FILE.pdf"

def main():
    # Load and chunk the document
    text = load_file(file_path)
    chunks = chunk_text_by_words(text)

    # Create Bedrock client
    bedrock = boto3.client("bedrock-runtime", region_name=region)

    for i, chunk in enumerate(chunks[:3]):  # Just send first 3 for testing
        prompt = f"""
        Human: Summarize the following financial document chunk:

        {chunk}

        Assistant:"""

        body = json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 1024,
            "temperature": 0.3,
            "top_k": 250,
            "top_p": 0.999
        })

        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body
        )

        result = json.loads(response['body'].read())
        print(f"\n--- Summary for chunk {i+1} ---\n")
        print(result["completion"])

if __name__ == "__main__":
    main()