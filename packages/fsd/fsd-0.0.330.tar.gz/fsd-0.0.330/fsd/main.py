import git
import json
import os
import asyncio
import re
import time
import shutil  # Import shutil for copying directories
import subprocess
from concurrent.futures import ProcessPoolExecutor
from fsd.explainer.ExplainerController import ExplainerController  # Ensure this module is correctly imported and available
from fsd.coding_agent.ControllerAgent import ControllerAgent  # Ensure this module is correctly imported and available
from fsd.FirstPromptAgent import FirstPromptAgent
from fsd.io import InputOutput
from fsd.repo import GitRepo
from fsd.util import utils
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
import traceback

logger = get_logger(__name__)
max_tokens = 4096
async def start(project_path):
    try:
        # check project_path exist
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"{project_path} does not exist.")

        repo = GitRepo(project_path)
        
        explainer_controller = ExplainerController(repo)
        coding_controller = ControllerAgent(repo)
        first_prompt_controller = FirstPromptAgent(repo)

        while True:
            user_prompt_json = input("Enter your prompt (type 'exit' to quit): ")
            if user_prompt_json.startswith('/rollback'):
                repo.reset_previous_commit()
                continue
            user_prompt, file_attachments, focused_files = parse_payload(user_prompt_json, project_path)
            result = await get_prePrompt(user_prompt, first_prompt_controller)
            pipeline = result['pipeline']
            if pipeline == "1" or pipeline == 1:
                await explainer_controller.get_started(user_prompt, file_attachments, focused_files)
                logger.info("#### `All done!` Keep chatting with us for more help. Thanks for using!")
            elif pipeline == "2" or pipeline == 2:
                repo.set_commit(user_prompt)
                await coding_controller.get_started(user_prompt)
                logger.info("#### `All done!` Keep chatting with us for more help. Thanks for using!")
            elif pipeline == "3":
                break
    except FileNotFoundError as e:
        logger.error(f"\n#### FileNotFoundError: {str(e)}")
        logger.info("#### Something went wrong, but we've reverted the changes. Please try again. Thank you for choosing us!")
        exit()
    except Exception as e:
        logger.error(f"\n#### Unexpected error: {str(e)}")
        logger.info(f"Full traceback: {traceback.format_exc()}")
        logger.info("#### Something went wrong, but we've reverted the changes. Please try again. Thank you for choosing us!")
        exit()
        
async def get_prePrompt(user_prompt, first_prompt_controller):
    """Generate idea plans based on user prompt and available files."""
    return await first_prompt_controller.get_prePrompt_plans(user_prompt)

def parse_payload(user_prompt_json, project_path):
    try:
        data = json.loads(user_prompt_json)
        user_prompt = data.get("prompt", "")
        file_path = data.get("file_path", [])
        tracked_file = data.get("tracked_file", [])

        if tracked_file:
            tracked_file = [os.path.join(project_path, file.lstrip('./')) for file in tracked_file]
    
        return user_prompt, file_path, tracked_file
    except:
        return user_prompt_json, [], []