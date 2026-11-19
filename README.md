# Citizen Assist AI – Conta de Luz em Dia

Assistente de terminal, feito em Python, que orienta famílias de baixa renda sobre a **conta de luz em atraso** e a **Tarifa Social de Energia Elétrica**. As respostas vêm de uma base de conhecimento verificada, sempre com a fonte oficial e a data de verificação.

> **Aviso:** este assistente NÃO é um canal oficial. Ele não substitui a distribuidora de energia, o CRAS nem a ANEEL.

Global Solution 2026.2 · FIAP · 1º ano de Ciência da Computação · Pensamento Computacional e Automação com Python

---

## Integrantes

|          Nome            |     RM    |
|--------------------------|-----------|
| Matheus Borges Soares    | RM 574085 |
| Eric Hernandes Penhalbel | RM 570237 |
| Enzo Ricardo Silva       | RM 571333 |

## Público e problema

**Público:** famílias de baixa renda, inscritas ou não no CadÚnico, que estão com a conta de luz atrasada ou com medo de ter a energia cortada.

**Problema:** muitas famílias que têm direito à Tarifa Social não recebem o desconto. Os motivos mais comuns são a conta estar no nome de outra pessoa e o CadÚnico estar desatualizado. Além disso, quem está com a conta atrasada muitas vezes não conhece os próprios direitos: o aviso de 15 dias antes do corte, os dias em que o corte é proibido, o parcelamento obrigatório para baixa renda e o prazo de religação. Essas informações existem, mas estão espalhadas em resoluções da ANEEL e em sites diferentes, numa linguagem difícil. O assistente reúne tudo isso em respostas curtas, cada uma com a fonte.

## ODS relacionados

- **ODS 1 – Erradicação da pobreza:** acesso a um benefício social que reduz o custo de um serviço essencial.
- **ODS 7 – Energia limpa e acessível:** energia a preço acessível para famílias de baixa renda.
- **ODS 10 – Redução das desigualdades:** informação clara sobre direitos para quem mais precisa deles.

## Como executar

Requisito: Python 3.10 ou mais recente. Não usa bibliotecas externas.

```bash
git clone https://github.com/Matheusbg1903/citizen-assist-ai.git
cd citizen-assist-ai
python main.py
```

Menu principal:

1. **Fazer uma pergunta:** você digita a dúvida em texto livre e o assistente busca a melhor orientação, na base principal e nas orientações de energia.
2. **Navegar por categorias:** lista numerada de categorias e orientações, com "0 para voltar" em todas as telas.
3. **Ver indicadores:** mostra os indicadores calculados a partir do histórico de atendimentos.
4. **Exportar atendimentos (CSV):** gera o arquivo `data/atendimentos.csv`.
5. **Orientações de energia:** as 3 orientações calculadas no estudo de Energias Renováveis e uma calculadora da economia do banho (ver Integrações).
6. **Ver a fila do mutirão:** mostra quantas pessoas esperam no Posto Cidadão e a espera estimada, se o servidor da fila virtual estiver ligado (ver Integrações).
0. **Sair:** pede uma nota de facilidade de 1 a 5 e exporta o CSV.

## Estrutura do projeto

```
citizen-assist-ai/
├── README.md
├── main.py                  # ponto de entrada: carrega a base e inicia o assistente
├── orientacao.py            # classe Orientacao: um registro da base e exibir()
├── base_conhecimento.py     # classe BaseConhecimento: carregar, categorias, pontuar, buscar
├── assistente.py            # classe Assistente: atendimento, histórico, indicadores, CSV
├── energia.py               # integração com Energias Renováveis (menu de energia e calculadora)
├── fila_mutirao.py          # integração com Computer Organization (lê a fila virtual pela rede)
├── teste_base.py            # teste da pontuação e da busca
├── teste_energia.py         # confere os números de energia e a melhoria do teste com usuários
├── roteiro_teste_usuarios.md # roteiro e folha de anotação do teste com usuários
└── data/
    ├── base_conhecimento.json   # 14 orientações em 3 categorias
    ├── energia.json             # 3 orientações de energia (contribuição de Energias Renováveis)
    ├── historico.json           # atendimentos registrados
    └── atendimentos.csv         # exportação dos atendimentos
```

As classes se ligam por composição: o `Assistente` tem uma `BaseConhecimento`, e a `BaseConhecimento` tem uma lista de objetos `Orientacao`.

## Base de conhecimento

A base principal tem **14 orientações em 3 categorias**, e a busca livre também procura nas 3 orientações de energia de `data/energia.json` (categoria "Energia: gastar menos na conta"):

- **Tarifa Social e descontos (6):** quem tem direito, gratuidade até 80 kWh, Desconto Social, desconto que não veio na conta, CadÚnico, família com aparelho elétrico para tratamento de saúde.
- **Conta atrasada e corte (5):** quando a luz pode ser cortada, dias e horários em que o corte é proibido, parcelamento, multa e juros, e por que negociar antes dos 90 dias de atraso.
- **Religação e direitos (3):** religação depois de pagar, corte indevido, dívida do antigo morador.

