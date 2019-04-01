# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "What's it gonna be? Hit or stand?"
user_score = 0
cpu_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):

        result = ""
        for card in self.cards:
            result += " " + card.__str__()

        return "Hand contains" + result

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        value = 0
        there_is_an_ace = False

        for card in self.cards:
            rank = card.get_rank()
            value += VALUES[rank]

            if(rank == 'A'):
                there_is_an_ace = True

        if(value < 11 and there_is_an_ace):
            value += 10

        return value

    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas, pos)
            pos[0] += 80 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit,rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)
    
    def __str__(self):
        result = ""
        for card in self.cards:
            result += " " + card.__str__()
        
        return "Deck contains" + result

#Define event handlers for buttons
def deal():
    global outcome, in_play, deck, user_hand, cpu_hand, cpu_score
    
    if (in_play == True):
        outcome = "You gave up! New deal?"
        cpu_score += 1
        in_play = False
    else:
        deck = Deck()
        outcome
        deck.shuffle()
        
        user_hand = Hand()
        cpu_hand = Hand()
        
        user_hand.add_card(deck.deal_card())
        user_hand.add_card(deck.deal_card())
        
        cpu_hand.add_card(deck.deal_card())
        cpu_hand.add_card(deck.deal_card())
        
        print "Player: %s" % user_hand
        print "CPU: %s" % cpu_hand
        
        in_play = True

def hit():
    global outcome, in_play

    if in_play:
        if user_hand.get_value() <= 21:
            user_hand.add_card(deck.deal_card())

        print "Player hand %s" % user_hand

        if user_hand.get_value() > 21:
            outcome = "You have busted. New deal?"
            in_play = False
            print "You have busted"

def stand():
    global outcome, user_score, cpu_score, in_play

    in_play = False

    while cpu_hand.get_value() < 17:
        cpu_hand.add_card(deck.deal_card())

    print "Dealer: %s" % cpu_hand

    if cpu_hand.get_value() > 21:
        outcome = "CPU's busted. Congrats!"
        print "CPU is busted. You win!"
        user_score += 1
    else:
        if cpu_hand.get_value() >= user_hand.get_value() or user_hand.get_value() > 21:
            print "CPU wins"
            outcome = "CPU wins. New deal?"
            cpu_score += 1
        else:
            print "Player wins. New deal?"
            outcome = "Player wins"
            user_score += 1

# Draw handler    
def draw(canvas):
    global outcome, in_play, card_back, card_loc, user_score, cpu_score
    canvas.draw_text("Blackjack", [220, 50], 45 ,"Blue")
    user_hand.draw(canvas, [100, 300])
    cpu_hand.draw(canvas, [100, 150])
    
    canvas.draw_text(outcome, [10, 100], 40 ,"Blue")
    
    canvas.draw_text("CPU: %s" % cpu_score, [10, 150], 20 ,"White")
    canvas.draw_text("Player: %s" % user_score, [10, 300], 20 ,"White")
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (136,199), CARD_BACK_SIZE)

# Initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# Create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# Start the game
deal()
frame.start()