import boto3
import json

# Set up Bedrock client
bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")

def query_claude(prompt):
    body = {
        "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
        "max_tokens_to_sample": 1000,
        "temperature": 0.5,
        "top_k": 250,
        "top_p": 1,
        "stop_sequences": ["\n\nHuman:"]
    }

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response['body'].read())
    return result['completion']

# Test it
print(query_claude("Summarize the financials of a mid-stage startup with $10M ARR and 30% YoY growth."))

!pip install boto3 pandas langchain