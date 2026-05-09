<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Assistente de Licitações — SUPLANTEC/SEJUSP</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');
:root{
  --azul:#0D3B8C;--azul-m:#1a5fb4;--azul-c:#4dc3f7;
  --bg:#07152b;--bg2:#0c2040;--bg3:#112850;--borda:#1a3a6b;
  --dourado:#f5cc6a;--dourado-m:#d4a843;
  --verde:#3cc48a;--texto:#ddeef8;--texto-fraco:#6a9ab8;
  --perigo:#e05252;--perigo-bg:rgba(224,82,82,0.1);
}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--texto);min-height:100vh;display:flex;flex-direction:column;}
#tela-login{min-height:100vh;display:flex;align-items:center;justify-content:center;background:radial-gradient(ellipse at 60% 40%,#0d2d6b 0%,#07152b 70%);padding:20px;}
.login-card{background:rgba(12,32,64,0.95);border:1px solid var(--borda);border-radius:20px;padding:40px 36px;width:100%;max-width:420px;box-shadow:0 20px 80px rgba(0,0,0,0.5);text-align:center;}
.login-logo{width:130px;height:130px;object-fit:contain;margin:0 auto 18px;display:block;}
.login-title{font-family:'DM Serif Display',serif;font-size:22px;margin-bottom:4px;}
.login-sub{font-size:11.5px;color:var(--texto-fraco);margin-bottom:5px;line-height:1.5;}
.login-orgao{font-size:11px;color:var(--dourado);margin-bottom:26px;font-weight:600;}
.login-label{display:block;text-align:left;font-size:11px;color:var(--texto-fraco);margin-bottom:6px;font-weight:500;text-transform:uppercase;letter-spacing:.8px;}
.login-input{width:100%;background:var(--bg3);border:1px solid var(--borda);color:var(--texto);padding:12px 16px;border-radius:10px;font-size:14px;font-family:'DM Sans',sans-serif;margin-bottom:16px;outline:none;transition:border-color .2s;}
.login-input:focus{border-color:var(--azul-c);}
.login-input::placeholder{color:var(--texto-fraco);}
.login-btn{width:100%;background:linear-gradient(135deg,var(--azul),var(--azul-m));border:none;border-radius:10px;color:white;padding:13px;font-size:14px;font-weight:600;font-family:'DM Sans',sans-serif;cursor:pointer;transition:all .2s;}
.login-btn:hover{transform:translateY(-1px);box-shadow:0 6px 20px rgba(13,59,140,0.4);}
.login-erro{background:rgba(224,82,82,0.1);border:1px solid rgba(224,82,82,0.3);border-radius:8px;padding:10px 14px;font-size:12px;color:#f08080;margin-bottom:14px;display:none;}
.login-rodape{margin-top:26px;padding-top:18px;border-top:1px solid var(--borda);font-size:10.5px;color:var(--texto-fraco);line-height:1.6;}
.login-rodape strong{color:var(--dourado);}
#app{display:none;flex-direction:column;height:100vh;}
.header{background:var(--bg2);border-bottom:1px solid var(--borda);padding:10px 18px;display:flex;align-items:center;gap:10px;flex-shrink:0;}
.header-logo{width:42px;height:42px;object-fit:contain;border-radius:50%;border:2px solid var(--borda);background:white;padding:2px;}
.header-info h1{font-family:'DM Serif Display',serif;font-size:15px;}
.header-info p{font-size:10px;color:var(--texto-fraco);margin-top:1px;}
.header-right{margin-left:auto;display:flex;gap:6px;align-items:center;flex-wrap:wrap;}
.pill{padding:3px 10px;border-radius:20px;font-size:10px;font-weight:600;}
.pill-gov{background:rgba(13,59,140,0.3);border:1px solid rgba(13,59,140,0.5);color:#7aabf0;}
.pill-pca{background:rgba(212,168,67,0.15);border:1px solid rgba(212,168,67,0.3);color:var(--dourado);}
.pill-pdf{background:rgba(224,82,82,0.15);border:1px solid rgba(224,82,82,0.3);color:#f08080;}
.pill-on{display:flex;align-items:center;gap:5px;background:rgba(42,157,110,0.15);border:1px solid rgba(42,157,110,0.3);color:var(--verde);}
.dot{width:6px;height:6px;background:var(--verde);border-radius:50%;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
.btn-sair{background:transparent;border:1px solid var(--borda);color:var(--texto-fraco);padding:3px 10px;border-radius:6px;font-size:10px;cursor:pointer;font-family:'DM Sans',sans-serif;}
.btn-sair:hover{border-color:var(--perigo);color:#f08080;}
.main{flex:1;display:flex;overflow:hidden;}
.pca-panel{width:290px;flex-shrink:0;background:var(--bg2);border-right:1px solid var(--borda);display:flex;flex-direction:column;overflow:hidden;transition:width .3s;}
.pca-panel.collapsed{width:0;border:none;overflow:hidden;}
.pca-header{padding:12px 14px 10px;border-bottom:1px solid var(--borda);flex-shrink:0;}
.pca-header-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;}
.pca-titulo{font-family:'DM Serif Display',serif;font-size:13px;color:var(--dourado);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.btn-reload{background:transparent;border:1px solid var(--borda);color:var(--texto-fraco);padding:3px 8px;border-radius:6px;font-size:11px;cursor:pointer;font-family:'DM Sans',sans-serif;}
.pca-filtro input{width:100%;background:var(--bg3);border:1px solid var(--borda);color:var(--texto);padding:6px 10px;border-radius:7px;font-size:11.5px;font-family:'DM Sans',sans-serif;outline:none;}
.pca-filtro input:focus{border-color:var(--azul-c);}
.pca-filtro input::placeholder{color:var(--texto-fraco);}
.pca-stats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;padding:8px 14px;border-bottom:1px solid var(--borda);flex-shrink:0;}
.stat-box{background:var(--bg3);border:1px solid #1e3f6b;border-radius:7px;padding:6px 8px;text-align:center;}
.stat-num{font-family:'DM Serif Display',serif;font-size:16px;color:var(--azul-c);}
.stat-num.v{color:var(--verde)}.stat-num.d{color:var(--dourado);}
.stat-label{font-size:9px;color:var(--texto-fraco);text-transform:uppercase;letter-spacing:.6px;margin-top:1px;}
.pca-lista{flex:1;overflow-y:auto;padding:8px 10px;scrollbar-width:thin;scrollbar-color:var(--borda) transparent;}
.pca-loading{text-align:center;padding:24px 12px;color:var(--texto-fraco);font-size:12px;}
.spin{display:inline-block;animation:spin 1s linear infinite;font-size:20px;}
@keyframes spin{to{transform:rotate(360deg)}}
.item-pca{background:var(--bg3);border:1px solid #1e3f6b;border-radius:8px;padding:8px 10px;margin-bottom:6px;cursor:pointer;transition:all .2s;}
.item-pca:hover{border-color:var(--azul-c);background:rgba(26,95,180,0.1);}
.item-pca.sel{border-color:var(--dourado-m);background:rgba(212,168,67,0.07);}
.item-num{font-size:9px;color:var(--texto-fraco);margin-bottom:2px;}
.item-desc{font-size:11px;color:var(--texto);line-height:1.4;margin-bottom:4px;font-weight:500;}
.item-meta{display:flex;gap:4px;flex-wrap:wrap;}
.tag{font-size:9px;padding:2px 6px;border-radius:10px;font-weight:600;}
.tv{background:rgba(42,157,110,0.15);border:1px solid rgba(42,157,110,0.25);color:var(--verde);}
.tc{background:rgba(26,95,180,0.15);border:1px solid rgba(26,95,180,0.25);color:var(--azul-c);}
.ts-n{background:rgba(217,79,79,0.12);border:1px solid rgba(217,79,79,0.25);color:#f08080;}
.ts-s{background:rgba(42,157,110,0.12);border:1px solid rgba(42,157,110,0.25);color:var(--verde);}
.chat-area{flex:1;display:flex;flex-direction:column;overflow:hidden;}
.sugestoes{background:var(--bg2);border-bottom:1px solid var(--borda);padding:7px 14px;display:flex;gap:6px;overflow-x:auto;flex-shrink:0;scrollbar-width:none;}
.sugestoes::-webkit-scrollbar{display:none;}
.chip{flex-shrink:0;background:var(--bg3);border:1px solid var(--borda);color:var(--texto-fraco);padding:4px 11px;border-radius:15px;font-size:10.5px;cursor:pointer;white-space:nowrap;font-family:'DM Sans',sans-serif;}
.chip:hover{border-color:var(--azul-c);color:var(--azul-c);}
.chip-pca{border-color:rgba(212,168,67,0.3);color:rgba(212,168,67,0.8);}
.chip-pca:hover{border-color:var(--dourado-m);color:var(--dourado);}
.chip-pdf{border-color:rgba(224,82,82,0.3);color:rgba(240,128,128,0.9);}
.chip-pdf:hover{border-color:var(--perigo);color:#f08080;}
.mensagens{flex:1;overflow-y:auto;padding:18px;display:flex;flex-direction:column;gap:13px;scrollbar-width:thin;scrollbar-color:var(--borda) transparent;}
.bv{text-align:center;padding:20px;}
.bv-logo{width:90px;height:90px;object-fit:contain;margin:0 auto 12px;display:block;}
.bv h2{font-family:'DM Serif Display',serif;font-size:20px;margin-bottom:3px;}
.bv-orgao{font-size:11px;color:var(--dourado);font-weight:600;margin-bottom:12px;}
.bv p{font-size:12px;color:var(--texto-fraco);max-width:440px;margin:0 auto;line-height:1.6;}
.bv-banners{max-width:480px;margin:10px auto 0;display:flex;flex-direction:column;gap:6px;}
.bv-banner{border-radius:8px;padding:8px 12px;font-size:11px;text-align:left;line-height:1.6;}
.bv-pca{background:rgba(212,168,67,0.07);border:1px solid rgba(212,168,67,0.22);color:rgba(212,168,67,0.85);}
.bv-pdf{background:rgba(224,82,82,0.07);border:1px solid rgba(224,82,82,0.22);color:rgba(240,128,128,0.85);}
.bv-ms{background:rgba(13,59,140,0.1);border:1px solid rgba(26,95,180,0.25);color:rgba(77,195,247,0.85);}
.bv-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;max-width:480px;margin:10px auto 0;}
.bv-card{background:var(--bg3);border:1px solid var(--borda);border-radius:8px;padding:9px 11px;text-align:left;cursor:pointer;transition:all .2s;}
.bv-card:hover{border-color:var(--azul-c);background:rgba(26,95,180,0.08);transform:translateY(-1px);}
.bv-card-icon{font-size:15px;margin-bottom:3px;display:block;}
.bv-card-titulo{font-size:11px;font-weight:600;}
.bv-card-desc{font-size:10px;color:var(--texto-fraco);margin-top:1px;}
.ctx-banner{margin:8px 14px 0;background:rgba(212,168,67,0.07);border:1px solid rgba(212,168,67,0.22);border-radius:8px;padding:7px 12px;font-size:11px;color:var(--dourado);display:flex;align-items:center;gap:7px;flex-shrink:0;}
.ctx-banner button{margin-left:auto;background:transparent;border:none;color:var(--texto-fraco);cursor:pointer;}
.pdf-area{margin:0 14px;flex-shrink:0;}
.pdf-drop{border:2px dashed var(--borda);border-radius:10px;padding:12px;text-align:center;cursor:pointer;background:var(--bg3);margin-bottom:8px;}
.pdf-drop:hover{border-color:var(--perigo);}
.pdf-lista{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:6px;}
.pdf-item{display:flex;align-items:center;gap:6px;background:var(--bg3);border:1px solid rgba(224,82,82,0.3);border-radius:8px;padding:5px 10px;font-size:11px;color:#f08080;}
.pdf-item button{background:transparent;border:none;color:var(--texto-fraco);cursor:pointer;}
.pdf-acoes{display:flex;gap:6px;margin-bottom:8px;flex-wrap:wrap;}
.btn-acao{background:transparent;border:1px solid rgba(224,82,82,0.4);color:#f08080;padding:5px 11px;border-radius:8px;font-size:11px;cursor:pointer;font-family:'DM Sans',sans-serif;}
.btn-acao:hover,.btn-acao.active{background:var(--perigo-bg);border-color:var(--perigo);}
.msg{display:flex;gap:8px;max-width:820px;}
.msg-u{flex-direction:row-reverse;align-self:flex-end;}
.msg-a{align-self:flex-start;}
.msg-av{width:30px;height:30px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:13px;flex-shrink:0;margin-top:2px;}
.av-u{background:rgba(26,95,180,0.3);border:1px solid rgba(26,95,180,0.4);}
.av-a{background:linear-gradient(135deg,var(--azul),var(--azul-m));}
.msg-balao{padding:10px 14px;border-radius:12px;font-size:13px;line-height:1.75;max-width:700px;}
.msg-u .msg-balao{background:rgba(26,95,180,0.2);border:1px solid rgba(26,95,180,0.3);border-top-right-radius:3px;}
.msg-a .msg-balao{background:var(--bg2);border:1px solid var(--borda);border-top-left-radius:3px;}
.msg-balao strong{color:var(--dourado);font-weight:600;}
.msg-balao ul,.msg-balao ol{padding-left:16px;margin:6px 0;}
.msg-balao li{margin-bottom:3px;}
.pdf-badge{display:inline-flex;align-items:center;gap:4px;background:var(--perigo-bg);border:1px solid rgba(224,82,82,0.3);border-radius:6px;padding:3px 8px;font-size:10px;color:#f08080;margin-bottom:6px;margin-right:4px;}
.msg-tempo{font-size:9px;color:var(--texto-fraco);margin-top:3px;}
.msg-u .msg-tempo{text-align:right;}
.digitando{display:flex;gap:8px;align-items:center;}
.dots{background:var(--bg2);border:1px solid var(--borda);border-radius:12px;border-top-left-radius:3px;padding:10px 15px;display:flex;gap:4px;}
.dots span{width:5px;height:5px;background:var(--azul-c);border-radius:50%;animation:bounce 1.2s infinite;}
.dots span:nth-child(2){animation-delay:.2s}.dots span:nth-child(3){animation-delay:.4s}
@keyframes bounce{0%,80%,100%{transform:scale(.65);opacity:.4}40%{transform:scale(1);opacity:1}}
.input-area{background:var(--bg2);border-top:1px solid var(--borda);padding:10px 14px;flex-shrink:0;}
.input-wrap{display:flex;gap:8px;align-items:flex-end;background:var(--bg3);border:1px solid var(--borda);border-radius:12px;padding:8px 12px;transition:border-color .2s;}
.input-wrap:focus-within{border-color:var(--azul-c);}
#input-msg{flex:1;background:transparent;border:none;color:var(--texto);font-family:'DM Sans',sans-serif;font-size:13px;resize:none;outline:none;max-height:100px;min-height:20px;line-height:1.5;}
#input-msg::placeholder{color:var(--texto-fraco);}
.btn-attach{width:32px;height:32px;background:transparent;border:1px solid rgba(224,82,82,0.3);border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:15px;color:#f08080;flex-shrink:0;}
.btn-send{width:34px;height:34px;background:linear-gradient(135deg,var(--azul),var(--azul-m));border:none;border-radius:8px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;}
.btn-send:hover{transform:scale(1.05);}
.btn-send:disabled{opacity:.35;cursor:not-allowed;transform:none;}
.input-dica{font-size:9.5px;color:var(--texto-fraco);text-align:center;margin-top:5px;}
.btn-toggle{background:var(--bg3);border:1px solid var(--borda);color:var(--texto-fraco);padding:4px 10px;border-radius:6px;font-size:10.5px;cursor:pointer;font-family:'DM Sans',sans-serif;}
.rodape{background:var(--bg2);border-top:1px solid var(--borda);padding:6px 18px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0;}
.rodape p{font-size:10px;color:var(--texto-fraco);}
.rodape strong{color:var(--azul-c);}
.cred strong{color:var(--dourado);}
#file-input{display:none;}
@media(max-width:640px){.pca-panel{display:none;}}
</style>
</head>
<body>

<!-- LOGIN -->
<div id="tela-login">
  <div class="login-card">
    <img src="/logo.png" class="login-logo" alt="SUPLANTEC/SEJUSP">
    <h1 class="login-title">Assistente de Licitações</h1>
    <p class="login-sub">SUPLANTEC · Superintendência de Planejamento,<br>Tecnologia e Projetos</p>
    <p class="login-orgao">SEJUSP · Governo de Mato Grosso do Sul</p>
    <div id="login-erro" class="login-erro">Senha incorreta. Tente novamente.</div>
    <label class="login-label" for="campo-senha">Senha de acesso</label>
    <input type="password" id="campo-senha" class="login-input" placeholder="Digite a senha">
    <button class="login-btn" id="btn-entrar">Entrar no Sistema</button>
    <div class="login-rodape">
      Desenvolvido por <strong>Alexander Santos</strong><br>
      SUPLANTEC · SEJUSP · Governo de Mato Grosso do Sul
    </div>
  </div>
</div>

<!-- APP -->
<div id="app">
  <div class="header">
    <img src="/logo.png" class="header-logo" alt="SUPLANTEC">
    <div class="header-info">
      <h1>Assistente de Licitações — SUPLANTEC/SEJUSP</h1>
      <p>Lei 14.133/2021 · Decretos MS · Pareceres PGE/MS · PCA PNCP · PDF</p>
    </div>
    <div class="header-right">
      <span class="pill pill-gov">SEJUSP/MS</span>
      <span class="pill pill-pca">PCA</span>
      <span class="pill pill-pdf">PDF</span>
      <button class="btn-toggle" id="btn-toggle-pca">PCA ▲</button>
      <span class="pill pill-on"><span class="dot"></span>Online</span>
      <button class="btn-sair" id="btn-sair">Sair</button>
    </div>
  </div>

  <div class="main">
    <div class="pca-panel" id="pca-panel">
      <div class="pca-header">
        <div class="pca-header-top">
          <span class="pca-titulo" id="pca-titulo">PCA...</span>
          <button class="btn-reload" id="btn-reload">↺</button>
        </div>
        <div class="pca-filtro">
          <input type="text" id="pca-busca" placeholder="Buscar item...">
        </div>
      </div>
      <div class="pca-stats" id="pca-stats" style="display:none">
        <div class="stat-box"><div class="stat-num" id="st-t">—</div><div class="stat-label">Itens</div></div>
        <div class="stat-box"><div class="stat-num v" id="st-c">—</div><div class="stat-label">Contratados</div></div>
        <div class="stat-box"><div class="stat-num d" id="st-v">—</div><div class="stat-label">Total</div></div>
      </div>
      <div class="pca-lista" id="pca-lista">
        <div class="pca-loading"><div class="spin">⏳</div><br>Carregando PCA...</div>
      </div>
    </div>

    <div class="chat-area">
      <div class="sugestoes">
        <button class="chip chip-pca" id="c1">📋 Analisar item PCA</button>
        <button class="chip chip-pdf" id="c2">📄 Enviar PDF</button>
        <button class="chip chip-pdf" id="c3">🔴 Red Team</button>
        <button class="chip chip-pdf" id="c4">✏️ Revisão</button>
        <button class="chip chip-pdf" id="c5">☑️ Checklist</button>
        <a href="/pesquisa-precos" class="chip" style="text-decoration:none;color:inherit;display:inline-flex;align-items:center;gap:4px;background:rgba(42,157,110,0.08);border-color:rgba(42,157,110,0.3);color:var(--verde);">🔍 Pesquisa de Preços</a>
        <a href="/modelos" class="chip" style="text-decoration:none;color:inherit;display:inline-flex;align-items:center;gap:4px;background:rgba(212,168,67,0.08);border-color:rgba(212,168,67,0.3);color:var(--dourado);">📚 Processos Modelo</a>
        <button class="chip" id="c6">✅ Dispensa MS</button>
        <button class="chip" id="c7">🏛️ PR PGE/MS</button>
        <button class="chip" id="c8">💰 Pesquisa preços</button>
      </div>

      <div id="ctx" style="display:none">
        <div class="ctx-banner">
          <span>📌</span>
          <span id="ctx-txt">Item PCA</span>
          <button id="btn-ctx-fechar">✕</button>
        </div>
      </div>

      <div class="pdf-area" id="pdf-area" style="display:none">
        <div class="pdf-drop" id="pdf-drop">
          <div style="font-size:22px">📄</div>
          <p style="font-size:12px;color:var(--texto-fraco);margin-top:4px">Clique ou arraste PDFs (máx. 5 por vez)</p>
        </div>
        <div class="pdf-lista" id="pdf-lista"></div>
        <div class="pdf-acoes" id="pdf-acoes" style="display:none">
          <span style="font-size:11px;color:var(--texto-fraco);align-self:center">Analisar como:</span>
          <button class="btn-acao" id="a1">🔴 Red Team</button>
          <button class="btn-acao" id="a2">✏️ Revisão</button>
          <button class="btn-acao" id="a3">☑️ Checklist</button>
          <button class="btn-acao" id="a4">📝 Resumo</button>
          <button class="btn-acao" id="a5">💬 Livre</button>
        </div>
      </div>

      <input type="file" id="file-input" accept=".pdf" multiple>

      <div class="mensagens" id="mensagens">
        <div class="bv" id="bv">
          <img src="/logo.png" class="bv-logo" alt="SUPLANTEC">
          <h2>Assistente de Licitações</h2>
          <p class="bv-orgao">SUPLANTEC · SEJUSP · Governo de Mato Grosso do Sul</p>
          <p>Pergunte sobre licitações ou envie PDFs para análise completa de processos.</p>
          <div class="bv-banners">
            <div class="bv-banner bv-pca">📅 <b>PCA integrado ao PNCP.</b> Clique em qualquer item para análise automática.</div>
            <div class="bv-banner bv-pdf">📄 <b>Análise de PDFs:</b> red team, revisão, checklist ou resumo de processos.</div>
            <div class="bv-banner bv-ms">🏛️ <b>Base legal completa:</b> 20 Decretos MS · Pareceres PGE/MS 2022–2025 · Lei 14.133/2021.</div>
          </div>
          <div class="bv-grid">
            <div class="bv-card" id="bv1"><span class="bv-card-icon">🔴</span><div class="bv-card-titulo">Red Team</div><div class="bv-card-desc">Análise crítica de processo</div></div>
            <div class="bv-card" id="bv2"><span class="bv-card-icon">☑️</span><div class="bv-card-titulo">Checklist</div><div class="bv-card-desc">Conformidade legal MS</div></div>
            <div class="bv-card" id="bv3"><span class="bv-card-icon">✅</span><div class="bv-card-titulo">Dispensa por valor</div><div class="bv-card-desc">PR 005-2025 · SDE</div></div>
            <div class="bv-card" id="bv4"><span class="bv-card-icon">📋</span><div class="bv-card-titulo">Pareceres PGE/MS</div><div class="bv-card-desc">Referenciais 2022–2025</div></div>
            <a href="/pesquisa-precos" style="text-decoration:none" class="bv-card"><span class="bv-card-icon">🔍</span><div class="bv-card-titulo" style="color:var(--verde)">Pesquisa de Preços</div><div class="bv-card-desc">Automática · 3 fontes · Excel</div></a>
            <a href="/modelos" style="text-decoration:none" class="bv-card"><span class="bv-card-icon">📚</span><div class="bv-card-titulo" style="color:var(--dourado)">Processos Modelo</div><div class="bv-card-desc">5 tipos · Word · Checklist</div></a>
          </div>
        </div>
      </div>

      <div class="input-area">
        <div class="input-wrap">
          <button class="btn-attach" id="btn-attach" title="Anexar PDF">📄</button>
          <textarea id="input-msg" placeholder="Pergunte sobre licitações ou envie um PDF..." rows="1"></textarea>
          <button class="btn-send" id="btn-send">➤</button>
        </div>
        <div class="input-dica">📄 Anexar PDF · Enter para enviar · Shift+Enter nova linha</div>
      </div>
    </div>
  </div>

  <div class="rodape">
    <p><strong>SUPLANTEC</strong> · Superintendência de Planejamento, Tecnologia e Projetos · SEJUSP/MS</p>
    <p class="cred">Desenvolvido por <strong>Alexander Santos</strong> · v2.0 · Lei 14.133/2021</p>
  </div>
</div>

<script>
(function() {
  // Estado global
  var HIST = [], AGUARD = false, PDFS = [], ACAO = 'livre';
  var ITENS = [], FILT = [], SEL = null, PCA_ABERTO = true;
  var CFG = { cnpj: '03015475000140', ano: 2026, seq: 3 };

  // ── HELPERS ──
  function g(id) { return document.getElementById(id); }
  function hora() { return new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }); }
  function escBV() { var b = g('bv'); if (b) b.style.display = 'none'; }

  // ── LOGIN ──
  g('btn-entrar').addEventListener('click', function() {
    var senha = g('campo-senha').value;
    if (!senha) return;
    fetch('/api/verificar-senha', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ senha: senha })
    })
    .then(function(r) { return r.json(); })
    .then(function(d) {
      if (d.ok) {
        sessionStorage.setItem('auth', 'ok');
        sessionStorage.setItem('session_token', d.token || '');
        g('tela-login').style.display = 'none';
        g('app').style.display = 'flex';
        iniciar();
      } else {
        g('login-erro').style.display = 'block';
        g('campo-senha').value = '';
        setTimeout(function() { g('login-erro').style.display = 'none'; }, 3000);
      }
    })
    .catch(function() { alert('Erro de conexão.'); });
  });

  g('campo-senha').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') g('btn-entrar').click();
  });

  g('btn-sair').addEventListener('click', function() {
    sessionStorage.removeItem('auth');
    g('app').style.display = 'none';
    g('tela-login').style.display = 'flex';
    g('campo-senha').value = '';
    HIST = [];
  });

  // Verificar sessão
  if (sessionStorage.getItem('auth') === 'ok') {
    g('tela-login').style.display = 'none';
    g('app').style.display = 'flex';
    document.addEventListener('DOMContentLoaded', iniciar);
    iniciar();
  }

  // ── PCA ──
  function iniciar() {
    authFetch('/api/config')
      .then(function(r) { return r.ok ? r.json() : CFG; })
      .then(function(d) { CFG = d; g('pca-titulo').textContent = 'PCA ' + CFG.ano; carregarPCA(); })
      .catch(function() { carregarPCA(); });
  }

  function carregarPCA() {
    var l = g('pca-lista');
    g('pca-stats').style.display = 'none';
    l.innerHTML = '<div class="pca-loading"><div class="spin">⏳</div><br>Carregando...</div>';
    authFetch('/api/pca?cnpj=' + CFG.cnpj + '&ano=' + CFG.ano + '&seq=' + CFG.seq)
      .then(function(r) { return r.json(); })
      .then(function(d) {
        if (d.status === 'erro') { l.innerHTML = '<div class="pca-loading">⚠️ Erro PNCP</div>'; return; }
        ITENS = d.itens || []; FILT = ITENS;
        g('pca-stats').style.display = 'grid';
        g('st-t').textContent = ITENS.length;
        var cont = ITENS.filter(function(i) { return (i.situacaoCompraItem || '').toLowerCase().indexOf('contrat') >= 0; }).length;
        g('st-c').textContent = cont || '—';
        var val = ITENS.reduce(function(s, i) { return s + parseFloat(i.valorTotal || i.valor || 0); }, 0);
        g('st-v').textContent = val > 0 ? 'R$' + (val / 1000000).toFixed(1) + 'M' : '—';
        renderLista(FILT);
      })
      .catch(function() { l.innerHTML = '<div class="pca-loading">⚠️ Erro de conexão</div>'; });
  }

  g('btn-reload').addEventListener('click', carregarPCA);

  g('pca-busca').addEventListener('input', function() {
    var b = this.value.toLowerCase();
    FILT = b ? ITENS.filter(function(i) {
      var d = (i.descricao || i.objetoContratacao || '').toLowerCase();
      var c = (i.categoriaItemPca && i.categoriaItemPca.descricao) ? i.categoriaItemPca.descricao.toLowerCase() : '';
      return d.indexOf(b) >= 0 || c.indexOf(b) >= 0;
    }) : ITENS;
    renderLista(FILT);
  });

  function renderLista(itens) {
    var l = g('pca-lista');
    if (!itens.length) { l.innerHTML = '<div class="pca-loading">Nenhum item.</div>'; return; }
    l.innerHTML = itens.map(function(item, idx) {
      var num = item.numeroItem || (idx + 1);
      var desc = item.descricao || item.objetoContratacao || 'Sem descrição';
      var val = parseFloat(item.valorTotal || item.valor || 0);
      var vf = val > 0 ? 'R$ ' + val.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) : '';
      var cat = (item.categoriaItemPca && item.categoriaItemPca.descricao) ? item.categoriaItemPca.descricao : '';
      var cont = (item.situacaoCompraItem || '').toLowerCase().indexOf('contrat') >= 0;
      var sel = SEL && SEL._idx === idx;
      return '<div class="item-pca' + (sel ? ' sel' : '') + '" data-idx="' + idx + '">'
        + '<div class="item-num">Item ' + num + '</div>'
        + '<div class="item-desc">' + (desc.length > 75 ? desc.substring(0, 75) + '...' : desc) + '</div>'
        + '<div class="item-meta">'
        + (vf ? '<span class="tag tv">' + vf + '</span>' : '')
        + (cat ? '<span class="tag tc">' + cat.substring(0, 20) + '</span>' : '')
        + '<span class="tag ' + (cont ? 'ts-s' : 'ts-n') + '">' + (cont ? '✓ Contratado' : 'Pendente') + '</span>'
        + '</div></div>';
    }).join('');
    l.querySelectorAll('.item-pca').forEach(function(el) {
      el.addEventListener('click', function() { selItem(parseInt(this.getAttribute('data-idx'))); });
    });
  }

  function selItem(idx) {
    var item = FILT[idx]; item._idx = idx; SEL = item;
    renderLista(FILT);
    var desc = item.descricao || item.objetoContratacao || 'Item';
    var val = parseFloat(item.valorTotal || item.valor || 0);
    var vf = val > 0 ? ' · R$' + val.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) : '';
    g('ctx-txt').textContent = 'Item ' + (item.numeroItem || (idx + 1)) + ': ' + desc.substring(0, 50) + '...' + vf;
    g('ctx').style.display = 'block';
    enviarTexto('Analise item do PCA ' + CFG.ano + ':\nItem: ' + (item.numeroItem || (idx + 1)) + '\nDescrição: ' + desc + '\nValor: ' + (vf || 'não informado') + '\nCategoria: ' + (item.categoriaItemPca && item.categoriaItemPca.descricao ? item.categoriaItemPca.descricao : 'não informada') + '\nOriente: 1) Modalidade com fundamento legal; 2) Parecer PGE/MS; 3) Checklist; 4) Alertas MS.');
  }

  g('btn-ctx-fechar').addEventListener('click', function() { SEL = null; g('ctx').style.display = 'none'; renderLista(FILT); });
  g('btn-toggle-pca').addEventListener('click', function() {
    PCA_ABERTO = !PCA_ABERTO;
    g('pca-panel').classList.toggle('collapsed', !PCA_ABERTO);
    this.textContent = 'PCA ' + (PCA_ABERTO ? '▲' : '▼');
  });

  // ── PDF ──
  function abrirPDF() { g('pdf-area').style.display = 'block'; g('file-input').click(); }

  function setAcao(a) {
    ACAO = a;
    ['a1','a2','a3','a4','a5'].forEach(function(id, i) {
      var acoes = ['redteam','revisao','checklist','resumo','livre'];
      var b = g(id); if (b) b.classList.toggle('active', acoes[i] === a);
    });
  }

  g('btn-attach').addEventListener('click', abrirPDF);
  g('c2').addEventListener('click', abrirPDF);
  g('c3').addEventListener('click', function() { abrirPDF(); setAcao('redteam'); });
  g('c4').addEventListener('click', function() { abrirPDF(); setAcao('revisao'); });
  g('c5').addEventListener('click', function() { abrirPDF(); setAcao('checklist'); });
  g('a1').addEventListener('click', function() { setAcao('redteam'); });
  g('a2').addEventListener('click', function() { setAcao('revisao'); });
  g('a3').addEventListener('click', function() { setAcao('checklist'); });
  g('a4').addEventListener('click', function() { setAcao('resumo'); });
  g('a5').addEventListener('click', function() { setAcao('livre'); });
  g('bv1').addEventListener('click', function() { abrirPDF(); setAcao('redteam'); });
  g('bv2').addEventListener('click', function() { abrirPDF(); setAcao('checklist'); });

  g('pdf-drop').addEventListener('click', function() { g('file-input').click(); });
  g('pdf-drop').addEventListener('dragover', function(e) { e.preventDefault(); this.style.borderColor='var(--perigo)'; });
  g('pdf-drop').addEventListener('dragleave', function() { this.style.borderColor=''; });
  g('pdf-drop').addEventListener('drop', function(e) { e.preventDefault(); this.style.borderColor=''; processarPDFs(e.dataTransfer.files); });
  g('file-input').addEventListener('change', function() { processarPDFs(this.files); });

  function processarPDFs(files) {
    if (!files.length) return;
    g('pdf-area').style.display = 'block';
    var fd = new FormData();
    Array.from(files).forEach(function(f) { fd.append('files', f); });
    authFetch('/api/upload-pdf', { method: 'POST', body: fd })
      .then(function(r) { return r.json(); })
      .then(function(d) {
        if (d.erros && d.erros.length) alert('Atenção:\n' + d.erros.join('\n'));
        PDFS = PDFS.concat(d.pdfs || []);
        renderPDFs();
        if (PDFS.length) g('pdf-acoes').style.display = 'flex';
      })
      .catch(function(e) { alert('Erro upload: ' + e.message); });
  }

  function renderPDFs() {
    var l = g('pdf-lista');
    l.innerHTML = PDFS.map(function(p, i) {
      return '<div class="pdf-item">📄 ' + p.nome + ' <span style="color:var(--texto-fraco)">(' + p.tamanho + ')</span><button data-i="' + i + '">✕</button></div>';
    }).join('');
    l.querySelectorAll('button').forEach(function(b) {
      b.addEventListener('click', function() {
        PDFS.splice(parseInt(this.getAttribute('data-i')), 1);
        renderPDFs();
        if (!PDFS.length) g('pdf-acoes').style.display = 'none';
      });
    });
  }

  // ── CHIPS ──
  g('c1').addEventListener('click', function() { enviarTexto('Com base no item do PCA selecionado, qual a modalidade indicada e documentos necessários?'); });
  g('c6').addEventListener('click', function() { enviarTexto('Como fazer dispensa por valor em MS? Passo a passo.'); });
  g('c7').addEventListener('click', function() { enviarTexto('Qual parecer PGE/MS usar para contratar um curso de capacitação?'); });
  g('c8').addEventListener('click', function() { enviarTexto('Como fazer pesquisa de preços no MS segundo o Dec. 15.940/22?'); });
  g('bv3').addEventListener('click', function() { enviarTexto('Como funciona a dispensa por valor em MS? Passo a passo.'); });
  g('bv4').addEventListener('click', function() { enviarTexto('Quais pareceres referenciais da PGE/MS posso usar sem nova consulta jurídica?'); });

  // ── CHAT ──
  function fmt(t) {
    return t
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/^#{1,3} (.*$)/gm, '<strong style="font-size:13px;color:var(--dourado);display:block;margin-top:9px">$1</strong>')
      .replace(/^- (.*$)/gm, '<li>$1</li>')
      .replace(/(<li>.*<\/li>)/g, function(m) { return '<ul>' + m + '</ul>'; })
      .replace(/^(\d+)\. (.*$)/gm, '<li>$2</li>')
      .replace(/\n\n/g, '</p><p style="margin-top:6px">')
      .replace(/\n/g, '<br>');
  }

  function addMsg(texto, tipo, pdfs) {
    pdfs = pdfs || [];
    escBV();
    var c = g('mensagens');
    var d = document.createElement('div');
    d.className = 'msg msg-' + (tipo === 'u' ? 'u' : 'a');
    var badges = pdfs.map(function(n) { return '<span class="pdf-badge">📄 ' + n + '</span>'; }).join('');
    d.innerHTML = '<div class="msg-av ' + (tipo === 'u' ? 'av-u' : 'av-a') + '">' + (tipo === 'u' ? '👤' : '⚖️') + '</div>'
      + '<div><div class="msg-balao">' + badges + fmt(texto) + '</div>'
      + '<div class="msg-tempo">' + hora() + '</div></div>';
    c.appendChild(d);
    c.scrollTop = c.scrollHeight;
  }

  function showDig() {
    escBV();
    var c = g('mensagens');
    var d = document.createElement('div');
    d.className = 'digitando'; d.id = 'dig';
    d.innerHTML = '<div class="msg-av av-a">⚖️</div><div class="dots"><span></span><span></span><span></span></div>';
    c.appendChild(d);
    c.scrollTop = c.scrollHeight;
  }

  function hideDig() { var d = g('dig'); if (d) d.remove(); }

  function enviarTexto(t) { g('input-msg').value = t; enviar(); }

  function enviar() {
    if (AGUARD) return;
    var inp = g('input-msg');
    var t = inp.value.trim();
    var nomes = [], content = [];

    if (PDFS.length) {
      var labels = {
        redteam: 'Faça um RED TEAM completo identificando vulnerabilidades jurídicas em Crítico, Alto, Médio e Conforme com base na legislação MS.',
        revisao: 'Revise este documento apontando problemas e sugestões com base na legislação MS.',
        checklist: 'Faça um CHECKLIST de conformidade verificando todos os requisitos legais MS.',
        resumo: 'Faça um RESUMO executivo extraindo os pontos mais relevantes.',
        livre: t || 'Analise este documento.'
      };
      var perg = ACAO === 'livre' ? (t || 'Analise este documento.') : labels[ACAO];
      nomes = PDFS.map(function(p) { return p.nome; });
      content = PDFS.map(function(p) {
        return { type: 'document', source: { type: 'base64', media_type: 'application/pdf', data: p.base64 }, title: p.nome };
      });
      content.push({ type: 'text', text: perg });
      if (!t) t = perg;
    } else {
      if (!t) return;
      content = [{ type: 'text', text: t }];
    }

    inp.value = ''; inp.style.height = 'auto';
    AGUARD = true; g('btn-send').disabled = true;
    addMsg(t, 'u', nomes);
    HIST.push({ role: 'user', content: content });

    if (PDFS.length) {
      PDFS = []; renderPDFs();
      g('pdf-acoes').style.display = 'none';
      g('pdf-area').style.display = 'none';
    }

    showDig();

    authFetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: HIST })
    })
    .then(function(r) { return r.json().then(function(d) { return { ok: r.ok, d: d }; }); })
    .then(function(res) {
      hideDig();
      if (!res.ok) throw new Error(res.d.error || 'Erro HTTP');
      HIST.push({ role: 'assistant', content: res.d.response });
      addMsg(res.d.response, 'a');
    })
    .catch(function(e) { hideDig(); addMsg('⚠️ Erro: ' + e.message, 'a'); })
    .finally(function() {
      AGUARD = false; g('btn-send').disabled = false; g('input-msg').focus();
    });
  }

  g('btn-send').addEventListener('click', enviar);
  g('input-msg').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); enviar(); }
  });
  g('input-msg').addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 100) + 'px';
  });

})();
</script>
</body>
</html>
