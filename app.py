"""
============================================================
AGENTE DE LICITAÇÕES MS — Servidor Web com suporte a PDF
============================================================
"""
import os, json, pathlib, base64
from flask import Flask, request, jsonify, send_from_directory
import anthropic
import requests as req

app = Flask(__name__, static_folder="static")

API_KEY    = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL      = "claude-sonnet-4-5"
MAX_TOKENS = 2048
ORGAO_CNPJ = os.environ.get("ORGAO_CNPJ", "03015475000140")
PCA_ANO    = int(os.environ.get("PCA_ANO", "2026"))
PCA_SEQ    = int(os.environ.get("PCA_SEQ", "3"))
PNCP_BASE  = "https://pncp.gov.br/api/consulta/v1"
MAX_PDF_MB = 10
MAX_PDFS   = 5

SP_PATH = pathlib.Path(__file__).parent / "system_prompt.txt"
SYSTEM_PROMPT = SP_PATH.read_text(encoding="utf-8") if SP_PATH.exists() else ""
SYSTEM_PROMPT += """

══ CAPACIDADE DE ANÁLISE DE PDFs ══
Quando o usuário enviar um ou mais PDFs, você deve:
1. IDENTIFICAR o tipo de documento: ETP, TR, DFD, Contrato, Parecer, Edital, Processo completo, etc.
2. ANALISAR o conteúdo à luz da legislação MS aplicável.
3. RESPONDER conforme o pedido:
   - RED TEAM: vulnerabilidades jurídicas em Crítico/Alto/Médio/Conforme
   - REVISÃO: problemas e correções sugeridas
   - RESUMO: pontos principais extraídos
   - CHECKLIST: conformidade com requisitos legais MS
4. Para MÚLTIPLOS PDFs: analisar cada um e verificar coerência entre eles
   (ex: se ETP, TR e DFD são consistentes entre si)
5. Sempre citar artigos, decretos e pareceres PGE/MS aplicáveis.
"""

TOOLS = [
    {
        "name": "buscar_pca_pncp",
        "description": "Busca itens do PCA de um órgão na API pública do PNCP.",
        "input_schema": {
            "type": "object",
            "properties": {
                "cnpj":      {"type": "string",  "description": "CNPJ sem pontos/traços"},
                "ano":       {"type": "integer", "description": "Ano do PCA"},
                "sequencia": {"type": "integer", "description": "Sequência do PCA"},
                "pagina":    {"type": "integer", "description": "Página", "default": 1}
            },
            "required": ["cnpj", "ano", "sequencia"]
        }
    },
    {
        "name": "buscar_contratacoes_pncp",
        "description": "Busca contratações no PNCP por palavras-chave.",
        "input_schema": {
            "type": "object",
            "properties": {
                "termo":        {"type": "string",  "description": "Termo de busca"},
                "data_inicial": {"type": "string",  "description": "Data inicial YYYYMMDD"},
                "data_final":   {"type": "string",  "description": "Data final YYYYMMDD"},
                "modalidade":   {"type": "integer", "description": "6=Pregão 8=Inexig 9=Dispensa"},
                "pagina":       {"type": "integer", "description": "Página", "default": 1}
            },
            "required": ["termo"]
        }
    }
]

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

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/config")
def config():
    return jsonify({"cnpj": ORGAO_CNPJ, "ano": PCA_ANO, "seq": PCA_SEQ})

@app.route("/api/chat", methods=["POST"])
def chat():
    if not API_KEY:
        return jsonify({"error": "API Key não configurada."}), 500

    data     = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "Nenhuma mensagem enviada"}), 400

    try:
        client = anthropic.Anthropic(api_key=API_KEY)
        msgs   = list(messages)

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

            texto = " ".join(b.text for b in response.content if hasattr(b, "text"))
            return jsonify({"response": texto})

    except anthropic.AuthenticationError:
        return jsonify({"error": "API Key inválida"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/upload-pdf", methods=["POST"])
def upload_pdf():
    if "files" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    files = request.files.getlist("files")
    pdfs  = []
    erros = []

    if len(files) > MAX_PDFS:
        return jsonify({"error": f"Máximo de {MAX_PDFS} PDFs por vez."}), 400

    for f in files:
        if not f.filename.lower().endswith(".pdf"):
            erros.append(f"{f.filename}: não é um PDF")
            continue
        conteudo   = f.read()
        tamanho_mb = len(conteudo) / (1024 * 1024)
        if tamanho_mb > MAX_PDF_MB:
            erros.append(f"{f.filename}: muito grande ({tamanho_mb:.1f}MB, máx {MAX_PDF_MB}MB)")
            continue
        b64 = base64.standard_b64encode(conteudo).decode("utf-8")
        pdfs.append({"nome": f.filename, "tamanho": f"{tamanho_mb:.1f}MB", "base64": b64})

    return jsonify({"pdfs": pdfs, "erros": erros, "total": len(pdfs)})

@app.route("/api/pca")
def pca():
    cnpj = request.args.get("cnpj", ORGAO_CNPJ)
    ano  = int(request.args.get("ano",  PCA_ANO))
    seq  = int(request.args.get("seq",  PCA_SEQ))
    pag  = int(request.args.get("pag",  1))
    return jsonify(buscar_pca_pncp(cnpj, ano, seq, pag))


@app.route("/api/verificar-senha", methods=["POST"])
def verificar_senha():
    """Verifica a senha mestra de acesso ao sistema."""
    senha_correta = os.environ.get("SENHA_ACESSO", "suplantec2025")
    data = request.get_json()
    senha_digitada = data.get("senha", "")
    return jsonify({"ok": senha_digitada == senha_correta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)

# Rota verificação de senha (adicionada ao final)
# Esta rota já está no app.py principal — garantir que exista
