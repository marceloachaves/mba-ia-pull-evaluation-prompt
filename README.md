# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

- Fazer pull de prompts do LangSmith Prompt Hub contendo prompts de baixa qualidade
- Refatorar e otimizar esses prompts usando técnicas avançadas de Prompt Engineering
- Fazer push dos prompts otimizados de volta ao LangSmith
- Avaliar a qualidade através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- Atingir pontuação mínima de 0.8 (80%) em todas as métricas de avaliação

## Exemplo no CLI

Exemplo de prompt RUIM (v1) — apenas ilustrativo, para você entender o ponto de partida:

```
==================================================
Prompt: {seu_username}/bug_to_user_story_v1
==================================================

Métricas Derivadas:
  - Helpfulness: 0.45 ✗
  - Correctness: 0.52 ✗

Métricas Base:
  - F1-Score: 0.48 ✗
  - Clarity: 0.50 ✗
  - Precision: 0.46 ✗

❌ STATUS: REPROVADO
⚠️  Métricas abaixo de 0.8: helpfulness, correctness, f1_score, clarity, precision
```

Exemplo de prompt OTIMIZADO (v2) — seu objetivo é chegar aqui:

```
# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação
python src/evaluate.py

Executando avaliação dos prompts...
==================================================
Prompt: {seu_username}/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.96 ✓

Métricas Base:
  - F1-Score: 0.93 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

✅ STATUS: APROVADO - Todas as métricas >= 0.8
```

## Tecnologias obrigatórias

- Linguagem: Python 3.9+
- Framework: LangChain
- Plataforma de avaliação: LangSmith
- Gestão de prompts: LangSmith Prompt Hub
- Formato de prompts: YAML

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

## OpenAI

- Crie uma API Key da OpenAI: https://platform.openai.com/api-keys
- Você vai precisar de um modelo de LLM para responder e de um modelo de LLM para avaliação. Consulte a documentação oficial da OpenAI para ver os modelos disponíveis.
- Custo estimado: ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma API Key da Google: https://aistudio.google.com/app/apikey
- Você vai precisar de um modelo de LLM para responder e de um modelo de LLM para avaliação. Consulte a documentação oficial do Google para ver os modelos disponíveis.
- Os limites de requisições gratuitas mudam com frequência. Consulte os limites atuais na documentação oficial do Google.

## Escolha dos modelos

Este desafio não fixa modelos. Nomes e versões mudam com frequência e alguns são descontinuados, então faz parte do desafio consultar a documentação oficial do provedor que você escolher, ver quais modelos estão disponíveis no momento e selecionar os que atendem ao objetivo. Você pode usar o mesmo modelo para responder e para avaliar, ou um modelo mais capaz na avaliação.

## Requisitos

### 1. Pull do Prompt inicial do LangSmith

O repositório base já contém prompts de baixa qualidade publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

Tarefas:

- Configurar suas credenciais do LangSmith no arquivo .env (conforme o arquivo .env.example)
- Implementar o script src/pull_prompts.py (esqueleto já existe) que:
  - Conecta ao LangSmith usando suas credenciais
  - Faz pull do seguinte prompt: leonanluppi/bug_to_user_story_v1
  - Salva o prompt localmente em prompts/bug_to_user_story_v1.yml

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

Tarefas:

- Analisar o prompt em prompts/bug_to_user_story_v1.yml
- Criar um novo arquivo prompts/bug_to_user_story_v2.yml com suas versões otimizadas
- Aplicar obrigatoriamente Few-shot Learning (exemplos claros de entrada/saída) e pelo menos uma das seguintes técnicas adicionais:
  - Chain of Thought (CoT): Instruir o modelo a "pensar passo a passo"
  - Tree of Thought: Explorar múltiplos caminhos de raciocínio
  - Skeleton of Thought: Estruturar a resposta em etapas claras
  - ReAct: Raciocínio + Ação para tarefas complexas
  - Role Prompting: Definir persona e contexto detalhado
- Documentar no README.md quais técnicas você escolheu e por quê

Requisitos do prompt otimizado:

- Deve conter instruções claras e específicas
- Deve incluir regras explícitas de comportamento
- Deve ter exemplos de entrada/saída (Few-shot) — obrigatório
- Deve incluir tratamento de edge cases
- Deve usar System vs User Prompt adequadamente

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

