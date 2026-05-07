#!/usr/bin/env python3
"""
=============================================================
AGENTE DE LICITAÇÕES MS — Script de Deploy e Teste
=============================================================
Pré-requisitos:
  pip install anthropic requests

Como usar:
  1. Defina sua API key no .env ou diretamente na variável abaixo
  2. Execute: python3 03_deploy.py
  3. O chat abrirá no terminal — digite sua pergunta

Documentação da API Anthropic:
  https://docs.anthropic.com
=============================================================
"""

import os, json, requests
import anthropic

# ── Configuração ─────────────────────────────────────────────
# Coloque sua chave aqui OU defina a variável de ambiente ANTHROPIC_API_KEY
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "sk-ant-COLOQUE_SUA_CHAVE_AQUI")

MODEL   = "claude-sonnet-4-20250514"
MAX_TOK = 1024

# Carregar system prompt do arquivo
with open("01_system_prompt.txt", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Carregar definição de tools
with open("02_agent_config.json", encoding="utf-8") as f:
    cfg = json.load(f)
    TOOLS = cfg["tools"]

# ── Implementação das tools ───────────────────────────────────
PNCP_BASE = "https://pncp.gov.br/api/consulta/v1"

def buscar_pca_pncp(cnpj: str, ano: int, sequencia: int, pagina: int = 1) -> dict:
    """Busca itens do PCA na API pública do PNCP."""
    url = f"{PNCP_BASE}/orgaos/{cnpj}/planos-contratacao/{ano}/{sequencia}/itens"
    params = {"pagina": pagina, "tamanhoPagina": 50}
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            data = r.json()
            itens = data if isinstance(data, list) else data.get("data", [])
            return {
                "status": "ok",
                "total_pagina": len(itens),
                "pagina": pagina,
                "itens": itens[:20]  # limita para não explodir o contexto
            }
        return {"status": "erro", "codigo": r.status_code, "mensagem": r.text[:200]}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

def buscar_contratacoes_pncp(termo: str, data_inicial: str = "20250101",
                              data_final: str = "20261231",
                              modalidade: int = None, pagina: int = 1) -> dict:
    """Busca contratações no PNCP por palavra-chave."""
    url = f"{PNCP_BASE}/contratacoes/publicacao"
    params = {
        "dataInicial": data_inicial,
        "dataFinal": data_final,
        "pagina": pagina,
        "tamanhoPagina": 20,
        "q": termo,
    }
    if modalidade:
        params["codigoModalidadeContratacao"] = modalidade
    try:
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            data = r.json()
            itens = data if isinstance(data, list) else data.get("data", [])
            return {"status": "ok", "total": len(itens), "resultados": itens[:15]}
        return {"status": "erro", "codigo": r.status_code, "mensagem": r.text[:200]}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

# Mapeamento tool_name → função
TOOL_MAP = {
    "buscar_pca_pncp": buscar_pca_pncp,
    "buscar_contratacoes_pncp": buscar_contratacoes_pncp,
}

# ── Loop de execução de tools ─────────────────────────────────
def executar_tools(tool_uses: list) -> list:
    resultados = []
    for tu in tool_uses:
        nome = tu.name
        params = tu.input
        print(f"  🔧 Executando tool: {nome}({params})")
        if nome in TOOL_MAP:
            resultado = TOOL_MAP[nome](**params)
        else:
            resultado = {"erro": f"Tool '{nome}' não implementada."}
        resultados.append({
            "type": "tool_result",
            "tool_use_id": tu.id,
            "content": json.dumps(resultado, ensure_ascii=False)
        })
    return resultados

# ── Chat com agentic loop ─────────────────────────────────────
def chat(historico: list, pergunta: str) -> str:
    client = anthropic.Anthropic(api_key=API_KEY)
    historico.append({"role": "user", "content": pergunta})
    messages = list(historico)

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOK,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )

        # Verificar se há tool_use
        tool_uses = [b for b in response.content if b.type == "tool_use"]

        if tool_uses:
            # Adicionar resposta do assistente (com tool_use)
            messages.append({"role": "assistant", "content": response.content})
            # Executar as tools e adicionar resultados
            resultados = executar_tools(tool_uses)
            messages.append({"role": "user", "content": resultados})
            # Continuar o loop
            continue

        # Resposta final (sem tool_use)
        texto = " ".join(b.text for b in response.content if hasattr(b, "text"))
        historico.append({"role": "assistant", "content": texto})
        return texto

# ── Interface de chat no terminal ─────────────────────────────
def main():
    print("=" * 60)
    print("  AGENTE DE LICITAÇÕES MS — Terminal")
    print("  Digite sua pergunta ou 'sair' para encerrar")
    print("=" * 60)
    historico = []
    while True:
        try:
            pergunta = input("\nVocê: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando...")
            break
        if pergunta.lower() in ("sair", "exit", "quit"):
            break
        if not pergunta:
            continue
        print("\nAgente: ", end="", flush=True)
        try:
            resposta = chat(historico, pergunta)
            print(resposta)
        except anthropic.AuthenticationError:
            print("❌ API Key inválida. Verifique a variável API_KEY no script.")
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
