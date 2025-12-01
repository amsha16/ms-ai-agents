import os
from dotenv import load_dotenv
import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import UserMessage
from autogen_ext.models.azure import AzureAIChatCompletionClient
from azure.core.credentials import AzureKeyCredential
from autogen_core import CancellationToken

from autogen_agentchat.messages import TextMessage
from autogen_agentchat.ui import Console

async def process_request(user_prompt: str):
    load_dotenv()
    client = AzureAIChatCompletionClient(
        model="gpt-4o-mini",
        endpoint="https://models.inference.ai.azure.com",
        # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings.
        # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
        credential= AzureKeyCredential(os.getenv("GITHUB_TOKEN")),
        model_info={
            "json_output": True,
            "function_calling": True,
            "vision": True,
            "family": "unknown",
            "structured_output":True
        },
    )
    
    result = await client.create([UserMessage(content=user_prompt, source="user")])
    print(result)
    await client.close()


async def main():
    
    # Ask for a prompt
    user_prompt = input(f"How can I help you?\n")
    
    # Run the async agent code
    await process_request (user_prompt)

if __name__ == "__main__":
    asyncio.run(main())
    
