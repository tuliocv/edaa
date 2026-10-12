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

# Tipos: mcq = múltipla escolha; numeric = previsão de custo; explain = justificativa com autoavaliação orientada.
STAGES = [
 dict(name='SETOR 01',title='O COLAPSO DA ESCALA',boss='Guardião do Crescimento',accent='⚡',theme='Escalabilidade, correção e Big-O', intro='Uma aplicação passou de centenas para milhões de registros. Sua missão é detectar rotinas que não escalam.',questions=[
  dict(t='mcq',q='Uma rotina acessa dados[0] em um vetor não vazio. Como seu custo cresce em relação ao número n de registros?',options=['O(n²)','O(1)','O(n)','O(log n)'],answer='O(1)',explanation='O acesso a uma posição conhecida do vetor é uma operação de custo constante, independentemente do tamanho do vetor.',concept='Acesso direto não requer percorrer todos os registros.'),
  dict(t='mcq',q='Um programa gera a resposta correta para 200 registros. O que esse teste NÃO demonstra?',options=['Que há pelo menos um teste bem-sucedido','Que o programa escala bem para milhões de registros','Que a execução retornou um resultado','Que a saída correspondeu ao caso testado'],answer='Que o programa escala bem para milhões de registros',explanation='Correção funcional para um caso não comprova eficiência nem escalabilidade com entradas grandes.',concept='Correção e eficiência são propriedades distintas.'),
  dict(t='mcq',q='Qual é o papel de n na análise de uma rotina que percorre todas as matrículas?',options=['Quantidade de instruções Java no arquivo','Número de registros na entrada','Memória RAM do computador','Quantidade de métodos da classe'],answer='Número de registros na entrada',explanation='n representa o tamanho da entrada relevante para o algoritmo: neste caso, o número de matrículas.',concept='Defina n antes de classificar T(n).'),
  dict(t='mcq',q='Qual complexidade representa um percurso simples pelos n estudantes, com trabalho constante por estudante?',options=['O(1)','O(n²)','O(n)','O(2ⁿ)'],answer='O(n)',explanation='Uma varredura com n iterações e custo constante por iteração exige trabalho proporcional a n.',concept='Uma passagem completa por n dados tem custo linear.'),
  dict(t='numeric',q='Uma rotina com dois laços completos aninhados executa n × n comparações. Para n = 1.200, quantas comparações são realizadas?',answer=1440000,explanation='1.200 × 1.200 = 1.440.000. Em geral, T(n)=n² e a classe é O(n²).',concept='Laços aninhados multiplicam as contagens de iterações.'),
  dict(t='mcq',q='Se n crescer de 1.000 para 10.000, a quantidade de operações de um algoritmo T(n)=n² cresce aproximadamente quanto?',options=['2 vezes','10 vezes','100 vezes','1.000 vezes'],answer='100 vezes',explanation='A entrada foi multiplicada por 10; o custo quadrático foi multiplicado por 10² = 100.',concept='Fator de escala no crescimento quadrático.'),
  dict(t='explain',q='Você recebe um sistema que funciona para 300 usuários, mas terá de atender 3 milhões. Escreva uma justificativa técnica explicando por que a equipe precisa analisar sua eficiência.',must=['correto','crescimento','entrada'],model='Uma rotina pode produzir a saída correta e ainda ter custo impraticável quando o tamanho da entrada cresce. É necessário identificar n, estimar o crescimento de T(n) e avaliar se o algoritmo atende ao volume futuro.',concept='A prova valoriza justificativas, não apenas o símbolo Big-O.'),
 ]),
 dict(name='SETOR 02',title='RADAR DE BUSCA',boss='Sentinela dos Índices',accent='🎯',theme='Busca sequencial e busca binária',intro='O banco de dados não para de crescer. Escolha a busca correta e identifique seus pré-requisitos.',questions=[
  dict(t='mcq',q='Um vetor de IDs está desordenado. Qual método funciona diretamente sem exigir ordenação prévia?',options=['Somente busca binária','Busca sequencial','A busca binária necessariamente','Nenhuma busca'],answer='Busca sequencial',explanation='A busca sequencial verifica posições uma a uma e não exige dados ordenados.',concept='A pré-condição da busca binária é uma coleção ordenada pelo critério buscado.'),
  dict(t='mcq',q='Em [71, 9, 24, 38, 12, 55], quantas comparações a busca sequencial faz até encontrar 38?',options=['2','3','4','6'],answer='4',explanation='A busca compara 71, 9, 24 e 38, parando na quarta comparação.',concept='Melhor caso: primeira posição. Pior caso: última posição ou ausência.'),
  dict(t='mcq',q='Qual é o comportamento típico de uma busca binária em um vetor ordenado?',options=['O(n²)','O(n)','O(log n)','O(1) sempre'],answer='O(log n)',explanation='A cada iteração, a busca binária elimina aproximadamente metade do espaço de busca.',concept='Metades sucessivas levam ao crescimento logarítmico.'),
  dict(t='mcq',q='Um vetor de alunos está ordenado por nota. Você deseja buscar por matrícula usando busca binária. O que falta?',options=['Nada: basta estar ordenado por qualquer campo','Ordenação pelo critério de matrícula ou índice próprio','Um laço adicional para duplicar os elementos','Converter o vetor em matriz'],answer='Ordenação pelo critério de matrícula ou índice próprio',explanation='A ordenação deve ser compatível com a chave pesquisada.',concept='Ordenação por nota não garante busca binária por matrícula.'),
  dict(t='numeric',q='Ao procurar um ID inexistente com busca sequencial em uma lista de 14 IDs, quantas comparações de igualdade são necessárias?',answer=14,explanation='Como nenhum elemento corresponde ao alvo, todos os 14 são comparados.',concept='Ausência de um elemento produz o pior caso da busca sequencial tradicional.'),
  dict(t='mcq',q='Qual situação pode fazer uma busca sequencial ser preferível a ordenar dados para aplicar uma busca binária?',options=['Muitas consultas recorrentes em dados estáticos e já ordenados','Apenas uma consulta em conjunto pequeno e desordenado','Dados sempre ordenados pela chave','Um índice binário já pronto'],answer='Apenas uma consulta em conjunto pequeno e desordenado',explanation='O custo de ordenar previamente pode não compensar uma única busca.',concept='Compare custo inicial, frequência das buscas e manutenção dos dados.'),
  dict(t='explain',q='Explique por que trocar uma busca sequencial por binária não garante automaticamente a melhor solução em qualquer sistema.',must=['orden','custo','busca'],model='A busca binária é O(log n) no vetor ordenado, mas pressupõe dados organizados pelo campo de busca. Ordenar e manter a coleção ordenada tem custo; com poucas consultas, o investimento pode não compensar.',concept='Analise o custo do sistema completo, não apenas de uma operação isolada.'),
 ]),
 dict(name='SETOR 03',title='A ARENA DO CODE REVIEW',boss='Duplicador de Pares',accent='🛠️',theme='Laços, otimização e limites assintóticos',intro='O motor de recomendações compara pares em excesso. Elimine trabalho redundante sem perder a análise de complexidade.',questions=[
  dict(t='mcq',q='Um código compara cada usuário com ele mesmo. Qual mudança elimina a diagonal de comparações?',options=['Começar j em i + 1','Começar j em 0 sempre','Trocar n por n²','Remover o laço externo'],answer='Começar j em i + 1',explanation='Iniciando em i+1, o par (i,i) é ignorado e cada par não ordenado é processado uma vez.',concept='Pares sem repetição podem ser enumerados acima da diagonal.'),
  dict(t='numeric',q='Para 9 pessoas, quantos pares distintos (sem auto-comparação e sem ordem) existem?',answer=36,explanation='n(n−1)/2 = 9×8/2 = 36.',concept='Quantidade de pares distintos: n(n−1)/2.'),
  dict(t='mcq',q='Uma otimização reduz comparações de n² para n(n−1)/2. O que acontece com a classe assintótica?',options=['Passa para O(n)','Passa para O(log n)','Permanece O(n²)','Passa para O(1)'],answer='Permanece O(n²)',explanation='O termo dominante continua proporcional a n²; houve economia de operações, não mudança da ordem de crescimento.',concept='Constantes multiplicativas não mudam Big-O.'),
  dict(t='mcq',q='Dois laços de n iterações são executados UM APÓS O OUTRO. Qual é o custo total?',options=['O(n²)','O(2ⁿ)','O(n)','O(log n)'],answer='O(n)',explanation='Somamos n+n=2n. Como o fator 2 é constante, O(2n)=O(n).',concept='Laços sequenciais somam; laços aninhados multiplicam.'),
  dict(t='mcq',q='Um algoritmo compara elementos adjacentes e interrompe ao concluir uma passagem sem trocas. Qual melhoria foi aplicada?',options=['Busca binária','Parada antecipada do Bubble Sort','Recursão do Merge Sort','Remoção completa das comparações'],answer='Parada antecipada do Bubble Sort',explanation='Sem trocas em uma passagem, o vetor já está ordenado. O melhor caso do Bubble otimizado é linear.',concept='A otimização pode melhorar o melhor caso sem alterar o pior caso quadrático.'),
  dict(t='mcq',q='Para reduzir movimentações em um vetor pequeno quase ordenado, qual algoritmo costuma ser boa escolha?',options=['Insertion Sort','Selection Sort sempre','Bubble original sempre','Busca sequencial'],answer='Insertion Sort',explanation='Insertion Sort desloca elementos para inserir a chave e aproveita a ordenação parcial.',concept='Algoritmos com o mesmo Big-O podem ter custos práticos distintos.'),
  dict(t='explain',q='Um colega diz: “Cortamos quase metade das comparações, então O(n²) virou O(n)”. Escreva uma resposta técnica.',must=['quadr','opera','constant'],model='A melhoria reduz a quantidade de operações por um fator aproximadamente constante, mas a quantidade ainda cresce quadraticamente. O termo dominante de n(n−1)/2 continua sendo n²; por isso, a classe permanece O(n²).',concept='Separe redução do custo real de redução da ordem de crescimento.'),
 ]),
 dict(name='SETOR 04',title='O NÚCLEO DOS VETORES',boss='Arquiteto da Memória',accent='🧬',theme='Arrays, cálculos e boas escolhas de estrutura',intro='Sua última missão é montar uma solução legível, escalável e justificável para processar dados acadêmicos.',questions=[
  dict(t='mcq',q='Por que double[] notas é melhor que declarar manualmente uma variável para cada uma das 400 notas?',options=['Porque um vetor sempre torna qualquer algoritmo O(1)','Porque organiza dados homogêneos e simplifica percurso e manutenção','Porque impede qualquer erro de programação','Porque elimina a necessidade de memória'],answer='Porque organiza dados homogêneos e simplifica percurso e manutenção',explanation='Vetores agrupam elementos de mesmo tipo e permitem operar sobre eles com índices e laços.',concept='Estrutura de dados adequada simplifica manutenção, acesso e processamento.'),
  dict(t='mcq',q='Qual é a complexidade para somar todas as notas de um vetor com n elementos?',options=['O(n)','O(1)','O(n²)','O(log n)'],answer='O(n)',explanation='É necessário visitar cada elemento uma vez, com custo constante por visita.',concept='Soma de n elementos requer uma varredura linear.'),
  dict(t='mcq',q='Para contar notas abaixo da média calculada previamente, qual é o custo de um segundo percurso completo?',options=['O(1)','O(n²)','O(n)','O(n³)'],answer='O(n)',explanation='A segunda passagem avalia cada uma das n notas uma vez.',concept='Contagem sob condição em uma passagem é linear.'),
  dict(t='numeric',q='Uma turma tem 280 notas. Um laço visita todas para somar e outro visita todas para contar notas abaixo da média. Quantas visitas aos elementos são feitas no total?',answer=560,explanation='São 280 visitas na primeira passagem e 280 na segunda: 560 = 2n, mantendo custo O(n).',concept='Somar duas passagens lineares gera 2n, não n².'),
  dict(t='mcq',q='Qual é a complexidade de percorrer todas as células de uma matriz com r linhas e c colunas?',options=['O(r+c)','O(r×c)','O(1)','O(log r)'],answer='O(r×c)',explanation='O total de células da matriz é r multiplicado por c.',concept='Dois laços aninhados sobre dimensões diferentes multiplicam seus tamanhos.'),
  dict(t='mcq',q='Entre os algoritmos abaixo, qual tem pior caso O(n log n) na implementação tradicional?',options=['Selection Sort','Bubble Sort','Merge Sort','Insertion Sort'],answer='Merge Sort',explanation='Merge Sort divide recursivamente o vetor e intercala cada nível em custo linear.',concept='Dividir e conquistar pode reduzir a classe de crescimento.'),
  dict(t='explain',q='Justifique por que uma solução que usa vetor e dois laços sequenciais para calcular a média e contar valores abaixo dela possui custo linear.',must=['vetor','sequenc','2n'],model='O vetor organiza todas as notas em uma estrutura indexada. O primeiro laço percorre n posições e o segundo percorre mais n posições, mas são sequenciais. Assim, T(n)=n+n=2n e sua complexidade é O(n).',concept='Distinguir laços consecutivos de laços aninhados é essencial.'),
 ]),
]


