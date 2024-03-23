import random


def create_deck():
    """
    Creates a 52 card deck card, each of which is an instance of class Card, and returns it as a list

    :return: A standard deck of cards (52 cards consisting of a combination of 13 ranks and 4 suits)1
    """
    deck = []
    card_suit = {'♠', '♦', '♥', '♣'}
    card_rank = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14}
    for i in card_rank:
        for j in card_suit:
            deck.append(Card(i, j))
    return deck


class Card:
    """
    Used to make cards for the game of blackjack

    :attribute rank: The rank of the specific card
    :attribute suit: The suit of the specific card
    """

    def __init__(self, rank, suit):
        """
        Initializes the card object

        :param rank: Gives the attribute rank a specific value
        :param suit: Gives the attribute suit one of the four possible card-suits
        """
        self.rank = rank
        self.suit = suit

    def get_value(self):
        """
        Gets the value of a card based on its rank.
        Face cards are 10 and any other card is its pip value while and ace is given an initial value of 11.

        :return: The value of the card based on its rank
        """
        if self.rank < 10:
            return self.rank
        if self.rank < 14:
            return 10
        return 11

    def get_count_HiLo(self):
        """
        Gets the card-count value of the specific card (In the Hi-Lo system)

        :return: The card-count value based on the cards rank and what that translates to in the Hi-Lo card-counting system
        """
        if self.rank < 7:
            return 1
        elif self.rank < 10:
            return 0
        else:
            return -1

    def get_count_Halves(self):
        """
        Gets the card-count value of the specific card (In the Halves system)

        :return: The card-count value based on the cards rank and what that translates to in the Halves card-counting system
        """
        if self.rank in [2, 7]:
            return 0.5
        elif self.rank == 9:
            return -0.5
        elif self.rank in [3, 4, 6]:
            return 1
        elif self.rank in [10, 11, 12, 13, 14]:
            return -1
        elif self.rank == 8:
            return 0
        else:
            return 1.5

    def get_count_Zen(self):
        """
        Gets the card-count value of the specific card (In the Zen Count system)

        :return: The card-count value based on the cards rank and what that translates to in the Zen Count card-counting system
        """
        if self.rank in [2, 3, 7]:
            return 1
        elif self.rank in [4, 5, 6]:
            return 2
        elif self.rank in [8, 9]:
            return 0
        elif self.rank in [10, 11, 12, 13]:
            return -2
        else:
            return -1


class CardShoe:
    """
    Used to store a list of type Card as well as all cards that have been discarded and the card count of the card-shoe

    :attribute cardShoe: A list meant to store cards within it, used for anything from players hands to the card-shoe that contains the decks blackjack will be played with
    :attribute discardShoe: A list meant to store cards that formally resided in the card-shoe list
    :attribute currentCardCount: The current card-count, dependent on what cards are in the discardShoe and what card count type was chosen by the player
    """

    def __init__(self):
        """
        Initializes a card-shoe
        """
        self.cardShoe = []
        self.discardShoe = []
        self.currentCardCount = 0

    def len_cardshoe(self):
        """
        Calculates and returns the length of the attribute cardShoe.

        :return: The length of the attribute cardShoe
        """
        return len(self.cardShoe)

    def add_cards(self, listOfCards):
        """
        Adds the given list of cards to the attribute cardShoe

        :param listOfCards: The list of cards that will be added to the attribute cardShoe
        """
        self.cardShoe.extend(listOfCards)

    def blank_shoe(self):
        """
        Clears the cardShoe's attribute cardShoe and discardShoe of any cards.
        This will automatically reset the card-count the next time it is calculated seeing as the discardShoe is now clear.
        """
        self.cardShoe.clear()
        self.discardShoe.clear()

    def draw(self, amount):
        """
        Removes a certain amount of cards from the attribute cardShoe and both returning them and placing them in the attribute discardShoe
        They are placed into the attribute discardShoe here so we don't have to deal with it later in the code.

        :param amount: The amount of cards to be drawn
        :return: A list of cards from the attribute cardShoe
        """
        cardsDrawn = []
        for i in range(amount):
            cardsDrawn.append(self.cardShoe[0])
            self.cardShoe.pop(0)
        self.discardShoe.extend(cardsDrawn)
        return cardsDrawn

    def create_shoe(self, length):
        """
        Puts a certain amount of decks of cards into the attribute cardShoe and then shuffles the attribute.
        This is used to create a shuffled card-shoe from which cards can be drawn to play the game of Blackjack.

        :param length: The amount of decks that will be put into the attribute cardShoe
        """
        for i in range(length):
            self.cardShoe.extend(create_deck())
        random.shuffle(self.cardShoe)

    def value_hand(self):
        """
        Calculates the value of the cards in the attribute cardShoe.
        This value is not the card-count value but simply the hand value of the cardShoe.

        :return: The cumulative value of all the cards in the attribute cardShoe
        """
        num = 0
        for card in self.cardShoe:
            num += card.get_value()
        return num

    def current_HiLo_count(self):
        """
        Calculates and returns the total card count value in the players discardShoe (based on the Hi-Lo card-count System)

        :return: the cumulative card-count value of all the cards in the the discardShoe (based on the Hi-Lo card-count system)
        """
        num = 0
        for card in self.discardShoe:
            num += card.get_count_HiLo()
        self.currentCardCount = num
        return num

    def current_Halves_count(self):
        """
        Calculates and returns the total card count value in the players discardShoe (based on the Halves card-count System)

        :return: the cumulative card-count value of all the cards in the the discardShoe (based on the Halves card-count system)
        """
        num = 0
        for card in self.discardShoe:
            num += card.get_count_Halves()
        return num

    def current_Zen_count(self):
        """
        Calculates and returns the total card count value in the players discardShoe (based on the Zen Count System)

        :return: the cumulative card-count value of all the cards in the the discardShoe (based on the Zen Count system)
        """
        num = 0
        for card in self.discardShoe:
            num += card.get_count_Zen()
        return num


