class BlackjackBot:
    def __init__(self):
        self.num_decks = 0
        self.running_count = 0
        self.cards_played = 0
        self.history = []
        self.allow_insurance = True
        self.dealer_stands_on_soft_17 = False

    def set_num_decks(self, num_decks):
        """Define o número de baralhos e valida a entrada."""
        if num_decks <= 0:
            raise ValueError("Número de baralhos deve ser maior que 0.")
        self.num_decks = num_decks

    def reset(self):
        """Reseta a contagem e o número de cartas jogadas."""
        self.running_count = 0
        self.cards_played = 0

    def update_count(self, card):
        """Atualiza a contagem com base na carta recebida."""
        card_values = {
            '2': 0.5, '3': 1, '4': 1, '5': 1.5, '6': 1,
            '7': 0.5, '8': 0, '9': -0.5, '10': -1, 'J': -1,
            'Q': -1, 'K': -1, 'A': -1
        }
        if card in card_values:
            self.running_count += card_values[card]
            self.cards_played += 1
        else:
            print(f"Carta inválida encontrada na atualização da contagem: {card}")

    def true_count(self):
        """Calcula a contagem verdadeira baseada na contagem corrente e o número de baralhos restantes."""
        remaining_decks = max(self.num_decks - (self.cards_played / 52), 1)
        return self.running_count / remaining_decks

    def calculate_hand_value(self, hand_cards):
        """Calcula o valor da mão do jogador considerando múltiplos ases e situações de bust."""
        total_value = 0
        num_aces = 0

        for card in hand_cards:
            if card.isdigit():
                total_value += int(card)
            elif card in ['J', 'Q', 'K']:
                total_value += 10
            elif card == 'A':
                num_aces += 1

        # Adiciona o valor dos ases
        total_value += num_aces  # Contando todos os ases como 1 inicialmente
        for _ in range(num_aces):
            if total_value + 10 <= 21:
                total_value += 10  # Ajusta o valor do ás de 1 para 11

        return total_value

    def get_action(self, player_value, dealer_card):
        """Determina a melhor ação baseada na estratégia básica de Blackjack e na contagem verdadeira."""
        dealer_value = self.calculate_hand_value([dealer_card])
        true_count = self.true_count()

        if player_value >= 17:
            return "Parar"
        elif player_value == 16:
            if dealer_value in [2, 3, 4, 5, 6] or (dealer_value == 10 and true_count >= 2):
                return "Parar"
            else:
                return "Comprar mais uma carta"
        elif player_value == 15:
            if dealer_value in [2, 3, 4, 5, 6] or (dealer_value == 10 and true_count >= 2):
                return "Parar"
            else:
                return "Comprar mais uma carta"
        elif player_value == 14:
            if dealer_value in [2, 3, 4, 5, 6]:
                return "Parar"
            else:
                return "Comprar mais uma carta"
        elif player_value == 13:
            if dealer_value in [4, 5, 6]:
                return "Parar"
            else:
                return "Comprar mais uma carta"
        elif player_value == 12:
            if dealer_value in [4, 5, 6]:
                return "Parar"
            else:
                return "Comprar mais uma carta"
        elif player_value == 11:
            return "Dobrar" if true_count >= 1 else "Comprar mais uma carta"
        elif player_value == 10:
            return "Dobrar" if true_count >= 2 else "Comprar mais uma carta"
        elif player_value == 9:
            return "Dobrar" if dealer_value in [3, 4, 5, 6] and true_count >= 1 else "Comprar mais uma carta"
        else:
            return "Comprar mais uma carta"

    def handle_insurance(self, dealer_card):
        """Lida com a opção de seguro quando o dealer mostra um Ás."""
        if self.allow_insurance and dealer_card == 'A':
            action = input("O dealer mostra um Ás. Deseja fazer seguro? (S/N): ").upper()
            if action == 'S':
                print("Você fez seguro.")
                # Lógica adicional para lidar com o seguro pode ser adicionada aqui
            else:
                print("Você optou por não fazer seguro.")
        else:
            print("Seguro não disponível ou não aplicável.")

    def validate_card(self, card):
        """Valida a entrada da carta."""
        return card in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def validate_hand_input(self, hand_input):
        """Valida a entrada da mão do jogador."""
        cards = hand_input.split()
        return all(self.validate_card(card) for card in cards)

    def ask_for_action(self, player_value, dealer_card, hand_cards):
        """Solicita a melhor ação e exibe a contagem atual."""
        action = self.get_action(player_value, dealer_card)
        true_count = self.true_count()
        print(f"\nContagem Corrente: {self.running_count:.1f}")
        print(f"Contagem Verdadeira: {true_count:.2f}")
        print(f"Valor da sua mão: {player_value}")
        print(f"Melhor ação com base na carta visível do dealer: {action}")

        # Adiciona ao histórico das rodadas
        self.history.append({
            "player_hand": hand_cards,
            "dealer_card": dealer_card,
            "action": action,
            "running_count": self.running_count,
            "true_count": true_count
        })

        action_input = input("Digite sua ação (Comprar/Parar/Dobrar): ").capitalize()
        if action_input not in ["Comprar", "Parar", "Dobrar"]:
            print("Ação inválida. Usando a ação recomendada.")
            action_input = action

        return action_input

    def handle_split(self, player_cards, dealer_card):
        """Lida com a lógica de dividir uma mão."""
        print("Você dividiu sua mão. Cada nova mão será jogada separadamente.")

        hands = [[player_cards[0]], [player_cards[1]]]
        for i in range(2):
            new_card = input(f"\nDigite a carta inicial para a mão {i + 1}: ").upper()
            if not self.validate_card(new_card):
                print("Carta inválida.")
                continue
            self.update_count(new_card)
            hands[i].append(new_card)

            # Para evitar solicitar ações repetidas após divisão
            player_value = self.calculate_hand_value(hands[i])
            print(f"\n--- Mão {i + 1} ---")
            print(f"Valor da mão {i + 1}: {player_value}")
            print(f"Melhor ação com base na carta visível do dealer: {self.get_action(player_value, dealer_card)}")

        return hands

    def handle_double(self, player_cards):
        """Lida com a lógica de dobrar a aposta."""
        print("Dobrando a aposta...")
        new_card = input("Digite a carta comprada após dobragem: ").upper()
        if not self.validate_card(new_card):
            print("Carta inválida.")
            return
        self.update_count(new_card)
        player_cards.append(new_card)

    def dealer_logic(self, dealer_hand):
        """Executa a lógica de compra do dealer de acordo com as regras definidas."""
        dealer_value = self.calculate_hand_value(dealer_hand)
        while dealer_value < 17:
            new_card = input("Digite a carta comprada pelo dealer: ").upper()
            if not self.validate_card(new_card):
                print("Carta inválida.")
                continue
            self.update_count(new_card)
            dealer_hand.append(new_card)
            dealer_value = self.calculate_hand_value(dealer_hand)

        if self.dealer_stands_on_soft_17 and dealer_value == 17 and 'A' in dealer_hand:
            print("O dealer para em 17 suave.")
            return dealer_hand

        return dealer_hand

    def run(self):
        """Executa o bot de Blackjack."""
        self.num_decks = int(input("Quantos baralhos estão sendo utilizados? "))
        self.dealer_stands_on_soft_17 = input("O dealer para em 17 suave? (S/N): ").strip().upper() == 'S'

        self.reset()

        while True:
            print("\n--- Nova Rodada ---")

            player_hand = input("Digite as cartas da sua mão (ex: 10 A): ").upper()
            if player_hand == 'SAIR':
                break
            if not self.validate_hand_input(player_hand):
                print("Entrada inválida. Certifique-se de usar cartas válidas (2-10, J, Q, K, A).")
                continue

            dealer_card = input("Digite a carta visível do dealer (ex: 5): ").upper()
            if not self.validate_card(dealer_card):
                print("Entrada inválida para a carta do dealer.")
                continue

            self.update_count(dealer_card)
            self.handle_insurance(dealer_card)

            player_cards = player_hand.split()
            player_value = self.calculate_hand_value(player_cards)

            if len(player_cards) == 2 and player_cards[0] == player_cards[1]:
                print("Você tem um par!")
                action = input(
                    "Deseja dividir (D), dobrar (B), comprar mais uma carta (C) ou parar (P)? ").upper()
                if action == 'D':
                    hands = self.handle_split(player_cards, dealer_card)
                    for i, hand in enumerate(hands):
                        hand_value = self.calculate_hand_value(hand)
                        print(f"\n--- Mão {i + 1} ---")
                        print(f"Valor da mão {i + 1}: {hand_value}")
                        print(f"Melhor ação com base na carta visível do dealer: {self.get_action(hand_value, dealer_card)}")
                        action_input = input(f"Digite sua ação para a mão {i + 1} (Comprar/Parar/Dobrar): ").capitalize()
                        while action_input == "Comprar":
                            new_card = input("Digite a carta comprada: ").upper()
                            if not self.validate_card(new_card):
                                print("Carta inválida.")
                                continue
                            self.update_count(new_card)
                            hand.append(new_card)
                            hand_value = self.calculate_hand_value(hand)
                            if hand_value > 21:
                                print(f"Você estourou com {hand_value}.")
                                break
                            action_input = self.get_action(hand_value, dealer_card)
                            print(f"Valor da mão {i + 1}: {hand_value}")
                elif action == 'B':
                    self.handle_double(player_cards)
                elif action == 'P':
                    print("Você escolheu parar.")
                else:
                    print("Comprando mais uma carta...")
                    new_card = input("Digite a carta comprada: ").upper()
                    if not self.validate_card(new_card):
                        print("Carta inválida.")
                        continue
                    self.update_count(new_card)
                    player_cards.append(new_card)
            else:
                action = self.ask_for_action(player_value, dealer_card, player_cards)
                while action == "Comprar":
                    new_card = input("Digite a carta comprada: ").upper()
                    if not self.validate_card(new_card):
                        print("Carta inválida.")
                        continue
                    self.update_count(new_card)
                    player_cards.append(new_card)
                    player_value = self.calculate_hand_value(player_cards)
                    if player_value > 21:
                        print(f"Você estourou com {player_value}.")
                        break
                    action = self.ask_for_action(player_value, dealer_card, player_cards)
                if player_value > 21:
                    continue

            other_players_cards = input(
                "\nDigite as cartas compradas por outros jogadores (separadas por espaço, ex: 9 J), ou pressione Enter se não houver: ").upper()
            other_players_cards = other_players_cards.split()

            for card in other_players_cards:
                if self.validate_card(card):
                    self.update_count(card)
                else:
                    print(f"Carta inválida encontrada na entrada de outros jogadores: {card}")

            dealer_subsequent_cards = input(
                "\nDigite as cartas subsequentes do dealer (separadas por espaço, ex: 2 3), ou pressione Enter se não houver: ").upper()
            dealer_subsequent_cards = dealer_subsequent_cards.split()

            for card in dealer_subsequent_cards:
                if self.validate_card(card):
                    self.update_count(card)
                else:
                    print(f"Carta inválida encontrada na entrada subsequente do dealer: {card}")

            dealer_hand = [dealer_card] + dealer_subsequent_cards
            dealer_hand = self.dealer_logic(dealer_hand)
            dealer_value = self.calculate_hand_value(dealer_hand)

            true_count = self.true_count()
            print(f"\nContagem Corrente atualizada: {self.running_count:.1f}")
            print(f"Contagem Verdadeira atualizada: {true_count:.2f}")
            print(f"Valor final da mão do dealer: {dealer_value}")
            print(f"Valor final da sua mão (mãos divididas, se aplicável):")
            for i, hand in enumerate(hands if len(player_hand.split()) == 2 and player_hand.split()[0] == player_hand.split()[1] else [player_cards]):
                hand_value = self.calculate_hand_value(hand)
                print(f"Mão {i + 1}: {hand_value}")

# Executar o bot
bot = BlackjackBot()
bot.run()