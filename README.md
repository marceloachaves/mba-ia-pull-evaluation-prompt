# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

- Fazer pull de prompts do LangSmith Prompt Hub contendo prompts de baixa qualidade
- Refatorar e otimizar esses prompts usando técnicas avançadas de Prompt Engineering
- Fazer push dos prompts otimizados de volta ao LangSmith
- Avaliar a qualidade através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- Atingir pontuação mínima de 0.8 (80%) em todas as métricas de avaliação


## A) Seção "Técnicas Aplicadas (Fase 2)":

O prompt final em bug_to_user_story_v2.yml utiliza as seguintes técnicas:

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
- Url dataset: https://smith.langchain.com/public/9929330a-ecc2-4f3b-95c3-0292a87ba71c/d