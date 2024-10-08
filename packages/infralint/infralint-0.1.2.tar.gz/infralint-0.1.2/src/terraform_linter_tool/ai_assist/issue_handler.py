import logging
import os
from typing import Dict, Optional

import openai
from openai.error import (APIConnectionError, AuthenticationError,
                          InvalidRequestError, OpenAIError)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AIHandlerFactory:
    """
    A Factory class to handle the creation and reuse of IssueHandler instances.
    Ensures that the handler is only created once, reusing it for subsequent calls.
    """
    _instance = None

    @staticmethod
    def get_handler():
        """Retrieve or create the IssueHandler instance."""
        if AIHandlerFactory._instance is None:
            AIHandlerFactory._instance = IssueHandler()  # Create IssueHandler via the factory
        return AIHandlerFactory._instance


class IssueHandler:
    """Handler for determining severity and resolution using OpenAI."""

    def __init__(self, model="gpt-4", timeout=30):
        self.model = model
        self.timeout = timeout
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
        else:
            raise RuntimeError("OpenAI API key not set. Please set the API key to use this feature.")

    def get_openai_response(self, prompt: str) -> Optional[str]:
        """Fetch a response from OpenAI."""
        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in security and best practices for infrastructure."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    },
                ],
                timeout=self.timeout  # Optional timeout
            )
            response = completion.choices[0].message["content"].strip()
            if not isinstance(response, str) or not response:  # Ensure it's a valid string
                logger.error("Received an invalid or empty response from OpenAI.")
                return None
            return response
        except (AuthenticationError, APIConnectionError, InvalidRequestError, OpenAIError) as e:
            logger.error(f"OpenAI error: {e}")
            raise RuntimeError(f"OpenAI error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise RuntimeError(f"Unexpected error: {e}")

    def infer_severity(self, description: str, framework: str) -> str:
        """
        Determine the severity based on the issue description.
        """
        prompt = (
            "Based on the following issue in the {framework} framework: '{description}', "
            "please determine the severity of the issue. Respond ONLY with one of the following: "
            "CRITICAL, HIGH, MEDIUM, LOW. Do not provide any other text."
        ).format(framework=framework, description=description)

        response = self.get_openai_response(prompt)
        valid_severities = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]

        if response and response.upper().strip() in valid_severities:
            return response.upper().strip()
        logger.error(f"Unable to determine severity for the issue: {description}")
        return "UNKNOWN"

    def generate_resolution_context(self, description: str, framework: str) -> str:
        """
        Generate additional context for CRITICAL or HIGH severity issues.
        """
        prompt = (
            "Given the following high-severity issue in the {framework} framework: '{description}', "
            "provide a short summary and resolution. Keep it brief."
        ).format(framework=framework, description=description)

        response = self.get_openai_response(prompt)
        return response or "No additional context available."

    def process_issue(self, description: str, framework: str) -> Dict[str, Optional[str]]:
        """
        Process the issue description, return severity, and optionally provide resolution context.
        """
        result: Dict[str, Optional[str]] = {"severity": None, "context": None}

        try:
            severity = self.infer_severity(description, framework)
            result["severity"] = severity

            if severity in ["CRITICAL", "HIGH"]:
                context = self.generate_resolution_context(description, framework)
                result["context"] = context

            return result
        except RuntimeError as e:
            logger.error(f"Error processing issue: {e}")
            return result