Tarefas:

- Implementar o script src/push_prompts.py (esqueleto já existe) que:
  - Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
  - Faz push para o LangSmith com nomes versionados: {seu_username}/bug_to_user_story_v2
  - Adiciona metadados (tags, descrição, técnicas utilizadas)
- Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
- Deixá-lo público

### 4. Iteração

Espera-se 3-5 iterações.

- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até TODAS as métricas >= 0.8

```
Critério de Aprovação:
- Helpfulness >= 0.8
- Correctness >= 0.8
- F1-Score >= 0.8
- Clarity >= 0.8
- Precision >= 0.8

MÉDIA das 5 métricas >= 0.8
```

IMPORTANTE: TODAS as 5 métricas devem estar >= 0.8, não apenas a média!

### 5. Testes de Validação

O que você deve fazer: Edite o arquivo tests/test_prompts.py e implemente, no mínimo, os 6 testes abaixo usando pytest:

- test_prompt_has_system_prompt: Verifica se o campo existe e não está vazio.
- test_prompt_has_role_definition: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- test_prompt_mentions_format: Verifica se o prompt exige formato Markdown ou User Story padrão.
- test_prompt_has_few_shot_examples: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- test_prompt_no_todos: Garante que você não esqueceu nenhum [TODO] no texto.
- test_minimum_techniques: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

Como validar:

```
pytest tests/test_prompts.py
```

## Estrutura obrigatória do projeto

Faça um fork do repositório base: https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt

```
mba-ia-pull-evaluation-prompt/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (já incluso)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado (criar)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (já incluso)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith (implementar)
│   ├── push_prompts.py       # Push ao LangSmith (implementar)
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares (pronto)
│
├── tests/
│   └── test_prompts.py       # Testes de validação (implementar)
```

O que você deve implementar:

- prompts/bug_to_user_story_v2.yml — Criar do zero com seu prompt otimizado
- src/pull_prompts.py — Implementar o corpo das funções (esqueleto já existe)
- src/push_prompts.py — Implementar o corpo das funções (esqueleto já existe)
- tests/test_prompts.py — Implementar os 6 testes de validação (esqueleto já existe)
- README.md — Documentar seu processo de otimização

O que já vem pronto (não alterar):

- src/evaluate.py — Script de avaliação completo
- src/metrics.py — 5 métricas implementadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- src/utils.py — Funções auxiliares
- datasets/bug_to_user_story.jsonl — Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- Suporte multi-provider (OpenAI e Gemini)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ordem de execução

1. Executar pull dos prompts ruins

```
python src/pull_prompts.py
```

2. Refatorar prompts

Edite manualmente o arquivo prompts/bug_to_user_story_v2.yml aplicando as técnicas aprendidas no curso.

3. Fazer push dos prompts otimizados

```
python src/push_prompts.py
```

4. Executar avaliação

```
python src/evaluate.py
```

## Entregável

1. Repositório público no GitHub (fork do repositório base) contendo:

- Todo o código-fonte implementado
- Arquivo prompts/bug_to_user_story_v2.yml 100% preenchido e funcional
- Arquivo README.md atualizado

2. README.md deve conter:

A) Seção "Técnicas Aplicadas (Fase 2)":

- Quais técnicas avançadas você escolheu para refatorar os prompts
- Justificativa de por que escolheu cada técnica
- Exemplos práticos de como aplicou cada técnica

B) Seção "Resultados Finais":

- Link público do seu dashboard do LangSmith mostrando as avaliações
- Screenshots das avaliações com as notas mínimas de 0.8 atingidas
- Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

C) Seção "Como Executar":

- Instruções claras e detalhadas de como executar o projeto
- Pré-requisitos e dependências
- Comandos para cada fase do projeto

3. Evidências no LangSmith:

- Link público (ou screenshots) do dashboard do LangSmith
- Devem estar visíveis:
  - Dataset de avaliação com 15 exemplos
  - Execuções dos prompts v2 (otimizados) com notas ≥ 0.8
  - Tracing detalhado de pelo menos 3 exemplos

## Dicas Finais