# Todos os itens seguem o mesmo formato acessível de múltipla escolha.
# Respostas certas e feedbacks são preservados, inclusive nos antigos itens abertos.
CONVERSIONS = {
 (0,4): ('1.440.000', ['144.000','1.440.000','2.400','14.400.000']),
 (0,6): ('Porque a correção em entradas pequenas não garante eficiência quando n cresce.', ['Porque o número de linhas do código aumenta automaticamente.', 'Porque a correção em entradas pequenas não garante eficiência quando n cresce.', 'Porque todo algoritmo se torna O(1) com mais memória.', 'Porque um programa correto não precisa de testes de desempenho.']),
 (1,4): ('14', ['1','7','13','14']),
 (1,6): ('A ordenação prévia e sua manutenção podem custar mais do que o benefício para poucas consultas.', ['Busca binária funciona da mesma forma em qualquer vetor.', 'A ordenação prévia e sua manutenção podem custar mais do que o benefício para poucas consultas.', 'Busca binária é sempre quadrática.', 'Busca sequencial precisa que os dados estejam ordenados.']),
 (2,1): ('36', ['9','18','36','72']),
 (2,6): ('Não. Reduzir comparações por um fator constante mantém o crescimento O(n²).', ['Sim. Qualquer economia de comparações muda a classe para O(n).', 'Não. Reduzir comparações por um fator constante mantém o crescimento O(n²).', 'Sim. O resultado passa a ser O(log n).', 'Não. O algoritmo original era O(1).']),
 (3,3): ('560', ['280','560','78.400','840']),
 (3,6): ('Os laços são sequenciais: n + n = 2n, que permanece O(n).', ['Os laços são sequenciais: n + n = 2n, que permanece O(n).', 'Dois laços sempre levam a n², mesmo sem aninhamento.', 'Um vetor torna todos os laços O(1).', 'A complexidade é O(log n) porque a média divide a soma por n.']),
}
for (setor, idx), (answer, options) in CONVERSIONS.items():
    item = STAGES[setor]['questions'][idx]
    item['t'] = 'mcq'
    item['answer'] = answer
    item['options'] = options
    item.pop('must', None)
    if 'model' in item:
        item['explanation'] = item.pop('model')
    item['q'] = (item['q']
        .replace('Escreva uma justificativa técnica explicando por que a equipe precisa analisar sua eficiência.', 'Qual justificativa técnica explica a necessidade de analisar a eficiência?')
        .replace('Explique por que trocar uma busca sequencial por binária não garante automaticamente a melhor solução em qualquer sistema.', 'Por que trocar busca sequencial por binária não garante automaticamente a melhor solução?')
        .replace('Escreva uma resposta técnica.', 'Qual resposta técnica está correta?')
        .replace('Justifique por que uma solução que usa vetor e dois laços sequenciais para calcular a média e contar valores abaixo dela possui custo linear.', 'Por que utilizar um vetor com dois laços sequenciais para calcular média e contar valores abaixo dela tem custo linear?')
        .replace('quantas comparações são realizadas?', 'qual é o número correto de comparações?')
        .replace('quantas comparações de igualdade são necessárias?', 'quantas comparações de igualdade são necessárias?')
        .replace('quantos pares distintos (sem auto-comparação e sem ordem) existem?', 'quantos pares distintos (sem auto-comparação e sem ordem) existem?')
        .replace('Quantas visitas aos elementos são feitas no total?', 'Quantas visitas aos elementos são feitas no total?'))
    if isinstance(item['answer'], str) and item['answer'] not in item['options']:
        raise ValueError('Alternativa correta não encontrada')
