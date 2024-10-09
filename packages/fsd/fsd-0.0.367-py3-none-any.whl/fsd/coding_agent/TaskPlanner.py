import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class TaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        """
        Initialize the TaskPlanner with necessary configurations.

        Args:
            directory_path (str): Path to the project directory.
            api_key (str): API key for authentication.
            endpoint (str): API endpoint URL.
            deployment_id (str): Deployment ID for the AI model.
            max_tokens (int): Maximum number of tokens for AI responses.
        """
        self.max_tokens = 4096
        self.repo = repo
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, file_list, original_prompt_language):
        """
        Get a development plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for task planning.
            file_list (list): List of available files.
            original_prompt_language (str): The language of the original prompt.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `TaskPlanner` is initiating the process to generate a task plan")
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a principal engineer specializing in Pyramid architecture. Generate an ordered list of tasks for implementing a system following Pyramid best practices based on the user's instruction and provided file list. Break down the implementation into smaller, manageable chunks, ensuring each task builds context for subsequent tasks.\n\n"
                    "Guidelines:\n"
                    "1. **Task Breakdown:** Split the implementation into smaller, focused tasks.\n"
                    "2. **Context Building:** Order tasks to build context progressively.\n"
                    "3. **File Selection:** Only include files from the provided `file_list`.\n"
                    "4. **Pyramid Structure:** Follow Pyramid architecture principles in task ordering.\n"
                    "5. **Iterative Approach:** It's acceptable to work on the same file multiple times, but avoid overkill.\n"
                    "6. **UI Emphasis:** For UI-related tasks, always mention 'nice, elegant UI'.\n"
                    "7. **File Structure:** For each task, provide `file_name` (full path), `techStack`, `need_data`, and `prompt`.\n"
                    "8. **Integration:** Ensure each task integrates seamlessly with others for maintainability and scalability.\n"
                    "9. **Exclusions:** Omit configuration, dependencies, and non-essential files. Exclude all image files except `.svg` and all audio asset files.\n"
                    "10. **Assets:** Include only asset files with the `.svg` extension.\n"
                    "11. **Data Requirement:** Set `need_data` to True only if the specific task and file being worked on require data from the original instruction, False otherwise.\n"
                    "12. **Prompt:** For SVG files, provide a highly detailed description. For all other files, keep the prompt brief to indicate the task's purpose.\n"
                    "13. **SVG Files:** For SVG files, provide a highly detailed description including precise size, comprehensive color scheme, intricate image content, specific purpose (e.g., social icon, logo), intended placement, visual elements, functionality, design attributes, and integration with the overall design. Aim for a professional, elegant, and clean design while providing explicit instructions.\n"
                    "Response Format:\n"
                    "Provide a JSON object in the following structure:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "/full/path/to/file",\n'
                    '            "techStack": "python",\n'
                    '            "need_data": true,\n'
                    '            "prompt": "Brief description for non-SVG files, detailed for SVG files"\n'
                    '        },\n'
                    '    ]\n'
                    "}\n\n"
                    "Important: Respond with only the specified JSON content. Do not include additional text, explanations, or Markdown formatting. Ensure tasks are correctly ordered according to Pyramid architecture best practices for optimal integration and maintainability.\n\n"
                    f"Current working project is {self.repo.get_repo_path()}\n\n"
                    "Return only valid JSON without Markdown symbols or invalid escapes."
                )
            },
            {
                "role": "user",
                "content": f"Create an ordered list of tasks to implement following Pyramid architecture best practices. Break down the implementation into smaller, manageable chunks, ensuring each task builds context for subsequent tasks. Only select files from this list:\n{file_list}\n\nInclude the `file_name` (full path), `techStack`, `need_data`, and `prompt` for each task in the specified JSON format. Ensure that the `file_name` respects the root path and the correct relative path from the original instruction. Set `need_data` to true only if the specific task and file being worked on require data from the original instruction, false otherwise, using Python's valid boolean syntax. For the `prompt` field, provide a brief description for non-SVG files, indicating the task's purpose. For SVG files, include a highly detailed description as specified in the guidelines. For UI-related tasks, always mention 'nice, elegant UI'. Here is the original instruction: {instruction}\n\nRespond using the language: {original_prompt_language}"
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### The `TaskPlanner` has successfully generated the task plan")
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### The `TaskPlanner` has repaired and processed the JSON response")
            return plan_json
        except Exception as e:
            logger.error(f" #### The `TaskPlanner` encountered an error while generating the task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction, file_lists, original_prompt_language):
        """
        Get development plans based on the user's instruction.

        Args:
            instruction (str): The user's instruction for task planning.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### The `TaskPlanner` is generating task plans")
        plan = await self.get_task_plan(instruction, file_lists, original_prompt_language)
        logger.debug("\n #### The `TaskPlanner` has completed generating the task plans")
        return plan