- Lembre-se da importância da especificidade, contexto e persona ao refatorar prompts
- Use Few-shot Learning com 2-3 exemplos claros para melhorar drasticamente a performance
- Chain of Thought (CoT) é excelente para tarefas que exigem raciocínio complexo (como análise de bugs)
- Use o Tracing do LangSmith como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- Não altere os datasets de avaliação - apenas os prompts em prompts/bug_to_user_story_v2.yml
- Itere, itere, itere - é normal precisar de 3-5 iterações para atingir 0.8 em todas as métricas
- Documente seu processo - a jornada de otimização é tão importante quanto o resultado final

---  

## A) Seção "Técnicas Aplicadas (Fase 2)":

A própria exigência do desafio está documentada em README.md: era obrigatório usar Few-shot Learning e pelo menos uma técnica adicional. O prompt final em bug_to_user_story_v2.yml implementa isso de forma explícita.

### 1) Few-shot Learning
- O arquivo final contém vários exemplos de entrada/saída, como:
  - “Exemplo 1”
  - “Exemplo 2”
  - “Exemplo 3”
  - “Exemplo 7”
  - “Exemplo 9”
- Isso ensina o modelo a seguir o formato esperado e a transformar bugs em User Stories com qualidade.

Por que foi usado:
- Para reduzir ambiguidades.
- Para fixar estrutura, nível de detalhe e linguagem esperada.
- Para melhorar consistência em casos repetitivos.

### 2) Role Prompting
- O prompt define a persona:
  - “Você é um analista de software especializado em análise de incidentes...”
- Também define responsabilidade e domínio.

Por que foi usado:
- A persona orienta a resposta para um contexto técnico e de desenvolvimento.
- Reduz respostas genéricas e melhora o nível de precisão.

### 3) Chain of Thought / Skeleton of Thought
- O prompt usa uma estrutura interna em etapas:
  - Passo 1: Extração de evidências
  - Passo 2: Identificação do problema
  - Passo 3: Fato vs hipótese
  - Passo 4: Ator e valor
  - Passo 5: Matriz de cobertura
  - Passo 6: Critérios de aceitação
  - Passo 7: Revisão de recall
  - Passo 8: Revisão de precisão e formato
- Isso é um típico “skeleton of thought” + raciocínio em etapas.

Por que foi usado:
- Para fazer o modelo separar observações, inferências e hipóteses.
- Para evitar que ele “copie o log” sem transformar em tarefa útil.

### 4) Output schema / structured prompting
- O prompt obriga a resposta em:
  - User Story
  - Critérios de Aceitação
  - Contexto Técnico
  - (quando aplicável) Critérios de Prevenção, Técnicos, Acessibilidade

Por que foi usado:
- Facilita avaliação automática.
- Garante que a resposta seja útil para desenvolvedores.
- Reduz respostas livres demais.

### 5) Guardrails e regras de inferência controlada
- Há regras explícitas sobre:
  - preservar fatos;
  - não transformar hipótese em fato;
  - não inventar valores/fluxos;
  - separar evidência direta de inferência;
  - manter somente o que está sustentado no relato.

Por que foi usado:
- Esse foi um ajuste crítico para qualidade e correção.
- O prompt anterior era simples demais e tendia a inferir sem base.

--- 
### Ajustes pontuais feitos e por que foram ajustados

### Ajuste 1: introdução de persona e contexto
No prompt final, a primeira seção já inicia com:
- “Você é um analista de software especializado...”
- “Sua tarefa é analisar evidências de um bug...”

Por que:
- Sem isso, o modelo tende a responder como um assistente genérico e não como um analista de incidentes.
- A persona reduz derivações sem foco.

### Ajuste 2: exigência de passos de raciocínio interno
O arquivo introduz “Processo de Raciocínio” com oito passos.

Por que:
- A revisão do problema mostrou que o modelo precisava de estrutura para:
  - extrair fatos;
  - diferenciar evidência e hipótese;
  - mapear impacto;
  - converter o bug em tarefa técnica útil.
- Esse ajuste foi essencial para melhorar “correctness” e “precision”.

### Ajuste 3: divisão entre fato e hipótese
A seção “Regras de análise” e “Separação fato vs hipótese” entra em detalhes.

Por que:
- Era um problema recorrente: o modelo “explicava como se soubesse” a causa do bug sem confirmação.
- Isso gerava respostas plausíveis, mas não confiáveis.
- A correção foi impor “evidência direta” vs “hipótese não confirmada”.

### Ajuste 4: padronização da saída
A seção “Formato da resposta” define a estrutura obrigatória.

