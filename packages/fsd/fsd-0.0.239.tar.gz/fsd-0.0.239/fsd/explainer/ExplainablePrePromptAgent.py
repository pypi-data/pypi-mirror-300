import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)
class ExplainablePrePromptAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_prePrompt_plan(self, user_prompt, file_attachments):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            user_prompt (str): The user's prompt.
            file_attachments (list): List of file paths attached by the user.

        Returns:
            dict: Development plan or error reason.
        """

        tree = self.repo.print_tree()
    
        messages = [
            {
                "role": "system",
                "content": (
                    "Analyze the user prompt, project structure, and attached files meticulously. Respond with a precise JSON format:\n\n"
                    "1. original_prompt_language: \n"
                    "   - Use explicitly specified language if provided.\n"
                    "   - Otherwise, accurately detect the language of the user's prompt.\n\n"
                    "2. processed_prompt: \n"
                    "   - Translate to English if not already in English.\n"
                    "   - Ensure clarity, conciseness, and preservation of original intent.\n\n"
                    "3. pipeline: \n"
                    "   - Choose '1' for:\n"
                    "     * Queries about specific project files\n"
                    "     * Code-related questions\n"
                    "     * Project-specific inquiries\n"
                    "   - Choose '2' for:\n"
                    "     * General, non-project-related questions\n"
                    "     * Non-code questions\n"
                    "     * Queries about already attached files without need for additional project context\n\n"
                    "4. role: \n"
                    "   - Determine the most appropriate expert role to address the query.\n"
                    "   - Examples: 'Senior C++ Engineer', 'iOS Development Expert', 'AI Ethics Specialist', etc.\n"
                    "   - Be specific and relevant to the question's domain.\n\n"
                    "Strict JSON Format:\n"
                    "{\n"
                    '    "role": "Specific Expert Title",\n'
                    '    "processed_prompt": "Clear, concise English version of the prompt",\n'
                    '    "original_prompt_language": "Detected or specified language",\n'
                    '    "pipeline": "1 or 2"\n'
                    "}\n\n"
                    "Ensure 100% valid JSON. No additional text or explanations outside the JSON structure."
                )
            },
            {
                "role": "user",
                "content": f"User prompt:\n{user_prompt}\n\nDetailed project structure:\n{tree}\n\nAttached files:\n{file_attachments}"
            }
        ]

        try:
            logger.debug("\n #### The `ExplainablePrePromptAgent` is initiating:\n A request to the AI for pre-prompt planning")
            response = await self.ai.prompt(messages, self.max_tokens, 0, 0)
            logger.debug("\n #### The `ExplainablePrePromptAgent` has successfully:\n Received the AI response for pre-prompt planning")
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            logger.debug("\n #### The `ExplainablePrePromptAgent` is attempting:\n To repair a JSON decoding error in the AI response")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.error(f"\n #### The `ExplainablePrePromptAgent` encountered an error:\n While getting the pre-prompt plan\n Error: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt, file_attachments):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `ExplainablePrePromptAgent` is beginning:\n The pre-prompt planning process")
        plan = await self.get_prePrompt_plan(user_prompt, file_attachments)
        logger.debug("\n #### The `ExplainablePrePromptAgent` has finished:\n The pre-prompt planning process")
        return plan
