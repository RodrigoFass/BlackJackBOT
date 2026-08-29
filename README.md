# BlackJackBOT

Assistente de contagem de cartas para Blackjack, em Python puro. Você informa as cartas conforme elas
aparecem na mesa; o programa mantém a contagem, calcula a contagem verdadeira e recomenda a jogada.

---

## Sobre

Não é um jogo: é um acompanhante de mesa. O programa não sorteia cartas nem simula partidas — ele lê o
que você digita, atualiza a contagem e responde o que fazer com a mão atual contra a carta visível do
dealer.

O fluxo de uma rodada:

1. Informe as cartas da sua mão e a carta visível do dealer
2. O programa mostra a contagem corrente, a contagem verdadeira e a jogada recomendada
3. Informe cada carta comprada, as cartas dos outros jogadores e as cartas seguintes do dealer
4. Ao fim da rodada, ele mostra a contagem atualizada e o resultado das mãos

Tudo que entra na mesa entra na contagem, e é por isso que as cartas dos outros jogadores também são
pedidas.

## Por que Wong Halves, e não Hi-Lo

Hi-Lo é o sistema recomendado para pessoas: valores inteiros de +1, 0 e −1, simples o bastante para
manter de cabeça durante horas. Wong Halves é mais preciso, mas usa valores fracionários em três
níveis e cansa rápido.

Esse argumento não vale aqui, porque quem faz a conta é o programa. Somar 0,5 custa o mesmo que somar 1.
Sem o custo mental, sobra a precisão:

| | Hi-Lo | Wong Halves |
|---|---|---|
| Correlação de aposta | ~0,97 | ~0,99 |
| Eficiência de jogo | ~0,51 | ~0,57 |
| Dificuldade para uma pessoa | baixa | alta |
| Dificuldade para um programa | nenhuma | nenhuma |

A diferença prática é pequena — centésimos de ponto percentual de vantagem — mas é de graça quando a
aritmética é automática.

### Os valores

| Carta | Valor |
|---|:---:|
| 2 | +0,5 |
| 3, 4, 6 | +1 |
| 5 | +1,5 |
| 7 | +0,5 |
| 8 | 0 |
| 9 | −0,5 |
| 10, J, Q, K, A | −1 |

O 5 pesa mais que as outras cartas baixas porque é a que mais atrapalha o dealer, e o 7 pesa menos que
o 6 porque é uma carta de transição. É essa granularidade que o Hi-Lo abre mão em nome da simplicidade.

### Contagem verdadeira

```
contagem verdadeira = contagem corrente / baralhos restantes
baralhos restantes  = baralhos totais − (cartas jogadas / 52)
```

A contagem corrente sozinha não diz nada: +6 com oito baralhos por jogar é quase nada, e +6 com um
baralho restante é uma vantagem real. O divisor tem piso de 1 para não explodir no fim do sapato.

## Estratégia implementada

Mãos duras, com desvios pela contagem verdadeira:

| Mão | Decisão |
|---|---|
| 17 ou mais | Parar |
| 16 | Parar contra 2–6; parar contra 10 se a contagem verdadeira ≥ 2; senão comprar |
| 15 | Parar contra 2–6; parar contra 10 se a contagem verdadeira ≥ 2; senão comprar |
| 14 | Parar contra 2–6; senão comprar |
| 13 | Parar contra 4–6; senão comprar |
| 12 | Parar contra 4–6; senão comprar |
| 11 | Dobrar se a contagem verdadeira ≥ 1; senão comprar |
| 10 | Dobrar se a contagem verdadeira ≥ 2; senão comprar |
| 9 | Dobrar contra 3–6 se a contagem verdadeira ≥ 1; senão comprar |
| 8 ou menos | Comprar |

Os desvios em 16 contra 10 e nos dobros de 9, 10 e 11 são o motivo de contar cartas: a estratégia
básica sozinha não muda de decisão conforme o sapato esquenta.

O valor da mão trata múltiplos Ases corretamente, escolhendo 1 ou 11 conforme couber em 21.

## Como usar

Requer apenas Python 3. Não há dependências externas — nenhum `pip install`.

```bash
python BlackJack.py
```

O programa pergunta quantos baralhos estão em uso e segue para as rodadas. Digite `SAIR` no lugar da
mão para encerrar.

Entradas aceitas: `2` a `10`, `J`, `Q`, `K`, `A`, separadas por espaço quando for mais de uma.

## Estrutura

```
BlackJackBOT/
├── BlackJack.py   # classe BlackjackBot: contagem, estratégia e laço de rodada
└── README.md
```

## Limitações conhecidas e próximos passos

O que o programa ainda não faz, em ordem de impacto:

- [ ] **Contar as cartas iniciais do jogador.** Hoje entram na contagem a carta do dealer, as cartas
      compradas, as dos outros jogadores e as seguintes do dealer — mas não as duas com que a mão
      começa. A contagem fica sistematicamente deslocada.
- [ ] **Estratégia de mãos suaves.** A decisão olha apenas o total, então A+7 é tratado como 18 e manda
      parar, quando a estratégia básica manda comprar ou dobrar contra 9, 10 e Ás.
- [ ] **Corrigir 13 contra 2 e 3.** A tabela atual manda comprar; a estratégia básica manda parar.
- [ ] **Recomendação de split.** O programa aceita dividir a mão, mas quem decide é o jogador — não há
      tabela de pares. Faltam os casos clássicos: sempre dividir 8 e A, nunca dividir 10 e 5.
- [ ] **Recomendação de seguro.** O seguro é oferecido quando o dealer mostra Ás, mas sem consultar a
      contagem. O critério padrão é aceitar a partir de contagem verdadeira +3.
- [ ] **Fazer a regra de soft 17 valer.** A opção é perguntada e guardada, mas o dealer compra até 17
      nos dois casos, então a escolha não muda comportamento nenhum.
- [ ] **Exibir o histórico.** As decisões são registradas em memória, mas nunca mostradas nem exportadas.
- [ ] **Cobertura de testes** para a contagem e para a tabela de decisão, que são a parte conferível
      sem mesa nenhuma.

## Aviso

Projeto educacional, escrito para praticar lógica de decisão e aritmética de contagem. Contagem de
cartas não é ilegal, mas cassinos costumam proibir e reservam o direito de recusar jogadores. Jogo de
aposta envolve risco de perda financeira, e nenhum sistema de contagem elimina isso — a vantagem
teórica de um contador competente fica em torno de 1%, e só se realiza no longo prazo.
