def straight_rank(hand: list[str]) -> int: # 0 for not a straight
    numbers = []
    for card in hand:
        numbers.append(int(card[1:]))
    numbers.sort(reverse = True)
    if numbers == [14, 5, 4, 3, 2]: return 7378945280
    last = numbers[0]
    for number in numbers[1:]:
        if number != last - 1: return 0
        last -= 1
    return numbers[0] * (14 ** 8)

def flush_rank(hand: list[str]) -> int:
    suits = []
    numbers = []
    for card in hand:
        numbers.append(int(card[1:]))
        suits.append(card[0])
    last = suits[0]
    for suit in suits[1:]:
        if suit != last: return 0
    numbers.sort(reverse = True)
    return numbers[0] * (14 ** 9) + numbers[1] * (14 ** 3) + numbers[2] * (14 ** 2) + numbers[3] * 14 + numbers[4]

def straight_flush_rank(hand: list[str]) -> int:
    if not straight_rank(hand) or not flush_rank(hand): return 0
    numbers = []
    for card in hand:
        numbers.append(int(card[1:]))
    numbers.sort(reverse = True)
    if numbers == [14, 5, 4, 3, 2]: return 283469561876480
    last = numbers[0]
    for number in numbers[1:]:
        if number != last - 1: return 0
        last -= 1
    return numbers[0] * (14 ** 12)

def four_rank(hand: list[str]) -> int:
    numbers = []
    for card in hand:
        numbers.append(int(card[1:]))
    number_count = {}
    for number in numbers:
        if number in number_count.keys():
            number_count[number] += 1
        else:
            number_count[number] = 1
    high_number, low_number = 0, 0
    for number, count in number_count.items():
        if count != 4 and count != 1: return 0
        if count == 4: high_number += number
        if count == 1: low_number += number
    if high_number == 0: return 0
    return high_number * (14 ** 11) + low_number

def full_rank(hand: list[str]) -> int:
    numbers = []
    for card in hand:
        numbers.append(int(card[1:]))
    number_count = {}
    for number in numbers:
        if number in number_count.keys():
            number_count[number] += 1
        else:
            number_count[number] = 1
    high_number, low_number = 0, 0
    for number, count in number_count.items():
        if count != 3 and count != 2: return 0
        if count == 3: high_number += number
        if count == 2: low_number += number
    return high_number * (14 ** 10) + low_number

def three_rank(hand: list[str]) -> int:
    numbers = []
    for card in hand:
        numbers.append(int(card[1:]))
    number_count = {}
    for number in numbers:
        if number in number_count.keys():
            number_count[number] += 1
        else:
            number_count[number] = 1
    three_number, high_number, low_number = 0, 0, 0
    for number, count in number_count.items():
        if count != 3 and count != 1: return 0
        if count == 3: three_number += number
        if count == 1:
            if low_number == 0:
                low_number += number
            elif low_number < number:
                high_number += number
            else:
                low_number, high_number = number, low_number
    if 0 in [three_number, high_number, low_number]: return 0
    return three_number * (14 ** 7) + high_number * 14 + low_number

def two_rank(hand: list[str]) -> int:
    numbers = []
    for card in hand:
        numbers.append(int(card[1:]))
    number_count = {}
    for number in numbers:
        if number in number_count.keys():
            number_count[number] += 1
        else:
            number_count[number] = 1
    high_pair, low_pair, kicker = 0, 0, 0
    for number, count in number_count.items():
        if count != 2 and count != 1: return 0
        if count == 2:
            if low_pair == 0:
                low_pair += number
            else:
                high_pair += number
        if count == 1: kicker += number
    if low_pair > high_pair: low_pair, high_pair = high_pair, low_pair
    if 0 in [high_pair, low_pair, kicker]: return 0
    return high_pair * (14 ** 6) + low_pair * 14 + kicker

def pair_rank(hand: list[str]) -> int:
    numbers = []
    for card in hand:
        numbers.append(int(card[1:]))
    number_count = {}
    for number in numbers:
        if number in number_count.keys():
            number_count[number] += 1
        else:
            number_count[number] = 1
    pair = 0
    kickers = []
    for number, count in number_count.items():
        if count != 2 and count != 1: return 0
        if count == 2: pair += number
        if count == 1: kickers.append(number)
    if pair == 0: return 0
    kickers.sort(reverse = True)
    return pair * (14 ** 5) + kickers[0] * (14 ** 2) + kickers[1] * 14 + kickers[2]

