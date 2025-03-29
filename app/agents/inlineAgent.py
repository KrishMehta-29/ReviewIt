from agents import Runner, function_tool, RunContextWrapper, FunctionTool
import asyncio
from openai import OpenAI
from app.github.beans import InlineComment
import json 


openAITool = {
      "type": "function",
      "name": "post_inline_comments_to_github",
      "description": "Creates a review comment on a GitHub pull request.",
      "parameters": {
        "type": "object",
        "required": [
          "file",
          "line",
          "comment"
        ],
        "properties": {
          "file": {
            "type": "string",
            "description": "The name of the file to which the comment will be added."
          },
          "line": {
            "type": "number",
            "description": "The line number in the file where the comment should be placed. It uses githubs position parameter, so format the line input correctly."
          },
          "comment": {
            "type": "string",
            "description": "The content of the comment to be added."
          }
        },
        "additionalProperties": False
      },
      "strict": True
    }


# Function to run the agent and get PR comments for a given diff
def getAgentInlinePRCommentsForDiff(diff: str) -> str:

    client = OpenAI()

    response = client.responses.create(
    model="gpt-4o",
    input=[
        {
        "role": "system",
        "content": [
            {
            "type": "input_text",
            "text": f"You are a staff software engineer, with loads of experience reviewing code. Your task will be given a PR diff, to review the diff, and adding inline comments using the post_inline_comments_to_github function. I want you to be critical, catch edgecases and add as many comments as needed to ensure that only the best quality code is pushed. Here is the diff: {diff}"
            }
        ]
        }
    ],
    text={
        "format": {
        "type": "text"
        }
    },
    reasoning={},
    tools=[
        openAITool
    ],
    temperature=1,
    max_output_tokens=16384,
    top_p=1,
    store=True
    )

    commentsToCreate = []
    for output in response.output:
        args = output.arguments
        argsJson = json.loads(args)
        comment = InlineComment(file=argsJson['file'], content=argsJson['comment'], line=argsJson['line'])
        commentsToCreate.append(comment)
    return commentsToCreate

# async def _getAgentInlinePRCommentsForDiff(diff: str) -> str:
#     try:
#         # Run the agent with the provided diff
#         result = await Runner.run(inline_code_comment_agent, f"Here is the diff: {diff}")

#         for item in result.new_items:
#             print(item)

#         return result.final_output
#     except Exception as e:
#         print(f"\nAn error occurred: {str(e)}\n")
#         return ""