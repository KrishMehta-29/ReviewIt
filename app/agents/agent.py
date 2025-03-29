from agents import Agent, Runner
import asyncio

githubAgent = Agent(
    name="github PR Summarizer Agent",
    instructions="""
    You are helpful AI agent that reads git diffs and creates a PR description.
    Make sure to explain each part of the diff. Do not explain parts that seem irrelevant.
    """,
    tools=[],
)

def getAgentPRCommentsForDiff(diff) -> str:
    return asyncio.run(_getAgentPRCommentsForDiff(diff))

async def _getAgentPRCommentsForDiff(diff) -> str:
    try:
        # Run the agent - AgentOps will automatically track this
        result = await Runner.run(githubAgent, f"Here is the diff: {diff}")
    
        # Print the response to the user
        return result.final_output
        
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}\n")
        