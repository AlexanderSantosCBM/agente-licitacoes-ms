"""
============================================================
AGENTE DE LICITAÇÕES MS — Servidor Web (Flask)
============================================================
"""
import os, json, pathlib
from flask import Flask, request, jsonify, send_from_directory
import anthropic
import requests as req

app = Flask(__name__, static_folder="static")

# ── Configuração ─────────────────────────────────────────────
API_KEY     = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL       = "claude-sonnet-4-5"
MAX_TOKENS  = 1024
ORGAO_CNPJ  = os.environ.get("ORGAO_CNPJ", "03015475000140")
PCA_ANO     = int(os.environ.get("PCA_ANO", "2026"))
PCA_SEQ     = int(os.environ.get("PCA_SEQ", "3"))
PNCP_BASE   = "https://pncp.gov.br/api/consulta/v1"

# Carrega system prompt do arquivo
SP_PATH = pathlib.Path(__file__).parent / "system_prompt.txt"
SYSTEM_PROMPT = SP_PATH.read_text(encoding="utf-8") if SP_PATH.exists() else ""

# ── Definição das tools ───────────────────────────────────────
TOOLS = [
    {
        "name": "buscar_pca_pncp",
        "description": "Busca itens do PCA de um órgão na API pública do PNCP.",
        "input_schema": {
            "type": "object",
            "properties": {
                "cnpj":      {"type": "string",  "description": "CNPJ sem pontos/traços"},
                "ano":       {"type": "integer", "description": "Ano do PCA"},
                "sequencia": {"type": "integer", "description": "Sequência do PCA no PNCP"},
                "pagina":    {"type": "integer", "description": "Página (padrão 1)", "default": 1}
            },
            "required": ["cnpj", "ano", "sequencia"]
        }
    },
    {
        "name": "buscar_contratacoes_pncp",
        "description": "Busca contratações no PNCP por palavras-chave — útil para pesquisa de preços.",
        "input_schema": {
            "type": "object",
            "properties": {
                "termo":         {"type": "string",  "description": "Termo de busca"},
                "data_inicial":  {"type": "string",  "description": "Data inicial YYYYMMDD"},
                "data_final":    {"type": "string",  "description": "Data final YYYYMMDD"},
                "modalidade":    {"type": "integer", "description": "6=Pregão 8=Inexig 9=Dispensa"},
                "pagina":        {"type": "integer", "description": "Página (padrão 1)", "default": 1}
            },
            "required": ["termo"]
        }
    }
]

# ── Implementação das tools ───────────────────────────────────
def buscar_pca_pncp(cnpj, ano, sequencia, pagina=1):
    url = f"{PNCP_BASE}/orgaos/{cnpj}/planos-contratacao/{ano}/{sequencia}/itens"
    try:
        r = req.get(url, params={"pagina": pagina, "tamanhoPagina": 50}, timeout=15)
        if r.status_code == 200:
            data = r.json()
            itens = data if isinstance(data, list) else data.get("data", [])
            return {"status": "ok", "total": len(itens), "itens": itens[:20]}
        return {"status": "erro", "codigo": r.status_code}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

def buscar_contratacoes_pncp(termo, data_inicial="20250101", data_final="20261231",
                              modalidade=None, pagina=1):
    params = {"dataInicial": data_inicial, "dataFinal": data_final,
              "pagina": pagina, "tamanhoPagina": 20, "q": termo}
    if modalidade:
        params["codigoModalidadeContratacao"] = modalidade
    try:
        r = req.get(f"{PNCP_BASE}/contratacoes/publicacao", params=params, timeout=15)
        if r.status_code == 200:
            data = r.json()
            itens = data if isinstance(data, list) else data.get("data", [])
            return {"status": "ok", "total": len(itens), "resultados": itens[:15]}
        return {"status": "erro", "codigo": r.status_code}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

TOOL_MAP = {
    "buscar_pca_pncp": buscar_pca_pncp,
    "buscar_contratacoes_pncp": buscar_contratacoes_pncp,
}

# ── Rotas ─────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/config")
def config():
    return jsonify({"cnpj": ORGAO_CNPJ, "ano": PCA_ANO, "seq": PCA_SEQ})

@app.route("/api/chat", methods=["POST"])
def chat():
    if not API_KEY:
        return jsonify({"error": "API Key não configurada. Defina ANTHROPIC_API_KEY no .env"}), 500

    data     = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "Nenhuma mensagem enviada"}), 400

    try:
        client = anthropic.Anthropic(api_key=API_KEY)
        msgs   = list(messages)

        # Agentic loop — continua enquanto houver tool_use
        while True:
            response = client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=msgs
            )

            tool_uses = [b for b in response.content if b.type == "tool_use"]

            if tool_uses:
                # Converte content para formato serializável
                content_serial = []
                for b in response.content:
                    if b.type == "text":
                        content_serial.append({"type": "text", "text": b.text})
                    elif b.type == "tool_use":
                        content_serial.append({
                            "type": "tool_use", "id": b.id,
                            "name": b.name, "input": b.input
                        })
                msgs.append({"role": "assistant", "content": content_serial})

                # Executar tools
                resultados = []
                for tu in tool_uses:
                    fn     = TOOL_MAP.get(tu.name)
                    result = fn(**tu.input) if fn else {"erro": f"Tool '{tu.name}' não encontrada"}
                    resultados.append({
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": json.dumps(result, ensure_ascii=False)
                    })
                msgs.append({"role": "user", "content": resultados})
                continue

            # Resposta final
            texto = " ".join(b.text for b in response.content if hasattr(b, "text"))
            return jsonify({"response": texto})

    except anthropic.AuthenticationError:
        return jsonify({"error": "API Key inválida"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/pca")
def pca():
    cnpj = request.args.get("cnpj", ORGAO_CNPJ)
    ano  = int(request.args.get("ano",  PCA_ANO))
    seq  = int(request.args.get("seq",  PCA_SEQ))
    pag  = int(request.args.get("pag",  1))
    return jsonify(buscar_pca_pncp(cnpj, ano, seq, pag))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