class Person:
    """
    This class is used to create the players, dealers and as a child class AI that will play blackjack

    :attribute money: The amount of money the person has
    :attribute dealer: A boolean used to determine if someone is a player or dealer
    (It's primary function is to show or not show one of the dealer's initial cards. The dealer has this turned of when his full hand needs to be shown)
    :attribute number: The player number of this specific Person
    :attribute hand: The player's hand of cards
    :attribute pot: The player's current bet
    :attribute count: The player's current hand value
    """

    def __init__(self, money, dealer, number, ):
        """
        Initializes an instance of class Person

        :param money: The amount of money the person starts out with
        :param dealer: Set to true if the person is the dealer, false if they are not
        :param number: The given player number of this Person
        """
        self.money = money  # The amount of money a specific Person has
        self.dealer = dealer  # Boolean used to know who is the dealer
        self.number = number  # Player Number
        self.hand = CardShoe()  # Player's hand of cards
        self.pot = 0  # The player's current bet
        self.count = 0  # THe player's current hand value

    def deal(self, cardShoe):
        """
        Deals cards to a player from the given card-shoe, placing that card in their attribute hand
        (Dealing means that two cards are given to the player)

        :param cardShoe: The cardshoe from which two cards will be drawn before they are given to the player
        """
        self.hand.add_cards(cardShoe.draw(2))

    def hit(self, cardShoe):
        """
        Hits a player with cards from the given card-shoe, placing that card in their attribute hand
        (Hitting means the player receives one card)

        :param cardShoe: The card-shoe from which one card will be drawn before that card is given to the person
        """
        self.hand.add_cards(cardShoe.draw(1))

    def bet(self, amount):
        """
        Takes a certain amount from the attribute money and adds that amount to the attribute pot

        :param amount: The amount that will be added to the players attribute pot and taken from their attribute money
        """
        self.money -= amount
        self.pot += amount

    def set_dealer_false(self):
        """
        Sets the attribute dealer to False
        Done so the dealer's first card is not shown in the function show_hand
        """
        self.dealer = False

    def set_dealer_true(self):
        """
        Sets the attribute dealer to True
        Done so the dealer's first card is shown in the function show_hand
        """
        self.dealer = True

    def show_hand(self):
        """
        Prints the Person's hand in ASCII code, with the first card being hidden depending on if the attribute dealer is true or false.
        The ASCII code used came from https://codereview.stackexchange.com/questions/82103/ascii-fication-of-playing-cards.
        It has however been altered so it works with the code created by Maurits van 't Hag
        """
        lines = [[] for i in range(9)]
        if not self.dealer:
            for card in self.hand.cardShoe:
                suit = card.suit
                rank = ""
                space = " "
                if card.rank == 10:
                    space = ""
                    rank = 10
                elif card.rank < 10:
                    rank = card.rank
                elif card.rank == 11:
                    rank = "J"
                elif card.rank == 12:
                    rank = "Q"
                elif card.rank == 13:
                    rank = "K"
                elif card.rank == 14:
                    rank = "A"
                lines[0].append('┌─────────┐')
                lines[1].append('│{}{}       │'.format(rank, space))  # use two {} one for char, one for space or char
                lines[2].append('│         │')
                lines[3].append('│         │')
                lines[4].append('│    {}    │'.format(suit))
                lines[5].append('│         │')
                lines[6].append('│         │')
                lines[7].append('│       {}{}│'.format(space, rank))
                lines[8].append('└─────────┘')
        else:
            lines[0].append('┌─────────┐')
            lines[1].append('│░░░░░░░░░│')
            lines[2].append('│░░░░░░░░░│')
            lines[3].append('│░░░░░░░░░│')
            lines[4].append('│░░░░░░░░░│')
            lines[5].append('│░░░░░░░░░│')
            lines[6].append('│░░░░░░░░░│')
            lines[7].append('│░░░░░░░░░│')
            lines[8].append('└─────────┘')

            for card in self.hand.cardShoe[1:len(self.hand.cardShoe)]:
                suit = card.suit
                rank = ""
                space = " "
                if card.rank == 10:
                    space = ""
                    rank = 10
                elif card.rank < 10:
                    rank = card.rank
                elif card.rank == 11:
                    rank = "J"
                elif card.rank == 12:
                    rank = "Q"
                elif card.rank == 13:
                    rank = "K"
                elif card.rank == 14:
                    rank = "A"
                lines[0].append('┌─────────┐')
                lines[1].append('│{}{}       │'.format(rank, space))  # use two {} one for char, one for space or char
                lines[2].append('│         │')
                lines[3].append('│         │')
                lines[4].append('│    {}    │'.format(suit))
                lines[5].append('│         │')
                lines[6].append('│         │')
                lines[7].append('│       {}{}│'.format(space, rank))
                lines[8].append('└─────────┘')

        result = []
        for index, line in enumerate(lines):
            result.append(''.join(lines[index]))
            print(result[index])

    def check_count(self):
        """
        Checks the Person's hand value then updates and returns it as their count attribute.
        The code assumes that the player both wants the highest possible hand value and does not want to go bust.
        It therefore stores the amount of aces in the player's hand and when going over a total of 21 checks if there are any in the person's hand.
        If there is it sets the aces value from 11 to 1 and repeats this process until it's hand value no longer over 21 or is out of aces.
        Finally returning the hand's value.

        :return: The players newly set count attribute
        """
        aces = 0
        self.count = 0
        for card in self.hand.cardShoe:
            if card.get_value() == 11:
                aces += 1
            self.count += card.get_value()

        while aces != 0 and self.count > 21:
            aces -= 1
            self.count -= 10
        return self.count

    def reset_pot(self):
        """
        Resets a players pot and count attribute to zero
        """
        self.pot = 0
        self.count = 0

    def return_money(self):
        """
        Returns someone their bet from their pot attribute to their money attribute and sets their count attribute to zero.
        Used when the both the player and the dealer have Blackjack.
        """
        self.money += self.pot
        self.count = 0
        self.pot = 0

    def pay_player(self, blackjack):
        """
        Pays a player after winning a hand.
        The blackjack boolean is used to see if they are being paid after getting Blackjack or be paid when beating the dealers hand

        :param blackjack: Boolean used to determine the amount of money a player will get depending on if it resulted from a blackjack or not
        """
        if blackjack:
            self.money += int(self.pot * 2.5)  # Prevents the players money from turning into a float
            self.reset_pot()  # (they will never be able to bet the decimals that are created
            # because when betting you input an integer)
        else:
            self.money += self.pot * 2
            self.reset_pot()

    def player_hand_blank(self):
        """
        Clears the players hand attribute of all cards
        """
        self.hand.blank_shoe()


