"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_v2_prompt() -> dict:
    """Carrega o prompt v2 e retorna o bloco interno do template."""
    prompts = load_prompts(Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml")
    return prompts["bug_to_user_story_v2"]

class TestPrompts:

    def test_prompt_structure(self):
        """Valida a estrutura geral do prompt."""
        prompt = load_v2_prompt()
        assert validate_prompt_structure(prompt)[0] is True

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt = load_v2_prompt()
        assert "system_prompt" in prompt
        assert prompt["system_prompt"].strip() != ""

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = load_v2_prompt()["system_prompt"]

        assert "Você é" in system_prompt
        assert "analista de software" in system_prompt.lower()

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = load_v2_prompt()["system_prompt"]
        assert "User Story" in system_prompt
        assert "Critérios de Aceitação" in system_prompt
        assert "Dado/Quando/Então" in system_prompt or "Como... Eu quero... Para que..." in system_prompt

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = load_v2_prompt()["system_prompt"]
        assert system_prompt.count("### Exemplo") >= 3
        assert "Entrada:" in system_prompt
        assert "Saída" in system_prompt

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt = load_v2_prompt()
        full_text = prompt["system_prompt"] + "\n" + prompt.get("user_prompt", "")
        assert "[TODO]" not in full_text
        assert "TODO" not in full_text

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        system_prompt = load_v2_prompt()["system_prompt"].lower()

        detected_techniques = 0
        if "você é" in system_prompt:
            detected_techniques += 1
        if "raciocine passo a passo" in system_prompt or "processo de raciocínio" in system_prompt:
            detected_techniques += 1
        if "### exemplos" in system_prompt or "exemplo 1" in system_prompt:
            detected_techniques += 1
        if "dado/quando/então" in system_prompt:
            detected_techniques += 1
        if "critérios de prevenção" in system_prompt:
            detected_techniques += 1

        assert detected_techniques >= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])