Cada orientação tem de 5 a 9 palavras-chave, fonte oficial (ANEEL, MME, REN ANEEL 1.000/2021 ou Banco Central) e data de verificação.

**Decisão:** a base não traz valores em reais, como "R$ 810,50". Ela fala em "meio salário mínimo por pessoa", porque o salário mínimo muda todo ano e o valor em reais ficaria desatualizado. Também avisa que as faixas antigas de 65%, 40% e 10% deixaram de valer em 5/7/2025.

## Regra de pontuação

A pergunta, as palavras-chave e o título são normalizados antes da comparação: tudo em minúsculas, sem acentos e sem pontuação. Também colocamos espaços nas pontas do texto, para comparar só palavras inteiras.

|                                Regra                             | Pontos |
|------------------------------------------------------------------|--------|
| Palavra-chave da orientação que aparece na pergunta              |   +3   |
| Palavra da pergunta, com 4 letras ou mais, que aparece no título |   +1   |

| Pontuação da melhor orientação |                                Resultado                                    |
|--------------------------------|-----------------------------------------------------------------------------|
|           6 ou mais            | Confiança **ALTA**                                                          |
|            3 a 5               | Confiança **MÉDIA**                                                         |
|          Menos de 3            | "Não encontrei": o assistente sugere outras palavras e mostra as categorias |

`buscar()` devolve uma lista de tuplas `(pontos, orientacao)`, da maior para a menor pontuação. O assistente mostra a melhor orientação. Se ela não resolver a dúvida, mostra até duas alternativas com 3 pontos ou mais.

**Exemplo:** "Tenho direito à tarifa social?"
- +3 por `tarifa social`
- +3 por `tenho direito`
- +1 por "tarifa", +1 por "social" e +1 por "direito", que aparecem no título "Tarifa Social de Energia: quem tem direito"
- Total: **9 pontos, confiança ALTA**

## Proteção de dados e entradas inválidas

- O assistente nunca pede nome, CPF, telefone ou e-mail.
- Pergunta com 8 ou mais dígitos, ou com `@`, é recusada e não fica registrada.
- Opção fora da faixa, letras, resposta vazia ou s/n inválido mostram uma mensagem e pedem a entrada de novo. O programa nunca é encerrado por isso.
- Se o JSON estiver ausente ou corrompido, o programa avisa e encerra sem travar.

## Integrações com outras disciplinas

As integrações entram no menu por `assistente.adicionar_opcao(rotulo, funcao)`, no `main.py`. A busca por pontuação continua sendo o centro do assistente; as integrações são opções a mais.

| Disciplina | O que entra no assistente | Onde está |
|---|---|---|
| **Soluções em Energias Renováveis** | Opção 5 do menu e busca livre: 3 orientações calculadas no estudo GS-SERS (Tarifa Social, chuveiro e energia solar) e uma calculadora da economia do banho. As orientações ficam em `data/energia.json`, no mesmo formato da base, e são carregadas por uma segunda `BaseConhecimento` (reuso da classe por composição). Cada consulta entra no histórico com origem `energia`, então conta nos indicadores e no CSV. | `energia.py`, `data/energia.json`, `teste_energia.py` |
| **Computer Organization** | Opção 6 do menu: lê pela rede (HTTP, `urllib` da biblioteca padrão) o estado da fila virtual do mutirão do Posto Cidadão e mostra pessoas na fila, espera estimada e senhas restantes. Se o servidor estiver desligado, o assistente avisa e continua. | `fila_mutirao.py` e o repositório da fila virtual |
| **Modelagem Linear** | A orientação CO05 ("Atrasou a conta: negocie antes dos 90 dias") usa a conclusão do relatório do grupo com dados do SCR do Banco Central: onde há mais atraso de 15 a 90 dias há mais inadimplência, então essa é a janela para negociar. Combina com a regra da ANEEL de corte em até 90 dias. | `data/base_conhecimento.json` (CO05) |
| **Computer Science** | Prevista: a triagem `S = A(B + C) + D` como opção do menu. A lógica e os testes são escritos pelo grupo, por causa da regra de IA da disciplina; o ponto de ligação já está comentado no `main.py`. | `main.py` |

Como a de energia usa as mesmas classes, o mesmo teste com usuários serve para PCP e para Energias: basta pedir a cada pessoa uma pergunta de energia além das perguntas de conta de luz.

## Fontes consultadas

As fontes da base principal foram verificadas em 12/11/2026, exceto as indicadas com outra data.