class AIPlayer(Person):
    """
    A child class for the class person this class is used to create instances of AI that play the game alongside the player

    :attribute name: The AI's name.
    :attribute unit: The amount that the AI's card count-count value is off using the Hi-Lo method. Used to determine their bet size later together with attribute unit.
    :attribute risk: This is added to the number 17 to determine at what hand value the AI wil stop drawing cards.
    :attribute leaveCounter: The amount of times the AI has lost in total. The AI is programmed to leave after having lost to many times.
    :attribute leaveCondition: A threshold for which when passed causes the AI to leave the table out of tilt.
    """

    def __init__(self, name, accuracy, risk, unit, leaveCondition):
        """
        Initializes an instance of the class AIPLayer which is a child class for the class Person

        :param name: The name the AI is given when it is initialized
        :param accuracy: The amount that the AI's card count value is off using the Hi-Lo method
        :param unit: The betting unit this AI bets in
        :param risk: Sets the risk the AI is willing to take, this amount is added to 17 and that result is when the AI will stop drawing cards.
        :param leaveCondition: Sets a threshold for when the AI leaves the table
        """
        super(AIPlayer, self).__init__(0, False, 0)
        self.name = name  # The AI's name
        self.accuracy = accuracy  # The amount that the AI's card count value is off using the Hi-Lo method
        self.unit = unit  # The betting unit this AI bets in
        self.risk = risk  # This is added to the number 17 to determine at what amount the AI wil stop drawing cards
        self.leaveCounter = 0  # The amount of times the AI has lost in a row
        self.leaveCondition = leaveCondition  # The amount of times the AI loses in a row before leaving the table out of tilt

    def check_bet_size(self, cardShoe):
        """
        Checks how large the AI's bet will be based upon the current true-count with a minimum of one unit

        :param cardShoe: the cardShoe used to determine what the true count is
        :return: the amount of money that the AI will bet
        """
        decksRemaining = len(cardShoe.cardShoe) / 52
        if cardShoe.current_HiLo_count() >= 0:
            num = cardShoe.currentCardCount
            calculation = num + self.accuracy
        else:
            num = cardShoe.currentCardCount
            calculation = num - self.accuracy
        if calculation <= 0:
            return self.unit
        trueCount = decksRemaining / calculation
        return int(trueCount * self.unit)

    def check_next_move(self):
        """
        Checks the AI's current hand and if they should draw another card based upon the risk attribute

        :return: 1 for when the AI should stop drawing cards, 0 for when the AI should continue drawing cards
        """
        num = self.hand.value_hand()
        stopValue = self.risk + 17
        if num >= stopValue:
            return 1
        return 0

    def check_leave(self):
        """
        Checks if the AI will leave the table based upon the attributes leaveCounter and leaveCondition

        :return: False when the AI should stay in the game, True for when they should leave
        """
        if self.leaveCounter < self.leaveCondition:
            return False
        else:
            return True


