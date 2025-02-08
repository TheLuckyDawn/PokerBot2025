'''
Simple example pokerbot, written in Python.
'''
from math import floor

import eval7

from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, BidAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
from eval7 import Card
import random

startRanking = 0

class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        pass

    def rate_start_hand(self, my_cards):
        handRating = 0
        isSameSuit = my_cards[0][1] == my_cards[1][1]
        isPair = my_cards[0][0] == my_cards[1][0]
        card1 = Card(my_cards[0])
        card2 = Card(my_cards[1])

        if isSameSuit:
            handRating += 250 #adds some ranking for same suit

        if isPair:
            handRating += 500 + card1.rank * 250 #adds a lot of rating for pairs, especially higher pairs

        handRating += card1.rank * 50
        handRating += card2.rank * 50 #adds 25 for each rank 

        if abs(card2.rank - card1.rank) < 5 and not isPair:
            handRating += (5 - abs(card2.rank - card1.rank)) * 50 #adds some rating for cards close enough for straights

        print("Hand: " + my_cards[0] + ", " + my_cards[1] + " -> Rating: " + str(handRating) + " -> Distance: " + str(abs(card2.rank - card1.rank)))
        return handRating

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''

        

        #my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        #game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        #round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        my_cards = round_state.hands[active]  # your cards
        my_stack = round_state.stacks[active]
        #big_blind = bool(active)  # True if you are the big blind
        pass

        

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        opp_bid = terminal_state.bids[1-active]  # How much opponent bid previously (available only after auction)

        if opp_bid != None:
            opp_bids.append(opp_bid)

    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        # May be useful, but you may choose to not use.
        min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        my_bid = round_state.bids[active]  # How much you bid previously (available only after auction)
        opp_bid = round_state.bids[1-active]  # How much opponent bid previously (available only after auction)
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot



        # very naive equity calculator
        # In theory we try and guess opponents hand but worse comes to worst we can
        # just test against a ton of random hands
        # deck = eval7.Deck()
        # deck.shuffle()
        # random_hand = deck.deal(2)
        # hand_range = eval7.HandRange(str(random_hand[0])[0] + str(random_hand[1])[0])

        bet_pct = (opp_pip / STARTING_STACK) + street/10

        range = None
        if bet_pct > .9:
            range = eval7.HandRange("KK+, AK+")
        elif bet_pct > .8:
            range = eval7.HandRange("77-88, T5s-T8s, A6o-A9o, K6o-K9o")
        else:
            range = eval7.HandRange("62s+, 52s+, 42s+, 32s, 62o+, 52o+, 42o+, 32o")

        equity = eval7.py_hand_vs_range_monte_carlo(list(map(eval7.Card, my_cards)), range, list(map(eval7.Card, board_cards)), 200)


        deck = eval7.Deck()
        deck.shuffle()
        random_hand = deck.deal(2)
        hand_range = eval7.HandRange(str(random_hand[0])[0] + str(random_hand[1])[0])
        equity = eval7.py_hand_vs_range_monte_carlo(list(map(eval7.Card, my_cards)), hand_range, list(map(eval7.Card, board_cards)), 200)
        print("Equity: " + str(equity))
        if street == 0:
            startRanking = self.rate_start_hand(my_cards)
            print(legal_actions)
            if BidAction in legal_actions:
                print("bid")
                card1 = Card(my_cards[0])
                card2 = Card(my_cards[1])
                if len(opp_bids) > 0 and (abs(card2.rank - card1.rank) < 5 and card2.rank != card1.rank) or card1.suit == card2.suit:
                    return BidAction(min(30, floor(sum(opp_bid)/len(opp_bid))+1))
                return BidAction(1)
            elif (startRanking < 600) and CheckAction in legal_actions:
                print("checked bad hand first")
                return CheckAction()
            elif (startRanking < 600) and FoldAction in legal_actions:
                return FoldAction()
            elif (startRanking > 2000) and RaiseAction in legal_actions and my_contribution < my_stack*0.2:
                print("raised by " + str(max(min_raise, min(floor(max_raise*(startRanking/4550)*0.7), max_raise))))
                return RaiseAction(max(min_raise, min(floor(max_raise*(startRanking/4550)*0.7), max_raise)))
            elif CheckAction in legal_actions:
                print("checked")
                return CheckAction()
            elif (startRanking > 2000) or (continue_cost/my_stack)*(random.randint(9,11)/10) < 0.15 and CallAction in legal_actions:
                print("called a " + str(continue_cost) + " bet, worth " + str(continue_cost/my_stack) + " of our stack of " + str(my_stack))
                return CallAction()
            elif FoldAction in legal_actions:
                print("folded by default")
                return FoldAction()

        if equity < 0.25 and FoldAction in legal_actions:
             print("fold late hand")
             return FoldAction()

        #goes all in randomly 
        if RaiseAction in legal_actions and random.randint(1, 200) == 200:
            print("all in")
            return RaiseAction(max_raise)

        if equity < 0.35 and CheckAction in legal_actions:
            print("check")
            return CheckAction()

        if equity < 0.5 and CallAction in legal_actions:
            print("call bc low equity")
            return CallAction()

        if RaiseAction in legal_actions:
            print("raise action")
            min_cost = min_raise - my_pip  # the cost of a minimum bet/raise
            max_cost = max_raise - my_pip  # the cost of a maximum bet/raise
            return RaiseAction(max(min_raise, floor(0.3 * max_raise)))
        elif CallAction in legal_actions:
            print("call bc cant raise")
            return CallAction()
        elif CheckAction in legal_actions:
            print("check")
            return CheckAction()
        elif BidAction in legal_actions:
            print("bid")
            return BidAction(2)



        print("default call")
        return CallAction()
    


if __name__ == '__main__':
    run_bot(Player(), parse_args())
