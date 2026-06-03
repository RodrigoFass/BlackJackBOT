# BlackJackBOT 🃏

Um simulador de Blackjack com contagem de cartas em Python, que recomenda as melhores jogadas baseado na estratégia básica e no sistema Hi-Lo.

## Sobre o Projeto

O BlackJackBOT acompanha o jogo em tempo real: você informa as cartas que saem, e o bot mantém a contagem atualizada e indica a jogada ótima para cada situação (Hit, Stand, Double, Split ou Insurance).

## Funcionalidades

- **Contagem de cartas Hi-Lo**: Cartas 2–6 somam +1, 7–9 são neutras, 10–Ás subtraem −1
- **True Count**: Divide a contagem atual pelo número estimado de decks restantes
- **Estratégia básica**: Recomendações de Hit, Stand, Double, Split e Insurance baseadas na mão do jogador e na carta visível do dealer
- **Suporte a Ás**: Tratamento correto de mãos suaves (soft hands)
- **Múltiplas mãos**: Suporte a split e jogo com múltiplas mãos simultâneas
- **Regra Soft 17**: Configurável para o dealer
- **Histórico de jogo**: Registra a contagem em cada decisão tomada

## Tecnologias

- **Python 3**
- Apenas bibliotecas nativas — nenhuma dependência externa

## Como Usar

```bash
python BlackJack.py
```

Siga os prompts interativos:
1. Informe as cartas da sua mão
2. Informe a carta visível do dealer
3. O bot exibe a recomendação de jogada e a contagem atual
4. Continue informando as cartas conforme são reveladas

## Estratégia Hi-Lo

| Carta  | Valor de contagem |
|--------|:-----------------:|
| 2 – 6  | +1                |
| 7 – 9  | 0                 |
| 10 – A | −1                |

Quanto maior o **true count**, maior a vantagem do jogador — o bot leva isso em conta nas recomendações.

## Estrutura do Projeto

```
BlackJackBOT/
└── BlackJack.py   # Lógica principal do jogo e contagem
```

## Aviso

Este projeto é para fins educacionais e de entretenimento. O uso de sistemas de contagem de cartas em cassinos físicos pode ser proibido.