Por que:
- Sem isso, o modelo poderia responder em texto livre, pouco comparável.
- A saída padronizada facilita:
  - testes,
  - avaliação,
  - uso em pipelines,
  - revisão humana.

### Ajuste 5: exemplos de entrada/saída detalhados
O final do prompt contém vários exemplos, mais do que o necessário.

Por que:
- Foi necessário ensinar o padrão de resposta por demonstração.
- Exemplos resolvem ambiguidades de:
  - linguagem,
  - estrutura,
  - tipo de informação relevante,
  - estilo de critério DADO/QUANDO/ENTÃO.

### Ajuste 6: foco em recall e cobertura
A seção “Revisão de recall” exige que cada fato do relato apareça em algum critério, contexto ou cálculo.

Por que:
- O problema identificado na avaliação do prompt que estava com baixo recall, mostra que o modelo estava omitindo dados importantes.
- Com isso, a resposta ficou mais completa.

### Ajuste 7: revisão de precisão e remoção de hipóteses
A seção “Revisão de precisão e formato” exige remover inferências sem suporte.

Por que:
- Isso corrige um erro clássico de LLM:
  - responder “bem” mas com afirmações inventadas.
- A ideia é preservar a fidelidade ao incidente.

### Ajuste 8: contexto técnico opcional e detalhado
A seção “Contexto Técnico” foi adicionada para manter dados relevantes sem poluir a User Story principal.

Por que:
- O prompt precisa preservar logs, endpoints, status, mensagens e impacto sem repetir tudo no corpo principal.
- Isso melhora o valor para a equipe técnica.



## B) Seção "Resultados Finais":

- Screenshot do dashboard em `resultados/screenshot/dashboard`
- Screenshots das avaliações com as notas mínimas de 0.8 atingidas em `resultados/screenshot/avaliacao_v2`
- Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)


# Resultados Finais

## Tabela Comparativa: Prompt v1 vs Prompt v2

| Métrica | Prompt v1 | Prompt v2 | Melhoria | Status v1 | Status v2 |
|---------|-----------|-----------|----------|-----------|-----------|
| **Helpfulness** | 0.89 | 0.91 | +0.02 | ✓ | ✓ |
| **Correctness** | 0.84 | 0.86 | +0.02 | ✓ | ✓ |
| **F1-Score** | 0.79 | 0.83 | +0.04 | ✗ | ✓ |
| **Clarity** | 0.89 | 0.92 | +0.03 | ✓ | ✓ |
| **Precision** | 0.89 | 0.90 | +0.01 | ✓ | ✓ |
| **MÉDIA GERAL** | 0.8566 | 0.8845 | +0.0279 | ✗ Reprovado | ✓ Aprovado |

---

## Análise dos Resultados

### Prompt v1 (Inicial)

- **Status**: ❌ **REPROVADO**
- **Problema Principal**: F1-Score em 0.79 (abaixo de 0.8)
- **Pontos Fortes**: 
  - Clarity: 0.89
  - Precision: 0.89
- **Pontos Fracos**: 
  - F1-Score baixo indicava falta de cobertura e recall

### Prompt v2 (Otimizado)

- **Status**: ✅ **APROVADO**
- **Todas as Métricas >= 0.8**: Sim
- **Maior Melhoria**: F1-Score (+0.04 pontos) — resultado direto das técnicas aplicadas
- **Melhoria Secundária**: Clarity (+0.03) — benefício da estrutura mais clara

### Impacto das Técnicas Aplicadas

A melhoria em **F1-Score** (+0.04) reflete o sucesso das técnicas implementadas:

1. **Chain of Thought (8 passos)** → Melhorou cobertura de fatos (recall)
2. **Guardrails e regras de fidelidade** → Melhorou precisão das respostas
3. **Few-shot Learning (10 exemplos)** → Fixou padrão esperado
4. **Estrutura obrigatória (User Story + Critérios)** → Garantiu completude

## C) Seção "Como Executar":

### VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Como executar

1. Fazer push dos prompts otimizados

```
python src/push_prompts.py
```

2. Executar avaliação

```
python src/evaluate.py
```  
3. Executar testes

```
pytest tests/test_prompts.py
```

## 3. Evidências no LangSmith:

- Screenshots do dashboard do LangSmith em `resultados/screenshot/dashboard`
- Tracing em `resultados/screenshot/tracing`