assert sum(len(s['questions']) for s in STAGES) == 28
assert all(q['t']=='mcq' and q['answer'] in q['options'] for s in STAGES for q in s['questions'])


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
        st.caption('Exercícios novos, preparados a partir dos conteúdos de aula e das competências exigidas na A1. Não reproduz o exame.')
        st.caption('Todos os resultados ficam na sessão; baixe seu relatório antes de fechar a aba.')

def intro():
    st.markdown('## 🚀 INICIAR CAMPANHA')
    st.markdown('''<div class="brief"><b>BRIEFING DA MISSÃO</b><br>
    Quatro setores temáticos. Vinte e oito questões de múltipla escolha para revisar conceitos essenciais. Cada resposta correta gera XP e recupera energia; cada erro custa energia e ativa uma explicação. A campanha continua mesmo se sua energia zerar: aprender faz parte da missão.<br><br>
    <b>Armas:</b> interpretação de código, Big-O, busca, vetores, laços e análise técnica.<br>
    <b>Objetivo:</b> compreender por que a solução funciona e como seu custo cresce — não memorizar o gabarito de uma prova.</div>''',unsafe_allow_html=True)
    alias=st.text_input('Codinome do agente',value='CADETE_01',max_chars=24)
    c1,c2=st.columns([1,2])
    with c1:
        if st.button('▶ ENTRAR NA ARENA',type='primary',use_container_width=True,disabled=not alias.strip()):
            g=st.session_state.game;g['started']=True;g['alias']=alias.strip();st.rerun()
    with c2:st.caption('Tempo estimado: 25–40 min · Acesso individual · Sem cadastro · Pode repetir')
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
    st.markdown(f'### 🎯 ALVO {i+1:02d}: {q["q"]}')
    key=f'a_{g["stage"]}_{i}'
    if not g['resolved']:
        a=st.radio('Selecione uma alternativa:',q['options'],index=None,key=key)
        if st.button('⚡ CONFIRMAR RESPOSTA',type='primary',disabled=a is None,use_container_width=True):
            score(a==q['answer'],a)
            st.rerun()
    else:
        cl='correct' if g['last'] else 'wrong'
        title='ACERTO CRÍTICO! + XP' if g['last'] else 'ESCUDO DANIFICADO · REVISÃO ATIVADA'
        st.markdown(f'<div class="{cl}"><b>{title}</b><br>{q.get("explanation",q.get("model",""))}</div>',unsafe_allow_html=True)
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
