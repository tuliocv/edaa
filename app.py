"""NEON COMPLEXITY: FPS retrô de revisão acadêmica, em Streamlit.
Uso: streamlit run app.py
Questões de treinamento inéditas, alinhadas às competências dos materiais fornecidos.
"""
import random
import math
import json
from datetime import datetime
import streamlit as st

st.set_page_config(page_title='NEON COMPLEXITY | Operação Big-O', page_icon='⚡', layout='wide', initial_sidebar_state='expanded')

CSS = r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Press+Start+2P&display=swap');
:root{--navy:#182640;--ink:#24324a;--sub:#53627a;--blue:#2463a5;--green:#147d56;--orange:#b45c19;--line:#dce4ee;--bg:#fff}
html,body,[class*="css"],.stApp{font-family:'Rajdhani',system-ui,sans-serif!important}
.stApp{background:#fff!important;color:var(--ink)!important}
[data-testid="stHeader"]{background:#fff!important}
[data-testid="stSidebar"]{background:#f7f9fc!important;border-right:1px solid var(--line)!important}
[data-testid="stSidebar"] *{color:var(--ink)}
.block-container{padding-top:1.4rem;max-width:1120px;padding-bottom:3rem}
h1,h2,h3,h4{font-family:'Rajdhani',sans-serif!important;color:var(--navy)!important;letter-spacing:.005em;font-weight:700!important}
p,li,label{font-size:1.06rem!important;color:var(--ink)}
.smallcap{font-family:'Press Start 2P',monospace;font-size:.59rem;line-height:2;color:#265b91;letter-spacing:.03em}
.hero{padding:2rem 1.75rem;border:1px solid #c9d9e9;border-left:6px solid #2364a5;border-radius:14px;background:#f2f7fc;box-shadow:0 6px 18px rgba(24,38,64,.06)}
.hero-title{font-family:'Press Start 2P',monospace;color:#1b497b;font-size:clamp(1.15rem,2.7vw,2rem);line-height:1.8;overflow-wrap:anywhere}
.hero-sub{color:#3c536c;font-size:1.18rem;margin-top:.5rem}
.stat{background:#fff;border:1px solid #dbe5ee;border-top:3px solid #2d699f;border-radius:10px;padding:15px 13px;min-height:95px;box-shadow:0 2px 8px rgba(25,52,80,.04)}
.stat .value{font-family:'Rajdhani',sans-serif;font-size:1.75rem;font-weight:700;color:#1c527f;line-height:1.4}
.stat .label{font-size:.92rem;color:#53627a;text-transform:uppercase;letter-spacing:.035em}
.mission{border:1px solid #dae3ed;border-radius:12px;background:#f8fafd;padding:1.15rem 1.35rem;margin:1rem 0}
.mission-title{color:#1c527f;font-weight:700;font-size:1.3rem;line-height:1.45}
.lore{color:#4c5e75;font-size:1.04rem;line-height:1.5}
.code-frame{background:#f5f7fb;border:1px solid #dce4ec;padding:16px 17px;border-radius:10px;font:.98rem/1.7 'Consolas','Courier New',monospace;color:#203c65;white-space:pre-wrap;overflow-x:auto}
[data-testid="stRadio"]{background:#fff;border:1px solid #dce4ee;border-radius:12px;padding:14px 16px}
[data-testid="stRadio"] label{font-size:1.06rem!important;line-height:1.55!important;color:#263852!important}
[data-testid="stRadio"] [role="radiogroup"]{gap:.35rem}
[data-testid="stRadio"] label[data-baseweb="radio"]{border:1px solid #e2e9f0;border-radius:8px;padding:9px 12px;background:#fff}
[data-testid="stRadio"] label[data-baseweb="radio"]:hover{background:#f1f6fc;border-color:#9ebcda}
div.stButton>button{border-radius:9px!important;min-height:44px!important;font-size:1.06rem!important;font-weight:700!important;transition:background .15s}
div.stButton>button[kind="primary"]{background:#255f99!important;border:1px solid #255f99!important;color:#fff!important}
div.stButton>button[kind="primary"]:hover{background:#174b7d!important}
div.stButton>button:not([kind="primary"]){background:#fff!important;border:1px solid #a7bbcf!important;color:#215683!important}
div.stButton>button:focus-visible{outline:3px solid #f3ab50!important;outline-offset:2px}
[data-testid="stProgressBar"]>div>div{background:#2870a8!important}
.correct,.wrong{border-radius:10px;padding:1rem 1.2rem;font-size:1.08rem;line-height:1.6}
.correct{border:1px solid #b8ddc9;border-left:5px solid #168252;background:#eef8f2;color:#174d37}
.wrong{border:1px solid #e9cbc2;border-left:5px solid #b65133;background:#fff4ef;color:#793b29}
.brief{background:#f2f7fc;border:1px solid #cddfeb;padding:1.1rem 1.3rem;border-radius:10px;color:#27445f}
.hint{background:#fff8ed;border-left:4px solid #b9722b;padding:.85rem 1.1rem;color:#66441f}
.footer{color:#62728a;font-size:.91rem;text-align:center;padding:2rem 0}
hr{border-color:#e0e7ef!important}
[data-testid="stAlert"]{border-radius:10px}
@media(max-width:720px){.block-container{padding:1rem}.hero{padding:1.25rem}.stat{min-height:84px}.smallcap{font-size:.49rem}}
</style>'''
st.markdown(CSS,unsafe_allow_html=True)

from banco_v3 import STAGES

def initialize():
    if 'game' not in st.session_state:
        st.session_state.game=dict(started=False, alias='', stage=0, index=0, xp=0, hp=100, streak=0, best_streak=0, correct=0, wrong=0, resolved=False, last=None, history=[], explanation_checks={})

def question():
    g=st.session_state.game
    return STAGES[g['stage']]['questions'][g['index']]

def score(correct, answer, explanation=''):
    g=st.session_state.game
    if correct:
        g['xp']+=100+min(g['streak'],4)*20
        g['hp']=min(100,g['hp']+8)
        g['streak']+=1
        g['best_streak']=max(g['streak'],g['best_streak'])
        g['correct']+=1
    else:
        g['hp']=max(0,g['hp']-16)
        g['streak']=0
        g['wrong']+=1
    g['history'].append(dict(setor=g['stage']+1,questao=g['index']+1,tipo=question()['t'],correto=correct,resposta=str(answer),nota=explanation))
    g['resolved']=True
    g['last']=correct

def advance():
    g=st.session_state.game
    if g['index']+1<len(STAGES[g['stage']]['questions']):g['index']+=1
    elif g['stage']+1<len(STAGES):g['stage']+=1;g['index']=0
    else:g['finished']=True
    g['resolved']=False;g['last']=None

def numberfmt(v):return f'{v:,}'.replace(',','.')

def header():
    st.markdown('''<div class="hero"><div class="smallcap">◈ PROTOCOLO ACADÊMICO // SIMULAÇÃO DE COMBATE</div>
    <div class="hero-title">NEON COMPLEXITY</div>
    <div class="hero-sub">OPERAÇÃO BIG-O · Sobreviva aos bugs. Domine a análise. Vença pela lógica.</div></div>''',unsafe_allow_html=True)

def progress():
    g=st.session_state.game
    total=sum(len(x['questions']) for x in STAGES)
    done=len(g['history'])
    a,b,c,d=st.columns(4)
    for col,label,value in [(a,'⚡ XP',numberfmt(g['xp'])),(b,'♥ ENERGIA',f"{g['hp']}%"),(c,'🎯 ACERTOS',f"{g['correct']}/{done}"),(d,'🔥 COMBO',str(g['streak']))]:
        col.markdown(f'<div class="stat"><div class="value">{value}</div><div class="label">{label}</div></div>',unsafe_allow_html=True)
    st.progress(done/total,text=f'Missões concluídas: {done}/{total}')

def sidebar():
    g=st.session_state.game
    with st.sidebar:
        st.markdown('<div class="smallcap">◈ PAINEL DE MISSÃO</div>',unsafe_allow_html=True)
        st.markdown('### 🕹️ NEON COMPLEXITY')
        st.caption('Treino de revisão · Estrutura de Dados e Análise de Algoritmos')
        st.divider()
        if g['started']:
            st.write('**Agente:**',g['alias'])
            for i,s in enumerate(STAGES):
                symbol='✅' if i<g['stage'] or g.get('finished') else '🔴' if i==g['stage'] else '🔒'
                st.markdown(f'{symbol} **{s["name"]}**  \\  {s["title"]}')
            st.divider()
            if st.button('🔁 Reiniciar campanha',use_container_width=True):
                del st.session_state.game
                st.rerun()
        st.caption('40 questões, incluindo 5 desafios integradores. Exercícios novos, preparados a partir dos conteúdos de aula e das competências exigidas na A1. Não reproduz o exame.')
        st.caption('Todos os resultados ficam na sessão; baixe seu relatório antes de fechar a aba.')

def intro():
    st.markdown('## 🚀 INICIAR CAMPANHA')
    st.markdown('''<div class="brief"><b>BRIEFING DA MISSÃO</b><br>
    Quatro setores temáticos. Quarenta questões de múltipla escolha para revisar conceitos essenciais. Cada resposta correta gera XP e recupera energia; cada erro custa energia e ativa uma explicação. A campanha continua mesmo se sua energia zerar: aprender faz parte da missão.<br><br>
    <b>Armas:</b> interpretação de código, Big-O, busca, vetores, laços e análise técnica.<br>
    <b>Objetivo:</b> compreender por que a solução funciona e como seu custo cresce — não memorizar o gabarito de uma prova.</div>''',unsafe_allow_html=True)
    alias=st.text_input('Codinome do agente',value='CADETE_01',max_chars=24)
    c1,c2=st.columns([1,2])
    with c1:
        if st.button('▶ ENTRAR NA ARENA',type='primary',use_container_width=True,disabled=not alias.strip()):
            g=st.session_state.game;g['started']=True;g['alias']=alias.strip();st.rerun()
    with c2:st.caption('Tempo estimado: 40–60 min · Acesso individual · Sem cadastro · Pode repetir')
    st.markdown('### Sua rota de treinamento')
    cols=st.columns(4)
    for col,s in zip(cols,STAGES):
        col.markdown(f'<div class="mission"><div class="smallcap">{s["name"]}</div><div class="mission-title">{s["accent"]} {s["title"]}</div><div class="lore">{s["theme"]}</div></div>',unsafe_allow_html=True)

def campaign():
    g=st.session_state.game
    if g.get('finished'):end_screen();return
    s=STAGES[g['stage']]; q=question(); i=g['index']
    st.markdown(f'<div class="mission"><div class="smallcap">{s["name"]} · DESAFIO {i+1} DE {len(s["questions"])} · INIMIGO: {s["boss"]}</div><div class="mission-title">{s["accent"]} {s["title"]}</div><div class="lore">{s["intro"]}</div></div>',unsafe_allow_html=True)
    progress()
    st.markdown(f'### 🎯 {"CHEFE FINAL" if q.get("boss") else "ALVO"} {i+1:02d}: {q["q"]}')
    if q.get('code'):
        st.code(q['code'],language='java')
    key=f'a_{g["stage"]}_{i}'
    if not g['resolved']:
        a=st.radio('Selecione uma alternativa:',q['options'],index=None,key=key)
        if st.button('⚡ CONFIRMAR RESPOSTA',type='primary',disabled=a is None,use_container_width=True):
            score(a==q['answer'],a)
            st.rerun()
    else:
        cl='correct' if g['last'] else 'wrong'
        title='ACERTO CRÍTICO! + XP' if g['last'] else 'ESCUDO DANIFICADO · REVISÃO ATIVADA'
        st.markdown(f'<div class="{cl}"><b>{title}</b></div>',unsafe_allow_html=True)
        st.markdown('**Resposta correta:** ' + q['answer'])
        st.info('**Raciocínio esperado:** ' + q['explanation'])
        st.markdown(f'**🧠 Conceito-chave:** {q["concept"]}')
        if g['index']==len(s['questions'])-1:st.success(f'CHEFE DE SETOR ENFRENTADO: {s["boss"]}. Prepare-se para o próximo setor.')
        if st.button('➡️ PRÓXIMA MISSÃO' if not(g['stage']==len(STAGES)-1 and g['index']==len(s['questions'])-1) else '🏁 FINALIZAR CAMPANHA',type='primary',use_container_width=True):advance();st.rerun()


def end_screen():
    g=st.session_state.game
    total=sum(len(s['questions']) for s in STAGES)
    pct=round(100*g['correct']/total)
    rank='LENDÁRIO' if pct>=90 else 'ELITE' if pct>=75 else 'SOBREVIVENTE' if pct>=55 else 'RECRUTA EM TREINAMENTO'
    st.markdown(f'<div class="hero"><div class="smallcap">TRANSMISSÃO FINAL · MISSÃO CONCLUÍDA</div><div class="hero-title">{rank}</div><div class="hero-sub">Agente {g["alias"]}: o sistema foi recuperado. Continue treinando o raciocínio!</div></div>',unsafe_allow_html=True)
    progress()
    st.markdown('## 📊 RELATÓRIO DE COMBATE')
    for n,s in enumerate(STAGES):
        arr=[h for h in g['history'] if h['setor']==n+1]
        ok=sum(h['correto'] for h in arr)
        st.write(f'**{s["name"]} — {s["theme"]}:** {ok}/{len(arr)} objetivos')
        st.progress(ok/len(arr))
    st.markdown('### Próximos passos')
    st.write('Releia os conceitos dos setores com menor desempenho. Para se preparar para a avaliação escrita, pratique justificar com suas palavras por que cada alternativa correta faz sentido.')
    report=dict(aplicacao='NEON COMPLEXITY — Operação Big-O',agente=g['alias'],gerado_em=datetime.now().isoformat(timespec='seconds'),resumo=dict(xp=g['xp'],acertos=g['correct'],erros=g['wrong'],total=total,percentual=pct,melhor_combo=g['best_streak'],modalidade="multipla_escolha"),historico=g['history'])
    st.download_button('⬇️ BAIXAR RELATÓRIO JSON',json.dumps(report,ensure_ascii=False,indent=2),file_name='neon_complexity_resultado.json',mime='application/json',use_container_width=True)
    if st.button('🔁 JOGAR NOVAMENTE',type='primary',use_container_width=True):del st.session_state.game;st.rerun()

initialize();header();sidebar()
if not st.session_state.game['started']:intro()
else:campaign()
st.markdown('<div class="footer">NEON COMPLEXITY © 2026 · Revisão independente de conteúdos acadêmicos · Inspirado em jogos de ação retrô, sem uso de nomes ou personagens licenciados.</div>',unsafe_allow_html=True)
