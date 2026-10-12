# NEON COMPLEXITY — Operação Big-O

App em Streamlit de revisão gamificada de Estrutura de Dados e Análise de Algoritmos, no estilo de ficção científica/FPS retrô **original**.

## Instalação

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

O Streamlit abrirá a aplicação no navegador (geralmente http://localhost:8501).

## Publicação em Streamlit Community Cloud

1. Envie `app.py` e `requirements.txt` para um repositório GitHub.
2. No Streamlit Community Cloud, clique em **Create app**, conecte o repositório e selecione `app.py`.
3. Compartilhe o endereço gerado com a turma.

## Sobre o conteúdo

Quatro setores com sete desafios cada (28 no total):
- Escalabilidade, correção vs. eficiência e Big-O;
- Busca sequencial, busca binária e pré-requisitos;
- Otimização de laços, custo das comparações e ordenação;
- Vetores, média, contagem, laços sequenciais e matrizes.

Há questões de alternativas, cálculos e justificativas escritas. Todas são **questões de treino inéditas**, alinhadas às competências da aula e da A1; não são reproduções da prova.

## Recursos

- Modo campanha, 4 chefes de setor, HUD com energia, XP, combo e pontuação;
- Feedback explicativo após cada resposta;
- Justificativas com autoavaliação por critérios (sem alegar correção automática);
- Exportação JSON individual para estudo pessoal;
- Nenhum banco de dados, login ou serviço externo é necessário;
- Sem trilhas sonoras, imagens ou personagens de franquias existentes.

### Importante

Os dados da partida ficam apenas na sessão atual do navegador e podem se perder ao recarregar/fechar; cada estudante pode baixar seu relatório ao finalizar. O relatório JSON não é um registro autenticado de desempenho, portanto não é indicado para nota oficial. O jogo não divulga o gabarito da A1: usa apenas as habilidades previstas na avaliação para compor desafios alternativos.