def high_rank(hand: list[str]) -> int:
    numbers = []
    for card in hand:
        numbers.append(int(card[1:]))
    numbers.sort(reverse = True)
    return numbers[0] * (14 ** 4) + numbers[1] * (14 ** 3) + numbers[2] * (14 ** 2) + numbers[3] * 14 + numbers[4]

"""
a hand has a rank from royal flush to high card.
for high card, the hand value is in this equation, where first card is the biggest, last is the smallest, each has a number 2 to 14.
    rank = first * (14 ^ 4) + second * (14 ^ 3) + third * (14 ^ 2) + fourth * 14 + fifth
    for example, AQJT9 would be 14 * (14 ^ 4) + 12 * (14 ^ 3) + 11 * (14 ^ 2) + 10 * 14 + 9 = 573057
    such equation makes A3456(555327) to be higher than KJT98(531686), which is what we need.
for one pair, the hand value is in this equation
    rank = pair * (14 ^ 5) + third * (14 ^ 2) + fourth * 14 + fifth
    for example, AAKQJ would be 14 * (14 ^ 5) + 13 * (14 ^ 2) + 12 * 14 + 11 = 7532263
for two pair, the hand value is in this equation
    rank = high_pair * (14 ^ 6) + low_pair * 14 + fifth
    for example, AAKKQ would be 14 * (14 ^ 6) + 13 * 14 + 12 = 105413698
for three of a kind, the hand value is in this equation
    rank = three_of_a_kind * (14 ^ 7) + high * 14 + low
    for example, AAAKQ would be 14 * (14 ^ 7) + 13 * 14 + 12 = 1475789250
for straight, the hand value is in this equation
    rank = high * (14 ^ 8)
    special case where the straight is A2345, high is set to 5.
    for example, AKQJT would be 14 * (14 ^ 8) = 20661046784, A2345 would be 5 * (14 ^ 8) = 7378945280
for flush, the hand value is in this equation
    rank = first * (14 ^ 9) + second * (14 ^ 3) + third * (14 ^ 2) + fourth * 14 + fifth
    for example, AQJT9s would be 14 * (14 ^ 9) + 12 * (14 ^ 3) + 11 * (14 ^ 2) + 10 * 14 + 9 = 289254690209
for full house, the hand value is in this equation
    rank = three_of_a_kind * (14 ^ 10) + pair
    for example, AAAKK would be 14 * (14 ^ 10) + 13 = 4049565169677
for four of a kind, the hand value is in this equation
    rank = four_of_a_kind * (14 ^ 11) + fifth
    for example, AAAAK would be 14 * (14 ^ 11) + 13 = 56693912375309
for straight flush, the hand value is in this equation
    rank = high * (14 ^ 12)
    special case where the straight flush is A2345s, high is set to 5.
    for example, AKQJTs would be 14 * (14 ^ 12) = 793714773254144, A2345s would be 5 * (14 ^ 12) = 283469561876480
"""
def eval_hand(hand: list[str]) -> tuple[int, str]:
    if straight_flush_rank(hand): return straight_flush_rank(hand), "straight flush"
    if four_rank(hand): return four_rank(hand), "four of a kind"
    if full_rank(hand): return full_rank(hand), "full house"
    if flush_rank(hand): return flush_rank(hand), "flush"
    if straight_rank(hand): return straight_rank(hand), "straight"
    if three_rank(hand): return three_rank(hand), "three of a kind"
    if two_rank(hand): return two_rank(hand), "two pair"
    if pair_rank(hand): return pair_rank(hand), "one pair"
    return high_rank(hand), "high card"

def Deck() -> list[str]:
    deck = []
    for suit in "SHCD":
        for rank in range(2, 14):
            deck.append(f"{suit}{rank}")
    return deck

def main():
    from random import shuffle
    deck = Deck()
    for i in range(10):
        shuffle(deck)
        hand = deck[:5]
        value, rank = eval_hand(hand)
        print(str(hand) + " " + str(value) + " " + rank)

if __name__ == '__main__': main()