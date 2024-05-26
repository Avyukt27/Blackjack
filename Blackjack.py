import argparse
import requests

parser = argparse.ArgumentParser(
    "Blackjack",
    "To play Virtual Blackjack in you Terminal",
)

parser.add_argument(
    '-debug', '--debug',
    default=0,
    type=int,
    choices=[0, 1],
    help='To debug the program (See hidden values)'
)

args = parser.parse_args()
debug = True if vars(args)['debug'] else False

#* Create 6 New Decks and Shuffle them
NEW_DECK = 'https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=6'
data = requests.get(NEW_DECK).json()
deck_id = data['deck_id']

#* HTTPS Links for API
DRAW = f'https://www.deckofcardsapi.com/api/deck/{deck_id}/draw/?count='
PLAYER_HAND = f'https://www.deckofcardsapi.com/api/deck/{deck_id}/pile/player_hand/add/?cards='
DEALER_HAND = f'https://www.deckofcardsapi.com/api/deck/{deck_id}/pile/dealer_hand/add/?cards='

#* Prepare Player and Dealer Hands and Values
player_cards: list[str] = []
dealer_cards: list[str] = []
known_dealer_cards: list[str] = []

values = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "0": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
}
player_value = 0
dealer_value = 0
known_dealer_value = 0

dealer_cutoff = 17

#* Betting
bet = 0

#* Draw from the deck
def draw(cards_to_draw: int=1, player: bool=True) -> None:
    data = requests.get(DRAW + str(cards_to_draw)).json()
    cards = data['cards']
    drawn_cards: list[str] = []
    prev_card: list[str] = []
    for i, card in enumerate(cards):
        drawn_cards.append(card["code"])
        prev_card = list(drawn_cards[i])
        if player:
            say_card(prev_card, action=1)
            add_to_player_hand(drawn_cards[i])
            view_score()
        else:
            print("The dealer drew a card")
            add_to_dealer_hand(drawn_cards[i])
            if len(dealer_cards) > 1:
                say_card(list(dealer_cards[-2]), person=1)

#* Print a Card to the screen
def say_card(card: list[str], action: int=0, person: int=0) -> None:
    verb = "have"
    if action == 1:
        verb = "drew"
    if action == 2:
        verb = "played"
    
    actor = "You"
    if person == 1:
        actor = "The dealer"
    
    value = ''
    suit = ''

    match card[1]:
        #* Spades
        case "S":
            suit = "Spades"
            match card[0]:
                case "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                    value = card[0]
                case "A":
                    value = "Ace"
                case "0":
                    value = "10"
                case "J":
                    value = "Jack"
                case "Q":
                    value = "Queen"
                case "K":
                    value = "King"
        #* Diamonds
        case "D":
            suit = "Diamonds"
            match card[0]:
                case "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                    value = card[0]
                case "A":
                    value = "Ace"
                case "0":
                    value = "10"
                case "J":
                    value = "Jack"
                case "Q":
                    value = "Queen"
                case "K":
                    value = "King"
        #* Clubs
        case "C":
            suit = "Clubs"
            match card[0]:
                case "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                    value = card[0]
                case "A":
                    value = "Ace"
                case "0":
                    value = "10"
                case "J":
                    value = "Jack"
                case "Q":
                    value = "Queen"
                case "K":
                    value = "King"
        #* Hearts
        case "H":
            suit = "Hearts"
            match card[0]:
                case "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9":
                    value = card[0]
                case "A":
                    value = "Ace"
                case "0":
                    value = "10"
                case "J":
                    value = "Jack"
                case "Q":
                    value = "Queen"
                case "K":
                    value = "King"
    print(f"{actor} {verb} a {value} of {suit}")

#* Add a Card to the Player's Hand
def add_to_player_hand(card: str) -> None:
    global player_cards

    player_cards.append(card)
    player_cards_url_part = (' '.join([_ for _ in player_cards])).replace(' ', ',')
    requests.get(PLAYER_HAND + player_cards_url_part)

#* Add a card to the Dealer's Hand
def add_to_dealer_hand(card: str) -> None:
    global dealer_cards
    global known_dealer_cards

    dealer_cards.append(card)
    known_dealer_cards = dealer_cards[0:len(dealer_cards) - 1]
    dealer_cards_url_part = (' '.join([_ for _ in dealer_cards])).replace(' ', ',')
    requests.get(DEALER_HAND + dealer_cards_url_part)

#* View the score of a person
#* True for Player, False for Dealer
def view_score(player: bool=True, debug: bool=False) -> None:
    global player_value
    global dealer_value
    global known_dealer_value
    
    if player:
        player_value = 0
        for card in player_cards:
            player_value += values[card[0]]
        print(f'Your score is: {player_value}')
        if player_value == 21:
            print("You got a Blackjack!")
        if player_value > 21:
            print("You Bust")
    else:
        dealer_value = 0
        for card in dealer_cards:
            dealer_value += values[card[0]]
        for card in known_dealer_cards:
            known_dealer_value += values[card[0]]
        print(f'The dealer\'s known score is: {known_dealer_value}')
        if debug:
            print(f'The dealer\'s score is: {dealer_value}')
        if dealer_value == 21:
            print("The dealer got a Blackjack")
        if dealer_value > 21:
            print("The dealer bust")

#* Declare the winner of the Game
def decalre_winner(player_score: int, dealer_score: int) -> None:
    if dealer_score > 21 and player_score > 21: #? Tie
        print("Tie")
    if dealer_score == player_score:
        print("Tie")
    if dealer_score > 21 and player_score < 21: #? Player Wins
        print("You Win!\nBet Doubled!")
    if dealer_score != 21 and player_score == 21:
        print("You Win!\nBet Doubled!")
    if dealer_score < player_score and player_score <= 21:
        print("You Win!\nBet Doubled!")
    if dealer_score < 21 and player_score > 21: #? Dealer Wins
        print("You Lose!\nBet Lost!")
    if dealer_score == 21 and player_score != 21:
        print("You Lose!\nBet Lost!")
    if dealer_score > player_score and dealer_score <= 21:
        print("You Lose!\nBet Lost!")

#* Main function
def main():
    while True:
        try:
            bet = input("How much will you bet: ")
        except TypeError:
            print("Number Please")
            continue
        else:
            bet = int(bet)
            break
    while True:
        action = input(f"\nAction (Bet of ${bet}): ")
        match action.lower():
            case "hit" if player_value <= 21:
                draw()
                if dealer_value < dealer_cutoff:
                    draw(player=False)
            case "stand" if player_value > 0:
                while dealer_cutoff > dealer_value:
                    draw(player=False)
                    view_score(player=False, debug=True)
                decalre_winner(player_value, dealer_value)
                break
            case "list":
                for card in player_cards:
                    say_card(list(card))
            case "score":
                view_score()
            case "dealer":
                if len(dealer_cards) > 1:
                    for card in dealer_cards[0:len(dealer_cards) - 1]:
                        say_card(list(card), person=1)
                elif len(dealer_cards) == 1:
                    print("Hidden")
                view_score(player=False, debug=debug)
            case "exit" | "":
                break

if __name__ == '__main__':
    main()