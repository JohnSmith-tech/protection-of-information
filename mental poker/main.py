import random
from sympy import randprime
from sympy import isprime
from methods_for_crypto.methods import *


def generate_c_number(p: int) -> int:
    c = 0
    while euclidean_algorithm(c, p)[0] != 1:
        c = random.randrange(2, p)
    return c


def eval_d_number(c: int, p: int) -> int:
    return exp_mod(euclidean_algorithm(c, p)[1], 1, p)


def generate_p() -> int:
    p = 0
    while isprime(p) == 0:
        q = randprime(0, int(pow(2, 24)))
        p = 2 * q + 1
    return p


def start_game() -> None:
    number_of_cards = 52
    number_of_players = 4
    number_of_player_cards = 2
    number_card_on_table = 5

    p = generate_p()
    print(f'P: {p}')

    keys_c = [generate_c_number(p-1) for _ in range(number_of_players)]
    keys_d = [eval_d_number(c, p-1) for c in keys_c]
    print(f'Keys c: {keys_c}')
    print(f'Keys d: {keys_d}')

    cards = [i for i in range(2, number_of_cards+2)]
    print(f'Block: {cards}')
    print(f'len block: {len(cards)}')

    for i in range(number_of_players):
        encode_cards = [exp_mod(j, keys_c[i], p) for j in cards]
        random.shuffle(encode_cards)
        cards = encode_cards

    print(f'Coding cards: {encode_cards}')

    cards_of_players = [
        [0]*number_of_player_cards for _ in range(number_of_players)]

    iter_for_distribute = 0
    for j in range(number_of_player_cards):
        for i in range(number_of_players):
            cards_of_players[i][j] = encode_cards[iter_for_distribute]
            iter_for_distribute += 1
    print(f'Cards of players: {cards_of_players}')

    used_cards = []
    for k in range(len(cards_of_players)):
        for i in range(len(cards_of_players[k])):
            used_cards.append(cards_of_players[k][i])
            for j in range(number_of_players):
                if i != j:
                    cards_of_players[k][i] = exp_mod(
                        cards_of_players[k][i], keys_d[j], p)
            cards_of_players[k][i] = exp_mod(
                cards_of_players[k][i], keys_d[i], p)
    print(f'Decode Cards_of_players: {cards_of_players}')

    cards_on_table = []
    for j in encode_cards:
        if not used_cards.__contains__(j):
            curr_card = j
            for key in keys_d:
                curr_card = exp_mod(curr_card, key, p)
            cards_on_table.append(curr_card)
        if len(cards_on_table) == number_card_on_table:
            break
    print(f'Cards on the table: {cards_on_table}')


if __name__ == "__main__":
    start_game()