class Game:
    """
    Class containing the functions to run blackjack and manage the players, Dealer and AI

    :attribute gameTrue: Attribute to determine if there is currently a game going on
    :attribute roundTrue: Attribute to determine if there is currently a round going on
    :attribute dealer: Creates a dealer of class Person with no money and number 0
    :attribute cardShoe: Creates a card-shoe which holds all cards and discard from the current game
    :attribute startingDecks: The amount of Decks the player has specified are being used. (to be specified in initiate_game)
    :attribute typeOfCount: The type of card-counting that will be used during this game of blackjack
    :attribute listPlayers: List of players in the game
    :attribute artificialPlayers: List of artificial players
    :attribute artificialPlayersDiscard: List of artificial players that are no longer participating in a specific round
    :attribute listOfAI: List of AI not currently at the table
    :attribute showCount: Boolean specified by player to determine if the card-count is shown between rounds.
    """

    def __init__(self):
        """
        Initializes the class Game
        """
        self.gameTrue = True  # Attribute to determine if there is currently a game going on
        self.roundTrue = True  # Attribute to determine if there is currently a round going on
        self.dealer = Person(0, True, 0)  # Creates a dealer of class Person with no money and number 0
        self.cardShoe = CardShoe()  # Creates a card-shoe which holds all cards and discard from the current game
        self.startingDecks = 0  # The amount of Decks the player has specified are being used. (to be specified in initiate_game)
        self.typeOfCount = 0  # The type of card-counting that will be used during this game of blackjack
        self.listPlayers = []  # List of players in the game
        self.artificialPlayers = []  # List of artificial players
        self.artificialPlayersDiscard = []  # List of artificial players that are no longer participating in a specific round
        self.listOfAI = []  # List of AI not currently at the table
        self.showCount = False  # Boolean specified by player to determine if the card-count is shown between rounds.
        self.showDecks = False  # Boolean specified by player to determind if the amount of decks remaining is shown between rounds.

    def start_game(self):
        """
        Starts a game and continues generating new rounds until the attribute gameTrue is set to False
        """
        self.initiate_game()
        self.fill_with_ai()

        while self.gameTrue:
            self.round()

    def initiate_game(self):
        """
        Collects the needed information to start the game of Blackjack from the player and stores it in class Game its attributes in the following order:

        1. Asks for the card-count type
        2. Asks if you would like the card-count shown between hands
        3. Asks for the number of players
        4. Asks for the amount of money every player starts out with
        """
        print("Hello Player. Welcome to blackjack.")
        print("-" * 45)

        self.typeOfCount = ask_count_type()
        self.ask_show_count()
        self.ask_show_decks()

        numPlayers = ask_num_players()
        startingMoney = ask_num_money()
        self.startingDecks = ask_num_decks()
        self.cardShoe.create_shoe(self.startingDecks)
        self.listPlayers = player_maker(numPlayers, startingMoney)

    def round(self):
        """
        Houses the format for a single round of blackjack in the following format:

        1. Check's if the cardShoe is full enough to play a round of Blackjack.
        2. Check's if an AI will join the table with a 20 percent chance of this happening.
        3. Shows the card-count if tasked to do so before every round.
        4. Resets everything from the dealer attribute to the AI.
        5. Collects the player's bets and simulates the AI's bets.
        6. Copy's the players into a list that is allowed to be changed and from which elements are allowed to be removed.
        7. Deal's cards to everyone
        8. Simulates the entire round
        9. Check's if the AI wishes to leave
        10. Resets all attributes that need to be reset.
        11. Asks the player's if they wish to leave
        12. Asks the user if they wish to stop playing Blackjack in general
        13. Checks if the players have enough money to continue
        """

        self.check_shoe()
        self.random_ai()

        self.show_card_count()
        self.show_amount_decks()

        self.reset_ai()

        print("Starting round:")
        self.roundTrue = True
        self.dealer.set_dealer_true()
        collect_bets(self.listPlayers)
        self.ai_bet()
        changeableList = self.listPlayers.copy()

        # This christmas tree structure is needed to be able to stop the round after every stage of said round
        self.deal_cards()
        if self.roundTrue:
            changeableList = self.first_check(changeableList)
            if self.roundTrue:
                changeableList = self.action_time(changeableList)
                self.ai_play()
                if len(self.listPlayers) == 0 and len(self.artificialPlayers) == 0:
                    self.roundTrue = False
                if self.roundTrue:
                    changeableList = self.dealer_draws(changeableList)
                    if self.roundTrue:
                        self.showdown(changeableList)

        self.check_if_ai_leaves()
        print("-" * 45)
        self.show_money()
        self.reset_hands()

        if self.gameTrue:
            self.check_if_leave()
        if self.gameTrue:
            self.ask_game_true()
            if not self.gameTrue:
                self.show_money()

        self.check_player_balance()

    def check_if_leave(self):
        """
        Checks if there are player who would like to leave.
        If there are it asks each player one by one if they would like to leave and removes them
        """
        print("Would any players like to leave the table?")
        answer = ask_yes_no()
        storage = []
        if answer == 1:
            for player in self.listPlayers:
                print("Would player " + str(player.number) + ".")
                remove = ask_yes_no()
                if remove == 1:
                    storage.append(player)
        for player in storage:
            self.listPlayers.remove(player)
        if len(self.listPlayers) == 0:
            self.gameTrue = False

    def check_player_balance(self):
        """
        Checks if there are players who are now broke, if there are it removes them from the game entirely
        and if there are no players left it closes the casino
        """
        for player in self.listPlayers:
            if player.money == 0:
                print("Player " + str(player.number) + " has no funds and will therefore be ejected from the Casino.")
                print("-" * 45)
                self.listPlayers.remove(player)
        if len(self.listPlayers) == 0:
            print("There is no one left.")
            print("The casino now closes.")
            self.roundTrue = False
            self.gameTrue = False

    def deal_cards(self):
        """
        Clears and then gives cards to all players, AI and the dealers hand.
        Showing all dealt cards.
        """
        self.dealer.player_hand_blank()
        self.dealer.deal(self.cardShoe)
        print("Dealer's hand:")
        self.dealer.show_hand()

        for player in self.listPlayers:
            player.player_hand_blank()
            player.deal(self.cardShoe)
            print("Player " + str(player.number) + "'s hand:")
            player.show_hand()

        for AI in self.artificialPlayers:
            AI.player_hand_blank()
            AI.deal(self.cardShoe)
            print(AI.name + " their hand")
            AI.show_hand()
        print("-" * 45)

    def first_check(self, givenList):
        """
        Checks if anyone has blackjack and acts accordingly

        :param givenList: a list of all players still playing the game
        :return: a list containing all remaining players in the game
        """
        if self.dealer.check_count() == 21:
            self.dealer.set_dealer_false()
            for player in self.listPlayers:
                if player.check_count != 21:
                    print("The dealer has blackjack, player " + str(player.number) + " does not.")
                    print("-" * 45)
                    print("Dealer's Cards")
                    self.dealer.show_hand()
                    print("Player " + str(player.number) + "'s Cards")
                    player.show_hand()
                    player.reset_pot()
                    print("Dealer takes your money, current balance player " + str(player.number) + ": " + str(
                        player.money))
                    print("-" * 45)
                else:
                    print("Both player " + str(player.number) + " and the dealer have blackjack")
                    print("Player will be given back their money.")
                    print("-" * 45)
                    print("Dealer's Cards")
                    self.dealer.show_hand()
                    print("Player " + str(player.number) + "'s Cards")
                    player.show_hand()
                    player.return_money()
                    print("Player" + str(player.number) + "'s balance is currently: " + str(player.money))
                    player.hand.blank_shoe()
                    print("-" * 45)

            for AI in self.artificialPlayers:
                if AI.check_count != 21:
                    print("The dealer has blackjack " + AI.name + " does not.")
                    print("Their bet will be taken")
                    print("-" * 45)
                    print("Dealer's Cards")
                    self.dealer.show_hand()
                    print(AI.name + " their Cards")
                    AI.show_hand()
                    AI.leaveCounter += 1
                    print("-" * 45)
                elif AI.check_count == 21:
                    print(AI.name + " and the dealer have blackjack")
                    print(AI.name + " will be given back their money.")
                    print("-" * 45)
                    print("Dealer's Cards")
                    self.dealer.show_hand()
                    print(AI.name + "Cards")
                    AI.show_hand()
                    AI.hand.blank_shoe()
                    print("-" * 45)
            self.roundTrue = False

        else:
            for player in givenList:
                if player.check_count() == 21:
                    player.pay_player(True)
                    print("Player " + str(player.number) + " got Blackjack!")
                    print("Your new balance is now: " + str(player.money))
                    givenList.remove(player)

            for AI in self.artificialPlayers:
                if AI.check_count() == 21:
                    print(AI.name + " has Blackjack.")
                    AI.leaveCounter += -1
                    self.artificialPlayersDiscard.append(AI)
                    self.artificialPlayers.remove(AI)

        if len(givenList) == 0 and len(self.artificialPlayers) == 0:
            self.roundTrue = False

        return givenList

    def action_time(self, givenList):
        """
        All the players perform their hit or stand actions

        :param givenList: a list of all player still playing the game
        :return: a list containing all remaining players still in the game
        """
        storage = []
        for player in givenList:
            playing = True
            if self.roundTrue:
                while playing:
                    print("-" * 45)
                    print("Player " + str(player.number) + " is playing")
                    player.show_hand()
                    answer = ask_player_move()
                    if answer == 2:
                        self.show_card_count()
                    elif answer == 1:
                        print("This is player " + str(player.number) + "'s final hand.")
                        player.show_hand()
                        player.check_count()
                        print("-" * 45)
                        playing = False
                    elif answer == 0:
                        player.hit(self.cardShoe)
                        player.show_hand()
                        if player.check_count() > 21:
                            print("Player " + str(player.number) + " went bust.")
                            print("Player " + str(player.number) + " has " + str(player.money) + " left")
                            player.reset_pot()
                            player.hand.blank_shoe()
                            storage.append(player)
                            print("-" * 45)
                            playing = False
        for player in storage:
            givenList.remove(player)
        return givenList

    def dealer_draws(self, givenList):
        """
        The dealer draws their cards up to card value 17

        :param givenList: a list of all player still playing the game
        :return: a list containing all remaining players still in the game
        """
        print("The dealer will now draw cards:")
        print("-" * 45)
        self.dealer.set_dealer_false()
        print("Dealer's current hand:")
        self.dealer.show_hand()
        self.dealer.check_count()

        if self.dealer.check_count() > 17:
            playing = False
        else:
            playing = True
        while playing:
            print("Dealer pulls a card:")
            self.dealer.hit(self.cardShoe)
            self.dealer.show_hand()
            if self.dealer.check_count() >= 17:
                playing = False
        print("-" * 45)
        print("Dealer has enough Cards")

        return givenList

    def reset_hands(self):
        """
        Resets the hands of all players and the dealer, after which it returns all AI to the attribute artificialPlayers
        """
        self.dealer.player_hand_blank()

        for player in self.listPlayers:
            player.player_hand_blank()
        self.roundTrue = False

        storage = []
        for AI in self.artificialPlayersDiscard:
            storage.append(AI)
            AI.player_hand_blank()
            self.artificialPlayersDiscard.remove(AI)
        self.artificialPlayers.extend(storage)

    def showdown(self, givenList):
        """
        Compares hands between player, AI and dealer

        :param givenList: a list of all players still playing the game
        """
        print("Dealer and players compare hands.")
        print("-" * 45)

        if self.dealer.check_count() > 21:
            self.dealer.set_dealer_false()
            print("-" * 45)
            print("The dealer went bust.")
            print("-" * 45)
            self.dealer.show_hand()
            print("-" * 45)
            for player in givenList:
                print("Player " + str(player.number) + " is paid " + str(player.pot))
                player.pay_player(False)
                print("Player " + str(player.number) + " current balance is: " + str(player.money))
            for AI in self.artificialPlayers:
                print(AI.name + " is paid.")
            self.roundTrue = False

        else:
            for player in givenList:
                print("Dealer's Hand:")
                self.dealer.show_hand()
                print("Player " + str(player.number) + "'s hand:")
                player.show_hand()
                player.check_count()
                self.dealer.check_count()

                if player.count > self.dealer.count:
                    print("Player wins by " + str(player.count - self.dealer.count) + ".")
                    player.pay_player(False)
                    print("Player's current balance is: " + str(player.money))
                elif player.count == self.dealer.count:
                    print("Player loses by tie.")
                    player.reset_pot()
                    print("Player's current balance is: " + str(player.money))
                elif player.count < self.dealer.count:
                    print("Player loses by " + str(self.dealer.count - player.count) + ".")
                    player.reset_pot()
                    print("Player's current balance is: " + str(player.money))

            for AI in self.artificialPlayers:
                print("Dealer's Hand:")
                self.dealer.show_hand()
                print(AI.name + " their hand:")
                AI.show_hand()

                if AI.check_count() > self.dealer.count:
                    print(AI.name + " wins by " + str(AI.count - self.dealer.count) + ".")
                    print(AI.name + " is paid. ")
                    if AI.leaveCounter > 0:
                        AI.leaveCounter += -1
                elif AI.check_count() == self.dealer.count:
                    print(AI.name + " loses by tie.")
                    AI.leaveCounter += 1
                elif AI.check_count() < self.dealer.count:
                    print(AI.name + " loses by " + str(self.dealer.count - AI.count) + ".")
                    AI.leaveCounter += 1

            self.roundTrue = False

    def ask_game_true(self):
        """
        Asks the user if they want to continue playing
        """
        answer = ask_game_stop()
        if answer == 1:
            self.gameTrue = False

    def show_money(self):
        """
        Prints every player's balance
        """
        print("These are the players scores")
        print("-" * 45)
        for player in self.listPlayers:
            print("Player " + str(player.number) + "'s balance: " + str(player.money))

    def check_shoe(self):
        """
        Checks the length of the card-shoe, if the card-shoe is less than half a deck of cards long it generates a new card-shoe.
        """
        if self.cardShoe.len_cardshoe() < (((len(self.listPlayers) + len(self.artificialPlayers)) * 5) + 5):
            print("The card-shoe is becoming to low to continue playing with.")
            print("We will therefore replace it, this will reset the card count.")
            print("-" * 45)
            print("Would you like the original amount of decks in the card-shoe?")
            answer = ask_yes_no()
            if answer == 0:
                self.startingDecks = ask_num_decks()
            self.cardShoe.blank_shoe()
            self.cardShoe.create_shoe(self.startingDecks)
            print("Card-shoe changed")

    def show_card_count(self):
        """
        If the boolean showCount has been set to true.
        Shows the card-count, dependent on the type of card count that has been specified.
        """
        print("-" * 45)
        print("Current card count value is:")
        if self.showCount:
            if self.typeOfCount == 2:
                print("Hi-Lo system: " + str(self.cardShoe.current_HiLo_count()))
            elif self.typeOfCount == 1:
                print("Halves system: " + str(self.cardShoe.current_Halves_count()))
            elif self.typeOfCount == 0:
                print("Zen Count system: " + str(self.cardShoe.current_Zen_count()))
            print("-" * 45)

    def ask_show_count(self):
        """
        Asks the user if they would like the card-count shown before they bet at the beginning of every round.
        """
        print("Would you like us to show you the card-count before betting every round?")
        answer = ask_yes_no()
        if answer == 1:
            self.showCount = True
        elif answer == 2:
            self.showCount = False

    def ask_show_decks(self):
        """
        Asks the player if they would like the amount of decks shown before every round.
        This is done because the amount of decks left is important to the true count, which can be used to adjust your bet size while counting cards.
        """
        print("Would you like us to show you the amount of decks left before betting every round?")
        answer = ask_yes_no()
        if answer == 1:
            self.showDecks = True
        elif answer == 0:
            self.showDecks = False

    def random_ai(self):
        """
        Generates a number between 1 and 10 with an 80 percent chance no one joins the table.
        If someone does join the table an AI is plucked from a pre-generated list with preset values determining the way they will play and how quickly they will leave.
        Then printing a random message to announce the AI has joined the table.
        """
        ran = random.randint(1, 10)
        if ran <= 8:
            print("No one new joins the table.")
        else:
            if len(self.listOfAI) > 0 and len(self.artificialPlayers) < 3:
                num = random.randint(0, len(self.listOfAI) - 1)
                AI = self.listOfAI[num]
                self.listOfAI.pop(num)
                self.artificialPlayers.append(AI)
                ran = random.randint(1, 8)
                if ran == 1:
                    print("Someone meanders around the casino floor before wandering in your direction.")
                if ran == 2:
                    print("The dealer looks up as someone wanders towards you.")
                if ran == 3:
                    print("Terry Cruise carries someone over.")
                if ran == 4:
                    print("Your phone rings...")
                    print("It's your mom...")
                    print(
                        "She tells you that she's set you up on a playdate and that they should join your game night any moment now.")
                    print("You notice someone beside you.")
                if ran == 5:
                    print("You pass out, waking up in a dark room with a new player.")
                if ran == 6:
                    print(
                        "Knowing you are not doing well, the power of a random number generator gifts you a new player.")
                if ran == 7:
                    print("Your let your thoughts wander.")
                    print("You are woken up by someone shaking your arm.")
                if ran == 8:
                    print("As you stare at an attractive person sitting at a nearby table.")
                    print(
                        "You lose focus, only waking when a new presence at the Blackjack table shakes you out of your trance.")
                print(AI.name + " has joined the table.")
            else:
                print("No one new joins the table.")

    def check_if_ai_leaves(self):
        """
        Checks if the AI players want to leave the table based upon their leaveCondition attribute.
        """
        removers = []
        for AI in self.artificialPlayers:
            answer = AI.check_leave()
            if answer:
                print("Tilted out of their mind, " + AI.name + " leaves.")
                removers.append(AI)
        for AI in removers:
            self.artificialPlayers.remove(AI)

    def ai_play(self):
        """
        Simulates all the AI playing the game and taking their turn in the round.
        This function could be expanded upon to include the player's card count,
        using it to determine if they will or won't draw more cards.
        """
        storage = []
        for AI in self.artificialPlayers:
            print(AI.name + " is playing:")
            AI.show_hand()
            playing = True
            while playing:
                answer = AI.check_next_move()
                if answer == 1:
                    print(AI.name + " stood.")
                    print("-" * 45)
                    playing = False
                elif answer == 0:
                    AI.hit(self.cardShoe)
                    print(AI.name + " hit.")
                    AI.show_hand()
                    if AI.check_count() > 21:
                        storage.append(AI)
                        print(AI.name + " went bust.")
                        print("Their money is returned.")
                        AI.leaveCounter += 1
                        playing = False

        self.artificialPlayersDiscard.extend(storage)
        for AI in storage:
            self.artificialPlayers.remove(AI)

    def ai_bet(self):
        """
        Goes through the list of AI that are currently playing and prints how much they bet.
        To be clear, the AI have no money and this is just for aesthetics.
        An observant player can however take note of how much the AI's bet varies compared to previous bets
        seeing as the AI are also keeping track of the card-count and adjusting their bets accordingly.
        Some however do this better than others.
        """
        for AI in self.artificialPlayers:
            print("-" * 45)
            print(AI.name + " bets " + str(AI.check_bet_size(self.cardShoe)))
            print("-" * 45)

    def fill_with_ai(self):
        """
        Fills the attribute listOfAI with pre-mades
        """
        self.listOfAI.append(AIPlayer("Cercei Lannister", 5, -1, 50, 5))
        self.listOfAI.append(AIPlayer("Margaery Tyrell", 5, -4, 25, 5))
        self.listOfAI.append(AIPlayer("Tyrion Lannister", 5, -2, 10, 5))
        self.listOfAI.append(AIPlayer("Tywin Lannister", 10, -2, 50, 6))
        self.listOfAI.append(AIPlayer("Joffrey Baratheon", -30, 3, 1000, 1))
        self.listOfAI.append(AIPlayer("Littlefinger", 5, -5, 10, 4))
        self.listOfAI.append(AIPlayer("Renley Baratheon", 10, -2, 420, 3))
        self.listOfAI.append(AIPlayer("Obyeryn Martell", 15, 1, 5, 3))
        self.listOfAI.append(AIPlayer("Varys", 1, -5, 10, 4))
        self.listOfAI.append(AIPlayer("John Snow", 20, 0, 1, 10))
        self.listOfAI.append(AIPlayer("Sansa Stark", -5, -1, 10, 4))

    def reset_ai(self):
        """
        Puts all ai in the artificalPlayersDiscard attribute back into the artificialPlayers attribute
        """
        self.artificialPlayers.extend(self.artificialPlayersDiscard)
        self.artificialPlayersDiscard.clear()

    def show_amount_decks(self):
        """
        Prints the amount of decks remaining rounded to one decimal point, if the boolean showDecks is set to True.
        """
        if self.showDecks:
            print("The amount of decks remaining is approximately: " + str(round(self.cardShoe.len_cardshoe() / 52, 1)))