- ANEEL – Tarifa Social: https://www.gov.br/aneel/pt-br/assuntos/tarifas/tarifa-social
- ANEEL – Como resolver: principais dúvidas: https://www.gov.br/aneel/pt-br/consumidores/como-resolver
- ANEEL – Resolução Normativa nº 1.000/2021 (arts. 343, 344, 346, 357, 359, 361 e 441): https://www2.aneel.gov.br/cedoc/ren20211000.html
- Banco Central – SCR.data (orientação CO05, verificado em 13/11/2026): https://www.bcb.gov.br/estabilidadefinanceira/scrdata
- Orientações de energia (verificadas em 13/11/2026): estudo GS-SERS do grupo, com tarifas da ANEEL (https://dadosabertos.aneel.gov.br/), irradiação do INPE/LABREN (https://labren.ccst.inpe.br/atlas_2017.html) e fator de emissão do MCTI (https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene)
- ANEEL – Conheça a Resolução 1.000: https://www.gov.br/aneel/pt-br/assuntos/noticias/2022/conheca-a-resolucao-1-000-que-reune-os-direitos-e-deveres-do-consumidor-de-energia-eletrica
- ANEEL – Cadastro automático na Tarifa Social: https://www.gov.br/aneel/pt-br/assuntos/noticias/2022/governo-federal-aprova-novo-modo-de-cadastro-na-tarifa-social
- MME – Programa Luz do Povo (Tarifa Social e Desconto Social): https://www.gov.br/mme/pt-br/luzdopovo
- MME – Tarifa social: saiba como funciona: https://www.gov.br/mme/pt-br/assuntos/noticias/tarifa-social-saiba-como-funciona-e-quem-pode-pedir-desconto
- Lei nº 15.235/2025 (gratuidade até 80 kWh e Desconto Social) e Lei nº 14.015/2020 (proibição de corte em sexta-feira, fim de semana e feriado)

## Resultado do teste com usuários

O teste foi feito em 16/11/2026 com **3 pessoas de fora da equipe** (P1, P2 e P3), cada uma numa sessão própria do assistente. Não registramos nomes nem dados dessas pessoas. O roteiro, com as tarefas e a folha de anotação, está em [`roteiro_teste_usuarios.md`](roteiro_teste_usuarios.md). A mesma rodada gerou as evidências da disciplina de Energias.

| Indicador | Resultado |
|---|---|
| Pessoas testadas | 3 |
| Atendimentos | 11 (6 por pergunta livre, 2 por categoria e 3 pelo menu de energia) |
| Resposta encontrada | 100,0% |
| Taxa de acerto (ajudou) | 90,9% |
| Tempo médio para encontrar | 21,4 s |
| Tentativas por atendimento | 1,1 |
| Facilidade de uso (1 a 5) | 4,0 (notas 3, 5 e 4) |
| Dúvidas sem solução | nenhuma pergunta livre ficou sem resposta |

**O que o teste mostrou:**
- **Uma resposta errada aceita.** O P3 perguntou "vale a pena colocar placa solar para quem está com a conta atrasada?" na pergunta livre. O assistente respondeu com a orientação de corte por conta atrasada (CO01, depois de 2 tentativas), porque a frase tinha "conta atrasada" e a orientação de energia solar só existia no menu 5.
- **Uma orientação que não ajudou.** O P2 abriu, pela navegação por categorias, a orientação sobre dívida do antigo morador (RE03) e respondeu que ela não resolveu a dúvida. Como veio da navegação, ela não aparece em "dúvidas sem solução", que só lista perguntas livres.
- **Limitação desta rodada.** Os participantes digitaram as perguntas a partir do enunciado das tarefas, e não com as próprias palavras. Por isso a taxa de resposta encontrada (100%) tende a ser maior do que seria com perguntas espontâneas.

**Melhoria feita a partir do teste:** a busca livre passou a procurar também nas 3 orientações de energia (`main.py`), e a orientação de energia solar (EN03) ganhou a palavra-chave "vale a pena". Agora a pergunta do P3 encontra a EN03 com 9 pontos, à frente da CO01 (8 pontos). O `teste_energia.py` confere essa pergunta e confere que "minha luz foi desligada" continua sem resposta, porque ela é a alteração ao vivo do vídeo.

## Limitações

- **A busca é por palavras, não por significado.** O assistente só encontra a resposta se a pergunta tiver uma palavra-chave ou uma palavra do título. Sinônimos não cadastrados, como "desligaram" em vez de "cortaram", não são reconhecidos.
- **O filtro de dado pessoal pode bloquear perguntas legítimas.** Uma pergunta como "consumo de 220 kWh em 10/2026" soma 9 dígitos e é recusada, mesmo sem ter dado pessoal.
- **As regras mudam.** A base reflete as regras vigentes em 12/11/2026. Mudanças na lei ou nas resoluções da ANEEL exigem atualizar o JSON.
- **O assistente não consulta a conta real.** Ele não calcula o valor de uma fatura nem informa se a família já recebe o desconto. Isso só a distribuidora pode fazer.
- **Não é canal oficial.** O assistente informa e encaminha, mas não resolve o problema no lugar da distribuidora ou do CRAS.

## Vídeo técnico

Link (YouTube, não listado):(https://youtu.be/kkZutfvEFqs)
