"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    # print("Mensagem do template:", prompt_data["template"])
    try:
        # Criar ChatPromptTemplate a partir da string do template
        # template = ChatPromptTemplate.from_template(prompt_data["template"])
        prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_data[prompt_name]["system_prompt"]),
            ("human", prompt_data[prompt_name]["user_prompt"])
        ])

        hub.push(
            "marceloac/" + prompt_name,
            object=prompt,
            new_repo_is_public=True,
            tags=prompt_data.get(prompt_name, {}).get('tags'),
            new_repo_description=prompt_data.get(prompt_name, {}).get('description')
        )
        return True
    except Exception as e:
        print(f"Erro ao enviar prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    if not isinstance(prompt_data, dict) or not prompt_data:
        return False, ["Arquivo de prompt vazio ou em formato inválido"]

    for prompt_name, prompt_config in prompt_data.items():
        if not isinstance(prompt_config, dict):
            errors.append(f"Prompt '{prompt_name}' deve ser um dicionário")
            continue

        system_prompt = str(prompt_config.get("system_prompt", "")).strip()
        user_prompt = str(prompt_config.get("user_prompt", "")).strip()

        if not system_prompt:
            errors.append(f"Prompt '{prompt_name}' está sem system_prompt")

        if not user_prompt:
            errors.append(f"Prompt '{prompt_name}' está sem user_prompt")

    return len(errors) == 0, errors


def main():
    """Função principal"""
    print_section_header("Verificando variáveis de ambiente")
    check_env_vars(["LANGSMITH_API_KEY"])

    print_section_header("Carregando prompt otimizado")
    prompt_data = load_yaml("prompts/bug_to_user_story_v2.yml")
    prompt_name = "bug_to_user_story_v2"

    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("Falha na validação do prompt:")
        for error in errors:
            print(f"- {error}")
        return 1

    print_section_header("Enviando prompt para o LangSmith Hub")
    success = push_prompt_to_langsmith(prompt_name, prompt_data)
    if success:
        print(f"Prompt '{prompt_name}' enviado com sucesso!")
        return 0
    else:
        print("Falha ao enviar prompt.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
