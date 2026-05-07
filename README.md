# AGENTE DE LICITAÇÕES MS — Guia de Deploy no Claude Platform

## ARQUIVOS DESTE PACOTE

| Arquivo | O que é | Onde usar |
|---|---|---|
| 01_system_prompt.txt | System prompt completo | Claude Platform → Workbench |
| 02_agent_config.json | Configuração completa do agente | Referência / API direta |
| 03_deploy.py | Script Python para testar localmente | Terminal do seu computador |
| .env.exemplo | Variáveis de ambiente | Copiar para .env |

---

## PASSO 1 — CRIAR CONTA NO CLAUDE PLATFORM

1. Acesse: https://console.anthropic.com
2. Clique em "Sign Up" ou "Log In"
3. Crie sua conta com e-mail institucional
4. Confirme o e-mail

---

## PASSO 2 — OBTER SUA API KEY

1. No Console, clique em "API Keys" no menu lateral esquerdo
2. Clique em "+ Create Key"
3. Dê um nome: "Agente Licitacoes MS"
4. COPIE A CHAVE — ela só aparece uma vez!
5. Guarde em local seguro (nunca compartilhe publicamente)

---

## PASSO 3 — TESTAR NO WORKBENCH (sem código)

1. No Console, clique em "Workbench" no menu lateral
2. No campo "System Prompt", cole TODO o conteúdo do arquivo:
   → 01_system_prompt.txt
3. Selecione o modelo: claude-sonnet-4-20250514
4. No campo "User", digite uma pergunta de teste:
   → "Como fazer uma dispensa por valor em MS?"
5. Clique em "Run"
6. O agente deve responder citando o PR 005-2025 da PGE/MS

Se funcionou: o agente está configurado corretamente!

---

## PASSO 4 — SALVAR COMO PROMPT REUTILIZÁVEL

1. No Workbench, clique em "Save" (botão superior direito)
2. Dê um nome: "Agente Licitações MS"
3. O prompt fica salvo com um ID único
4. Você pode abrir e usar em qualquer sessão futura

---

## PASSO 5 — TESTAR LOCALMENTE VIA SCRIPT PYTHON

Pré-requisitos:
  pip install anthropic requests

1. Copie .env.exemplo para .env:
   cp .env.exemplo .env

2. Edite o .env e coloque sua API Key real:
   ANTHROPIC_API_KEY=sk-ant-SUA_CHAVE_AQUI

3. Execute o script:
   python3 03_deploy.py

4. O terminal abrirá um chat interativo com o agente

---

## PASSO 6 — INTEGRAR NO SEU SITE OU SISTEMA (avançado)

Para incorporar o agente em uma aplicação web, use a API:

```python
import anthropic, os

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

with open("01_system_prompt.txt") as f:
    system = f.read()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=system,
    messages=[
        {"role": "user", "content": "Como fazer dispensa por valor em MS?"}
    ]
)
print(response.content[0].text)
```

---

## CUSTOS ESTIMADOS (Referência — mai/2026)

| Modelo | Input (por 1M tokens) | Output (por 1M tokens) |
|---|---|---|
| claude-sonnet-4-20250514 | ~$3,00 | ~$15,00 |

O system prompt tem ~18.000 tokens. Cada conversa consome:
- Input: ~18.000 (system) + mensagens do usuário
- Output: resposta do agente

Estimativa por pergunta: ~$0,05 a $0,15

---

## SUPORTE

- Documentação Anthropic: https://docs.anthropic.com
- Console: https://console.anthropic.com
- Fórum NELCA/GestGov: https://gestgov.discourse.group
