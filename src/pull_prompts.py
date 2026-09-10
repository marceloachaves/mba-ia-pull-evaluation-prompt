"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    #client = LangSmithClient()
    prompts = hub.pull("leonanluppi/bug_to_user_story_v1")
    promptToYaml = ""
    for message in prompts.messages:
        promptToYaml += message.prompt.template
    
    save_yaml(promptToYaml, Path("prompts/bug_to_user_story_v1.yml"))


def main():
    """Função principal"""
    print_section_header("Verificando variáveis de ambiente")
    check_env_vars(["LANGSMITH_API_KEY"])

    print_section_header("Fazendo pull dos prompts do LangSmith")
    pull_prompts_from_langsmith()


if __name__ == "__main__":
    sys.exit(main())