def player_maker(numOfPlayers, money):
    """
    Used to create players with player numbers starting at 1 and ending at the given numOfPlayers along with a predetermined amount of money

    :param numOfPlayers: The amount of players that will be in the game of blackjack
    :param money: The amount of money all players start out with
    :return: a list of players made to the specifications given by the parameters
    """
    listOfPlayers = []
    for i in range(numOfPlayers):
        listOfPlayers.append(Person(money, False, (i + 1)))
    return listOfPlayers


# Underneath here are all the functions used to ask the user for input

def collect_bets(givenList):
    """
    Used to collect the bets from the players in the list givenList
    Players can choose to give no input or an incorrect input, when given an incorrect or empty input the game will let the player play with 0 as their bet.
    This is done because the goal is not to have a player win or lose money but to let them learn how to card-count.

    :param givenList: The list of players that will be betting
    """
    for players in givenList:
        print("-" * 45)
        try:
            print("How much would player " + str(players.number) + " like to bet?")
            bet = int(input("Amount:"))
            if players.money < bet:
                print("You do not have enough money to bet that much")
                print("Your current balance is: " + str(players.money))
                raise ValueError
        except ValueError:
            print("Invalid input, try again.")
            continue
        players.bet(bet)


def ask_num_decks():
    """
    Used to ask the user the amount of decks they would like used in the card-shoe (maximum of 15)
    An amount larger than three is recommended as else the card-shoe might have to be filled to soon.

    :return: the amount of decks the user specified they would like to have in the card-shoe
    """
    condition = True
    numOfDecks = 0
    while condition:
        try:
            print("Give a number between 1 and 15 to determine the amount of decks in the card shoe.")
            print("An amount larger than 3 is recommended")
            numOfDecks = int(input("Amount of decks:"))
            if numOfDecks > 15 or numOfDecks < 0:
                raise ValueError
        except ValueError:
            print("Input not correct, try again.")
            print("-" * 45)
            continue
        else:
            condition = False
    print("-" * 45)
    return numOfDecks


