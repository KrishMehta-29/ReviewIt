from agents import Agent, Runner, WebSearchTool
import os
from dotenv import load_dotenv
import agentops
import asyncio
from app.auth import get_pull_request_diff

load_dotenv()

# Get AGENTOPS_API key from environment variables
AGENTOPS_API_KEY = os.getenv("AGENTOPS_API_KEY")

# Initialize AgentOps - this is all you need for automatic instrumentation
agentops.init(AGENTOPS_API_KEY)

# Create specialized agents
github_agent = Agent(
    name="github PR Summarizer Agent",
    instructions="""
    You are helpful AI agent that reads git diffs and creates a PR description.
    Make sure to explain each part of the diff. Do not explain parts that seem irrelevant.
    """,
    tools=[],
)


async def getAICallFromDiff(diff):
    try:
        # Run the agent - AgentOps will automatically track this
        diff = get_pull_request_diff("KrishMehta-29", "ReviewIt", 3)
        result = await Runner.run(github_agent, f"Here is the diff: {diff}")

        # Print the response to the user
        return result.final_output
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}\n")
        

# if __name__ == "__main__":
#     asyncio.run(main())