import os
import aiohttp
import asyncio
import json
import sys
from json_repair import repair_json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)
class ExplainableFileFinderAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file or empty string if file doesn't exist.
        """
        if not os.path.exists(file_path):
            logger.debug(f"\n #### `File Manager Agent`: File does not exist - `{file_path}`")
            return ""

        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.debug(f"\n #### `File Manager Agent`: Encountered an error while reading `{file_path}` with `{encoding}` encoding\n Error: `{e}`")

        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.debug(f"\n #### `File Manager Agent`: Failed to read `{file_path}` in binary mode\n Error: `{e}`")

        return ""

    async def get_file_planning(self, idea):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.

        Returns:
            dict: JSON response with the plan or an empty array if no files are found.
        """
        all_file_contents = self.repo.print_tree()
        directory_path = self.repo.get_repo_path()
        prompt = (
            f"Analyze the user prompt and project structure to identify the most relevant files for providing context to answer the user's request. "
            f"Build a JSON response listing these files. Include only files that are directly related to the user's query or essential for understanding the context. "
            f"Provide only a JSON response without any additional text or Markdown formatting. "
            f"Current working project is {directory_path}. "
            f"Use this JSON format:"
            "{\n"
            f"    \"working_files\": [\"{directory_path}/path/to/most_relevant_file1.ext\", \"{directory_path}/path/to/most_relevant_file2.ext\"]\n"
            "}\n\n"
            "Ensure the 'working_files' list contains only the most pertinent files, prioritizing those that directly address the user's request. "
            "It is crucial that each file path in the 'working_files' list is an absolute path, starting from the root directory. "
            f"Always prepend '{directory_path}' to each file path to ensure it's a full, absolute path. "
            "If no relevant files are found, return an empty array for 'working_files' like this: "
            "{\n"
            f"    \"working_files\": []\n"
            "}\n"
            "Return only valid JSON without Markdown symbols or invalid escapes."
        )

        messages = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": f"This is user request to do:\n{idea}\nThis is the current project context:\n{all_file_contents}\n"
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            return {
                "reason": str(e)
            }

    async def get_file_plannings(self, idea):
        """
        Request file planning from Azure OpenAI API for a given idea and project structure.

        Args:
            idea (str): The general plan idea.
            files (list): List of file paths representing the project structure.

        Returns:
            dict: JSON response with the plan.
        """
        logger.info(f"\n #### The `File Manager Agent` is looking for any relevant context.")
        logger.info("\n-------------------------------------------------")
        plan = await self.get_file_planning(idea)
        logger.debug(f"\n #### `File Manager Agent`: Successfully completed the search for relevant files")
        return plan