def ask_num_money():
    """
    Used to ask the user the amount of money all players should start the game with (maximum of 1000000)

    :return: the amount of money that all players will start the game of blackjack with
    """
    condition = True
    money = 0
    while condition:
        try:
            print("How much money do all players start out with?")
            money = int(input("Amount of money:"))
            if money > 1000000:
                print("No.")
                print("You are not allowed that much money.")
                raise ValueError
        except ValueError:
            print("Input not correct, try again.")
            print("-" * 45)
            continue
        else:
            condition = False
    print("-" * 45)
    return money


def ask_num_players():
    """
    Used to ask the user for the amount of players that will participate in the game (maximum of five)

    :return: The number of players that will be starting the game of blackjack
    """
    condition = True
    numOfPlayers = 0
    while condition:
        try:
            print("Give a number between 1 and 5 to determine the amount of players.")
            numOfPlayers = int(input("Amount of players:"))
            if numOfPlayers > 5 or numOfPlayers < 0:
                raise ValueError
        except ValueError:
            print("Input not correct, try again.")
            print("-" * 45)
            continue
        else:
            condition = False
    print("-" * 45)
    return numOfPlayers


def ask_player_move():
    """
    Used to ask a player what their next move will be in the action_time function in class Game

    :return: 2 if the player would like to have the card-count returned to them, 1 if they would like to stand 0 if they would like to hit
    """
    condition = True
    while condition:
        try:
            print("Would you like to Stand or Hit?")
            print("To get the current card-count type count.")
            answer = input("Answer: ")
            if answer.upper() == "COUNT":
                answer = 2
            elif answer.upper() == "STAND":
                answer = 1
            elif answer.upper() == "HIT":
                answer = 0
            else:
                raise ValueError
        except ValueError:
            print("Input not viable, try again.")
            print("-" * 45)
            continue
        else:
            condition = False
        print("-" * 45)
        return answer


