import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from fsd.util.utils import read_file_content
logger = get_logger(__name__)

class IdeaDevelopment:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway()

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, role, crawl_logs):
        """
        Initialize the conversation with a system prompt and user context.
        """
        logger.debug("Initializing conversation with system prompt and user context")

        all_file_contents = self.repo.print_summarize_with_tree()

            # Start of Selection
        system_prompt = (
            f"You are a senior {role}. Analyze the project files and create a detailed plan. Follow these guidelines:\n\n"
            "**Guidelines:**\n"
            "- **Enterprise Standards:** Ensure scalability, performance, and security.\n"
            "- **External Resources:** Assume external data from Zinley crawler agent will be provided later. Guide coders to integrate it properly without including data directly.\n"
            "- **No Source Code:** Focus on technical and architectural planning; exclude source code.\n"
            "- **File Integrity:** Modify existing files without renaming. Create new files if necessary, detailing updates and integrations.\n"
            "- **Image Assets:** Follow strict specifications for file sizes and include detailed plans for new files and images.\n"
            "- **README:** Mention inclusion or update of README without detailing it.\n"
            "- **Structure & Naming:** Propose clear, logical file and folder structures for scalability and expansion.\n"
            "- **UI Design:** Ensure a well-designed UI for everything, tailored for each platform.\n\n"

            "**2. Strict Guidelines:**\n\n"

            "**2.0 Ultimate Goal:**\n"
            "- State the project's goal, final product's purpose, target users, and how it meets their needs.\n\n"

            "**2.1 Existing Files:**\n"
            "- Provide thorough descriptions of implementations in existing files, specifying the purpose and functionality of each.\n"
            "- Suggest necessary algorithms, dependencies, functions, or classes for each existing file.\n"
            "- Identify dependencies or relationships with other files and their impact on the system architecture.\n"
            "- Describe the use of image, video, or audio assets in each existing file, specifying filenames and their placement.\n"
            "- Specify what modifications are needed in each existing file to align with the new development plan.\n\n"

            "**2.2 New Files:**\n\n"

            "- Organize all files deeply following enterprise setup standards.\n"
            "- Provide a detailed description of the file and folder structure.\n"
            "- Ensure that new files are structured according to enterprise-level standards.\n"
            "- Provide comprehensive details for implementations in each new file.\n"
            "- Suggest required algorithms, dependencies, functions, or classes for each new file.\n"
            "- Explain how each new file will integrate with existing systems.\n"
            "- Describe the usage of image, video, or audio assets in new files, specifying filenames and their placement.\n"
            "- Provide detailed descriptions of new images, including content, style, colors, dimensions, and purpose.\n"
            "- For new social media icons, specify the exact platform and provide clear details for each icon.\n"
            "- For all new generated images, include the full path for each image.\n"
            "- Define the expected new tree structure after implementation.\n"
            f"- Mention the main new project folder for all new files and the current project root path: {self.repo.get_repo_path()}.\n"
            "- Ensure all critical files are included in the plan.\n"
            "- Never propose creation of files that cannot be generated through coding.\n\n"

            "**2.3 Existing Context Files:**\n"
            "- Provide a list of relevant existing context files necessary for understanding and completing the task.\n"
            "- Exclude non-essential files like assets, development environment configurations, and IDE-specific files.\n"
            "- Ensure there is no overlap with Existing Files (2.1) and New Files (2.2).\n"
            "- Existing Context Files will be used for RAG purposes.\n"
            "- If no relevant context files are found, mention this briefly.\n\n"

            "**2.4 Dependencies:**\n"
            "- Enumerate all dependencies needed for the task.\n"
            "- Use the latest versions of dependencies.\n"
            "- Include only dependencies that can be installed via the command line interface (CLI).\n"
            "- Provide exact CLI commands for installing dependencies.\n"
            "- Exclude dependencies that require IDE manipulation.\n"
            "- Ensure compatibility among all dependencies and with the existing system architecture.\n\n"

            "**2.5 APIs:**\n"
            "- Clearly mention any APIs that need to be used in the project.\n"
            "- If applicable, specify the authentication methods required for each API.\n"
            "- Describe how data will flow between the application and the APIs.\n"
            "- Outline strategies for handling API errors and rate limiting.\n"
            "- Provide full links to the API documentation.\n\n"

            "**2.6 Crawl Data Integration:**\n"
            "- If crawl data is provided, specify which file(s) should access this data.\n"
            "- Explain how the crawl data should be integrated into the project structure.\n"
            "- Provide clear instructions on how to use the crawl data within the specified files.\n"
            "- If no crawl data is provided, state that no integration is needed at this time.\n"

            "**(Do not ADD anything more thing, Stop here!):**\n\n"

            "**No Yapping:** Provide concise, focused responses without unnecessary elaboration or repetition.\n\n"
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current project structure and files summary:\n{all_file_contents}\n"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

        if crawl_logs:
            crawl_logs_prompt = f"Use this existing crawl data for planning: {crawl_logs}"
            self.conversation_history.append({"role": "user", "content": crawl_logs_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Understood. Using provided data only."})

            utilization_prompt = (
                "Specify which file(s) should access this crawl data. "
                "Do not provide steps for crawling or API calls. "
                "The data is already available. "
                "Follow the original development plan guidelines strictly, "
                "ensuring adherence to all specified requirements and best practices."
            )
            self.conversation_history.append({"role": "user", "content": utilization_prompt})
            self.conversation_history.append({"role": "assistant", "content": "Will specify files for data access, following original development plan guidelines strictly. No additional crawling or API calls needed."})

    async def get_idea_plan(self, user_prompt, original_prompt_language):
        logger.debug("Generating idea plan based on user prompt")

        lazy_prompt = """You are diligent and tireless!
            You ALWAYS provide a complete and detailed plan without leaving any part unimplemented.
            You NEVER include placeholder comments or TODOs in your plan.
            Your tree structure MUST clearly show how you would implement each component with specific files.
            You ALWAYS FULLY DESCRIBE every aspect of the needed plan, ensuring no steps are left vague or incomplete.
            """
        
        prompt = (
            f"Follow the user prompt and provide a detailed, step-by-step no-code plan. "
            f"Do not include code snippets or technical details. "
            f"Focus on high-level concepts, strategies, and approaches. "
            f"Here's the user prompt:\n\n{user_prompt}\n\n"
            f"Return a well-formatted response with clear headings (use h4 ####) and appropriate spacing. "
            f"Use markdown tables for lists. "
            f"Include tree structures in plaintext markdown within code blocks:\n"
            f"```plaintext\n"
            f"project/\n"
            f"├── src/\n"
            f"│   ├── main.py\n"
            f"│   └── utils.py\n"
            f"├── tests/\n"
            f"│   └── test_main.py\n"
            f"└── README.md\n"
            f"```\n"
            f"Include bash commands in code blocks:\n"
            f"```bash\n"
            f"command here\n"
            f"```\n"
            f"{lazy_prompt}"
            f"Include essential icons or images in the plan. "
            f"Follow instructions clearly. "
            f"Respond in: {original_prompt_language}. "
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.stream_prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            return response
        except Exception as e:
            logger.error(f"`IdeaDevelopment` agent encountered an error: {e}")
            return {
                "reason": str(e)
            }

    async def get_idea_plans(self, user_prompt, original_prompt_language):
        logger.debug("Initiating idea plan generation process")
        return await self.get_idea_plan(user_prompt, original_prompt_language)