def ask_game_stop():
    """
    Used to ask a player if they would like to stop the game in its entirety

    :return: 1 if they would like to stop the game entirely, 0 if they would not like to stop the game entirely
    """
    print("Would you like to end the game?")
    return ask_yes_no()


def ask_count_type():
    """
    Used to ask the user what card-counting method should be used, gives the choice of Hi-Lo, Halves and Zen count

    :return: 2 for Hi-Lo card counting system, 1 for the Halves card counting system and 0 for the Zen count card-counting system
    """
    condition = True
    while condition:
        try:
            print("What type of card counting would you like to use?")
            print("You have the choice of Hi-lo, Halves and Zen Count.")
            print("The commands for which are, Hi, Half and Zen respectively.")
            answer = input("Answer: ")
            if answer.upper() == "HI":
                answer = 2
            elif answer.upper() == "HALF":
                answer = 1
            elif answer.upper() == "ZEN":
                answer = 0
            else:
                raise ValueError
        except ValueError:
            print("Input not viable, try again.")
            print("-" * 45)
            continue
        else:
            condition = False
        print("-" * 45)
        return answer


def ask_yes_no():
    """
    Asks a yes or no question. Gives back 1 for yes and 2 for no.
    This function does not use booleans for the reason that it is easier to change if you use integers instead.
    Adding things like, 'Stop Game' if the developer feels like it down the line.
    """
    condition = True
    while condition:
        try:
            print("Answer Yes or No.")
            answer = input("Answer: ")
            if answer.upper() == "YES":
                answer = 1
            elif answer.upper() == "NO":
                answer = 0
            else:
                raise ValueError
        except ValueError:
            print("Input not viable, try again.")
            print("-" * 45)
            continue
        else:
            condition = False
        print("-" * 45)
    return answer


if __name__ == '__main__':
    blackjack = Game()
    blackjack.start_game()
