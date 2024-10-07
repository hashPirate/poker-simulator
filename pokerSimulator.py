import random
from treys import Card, Evaluator, Deck
from multiprocessing import Pool, cpu_count
import time

# Incredibly fast pooled poker simulator. 5 million trials in under a minute. Future plans include speed calculation and perhaps training a model on this data as well.

class PokerSimulator:
    def __init__(self, num_players): #initializing poker class and stating evaluator to evaluate the poker hands.
        self.num_players = num_players
        self.evaluator = Evaluator()
        self.results = []

    def simulate_hand(self, trial_number):

        deck = Deck() # i love treys it makes this so simple
        deck.shuffle()
        initialCards = {i: [deck.draw(1)[0], deck.draw(1)[0]] for i in range(1, self.num_players + 1)} #best way to draw 2 cards for the number of players

        #deal all the community cards
        deck.draw(1) #burning the cards per deal
        flop = [deck.draw(1)[0], deck.draw(1)[0], deck.draw(1)[0]]
        deck.draw(1)  
        turn = deck.draw(1)[0]
        deck.draw(1)  
        river = deck.draw(1)[0]
        community_cards = flop+[turn,river]

        scores = {player: self.evaluator.evaluate(community_cards,initialCards[player]) for player in range(1, self.num_players + 1)} # We can easily evaluate each players hand this way!! the lower the score the better
        winner = min(scores,key=scores.get) #grabbing minscore
        currentResult='Loss'
        if(winner==1): currentResult='Win'
        winHand = None
        if(winner!=1):
            winHand = initialCards[winner]
        result = { #simple dict containing trial, hand, cards, result and the winner
            'trialNum': trial_number,
            'yourHand': initialCards[1],
            'communityCards': community_cards,
            'result': currentResult,
            'winningHand': winHand
        }

        return result

    def save_results(self, results, filename='pokersim.txt'):
        cards = {}
        def cardToStr(cardInt):
            if not(cardInt in cards):
                cards[cardInt] = Card.int_to_pretty_str(cardInt)
            return cards[cardInt]
        outputLines = []
        for result in results:
            trialNum = result['trialNum']
            yourHand = ', '.join(cardToStr(card) for card in result['yourHand']) # added cards in hand sep=comma
            communityCards = ', '.join(cardToStr(card) for card in result['communityCards'])
            outputLines.append(f"Trial {trialNum}:\n")
            outputLines.append(f"Your hand: {yourHand}\n")
            outputLines.append(f"Community Cards: {communityCards}\n")
            outputLines.append(f"Result: {result['result']}\n")
            if result['result'] == 'Loss':
                winning_hand = ', '.join(cardToStr(card) for card in result['winningHand'])
                outputLines.append(f"Lost to hand: {winning_hand}\n")
            outputLines.append("\n")

        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(outputLines) #used writelines instead for faster output
        print(f"Results saved to {filename}")


def run_simulation(inputList):
    simulator, trialNumber = inputList
    return simulator.simulate_hand(trialNumber)

if __name__ == "__main__":
    numPlayers = int(input("Enter the number of players (including you): "))
    numSimulations = int(input("Enter the number of simulations: "))  #number of hands to simulate
    startTime = time.time()
    pokerSim = PokerSimulator(numPlayers) # we reached this statement beware 
    numProcesses = cpu_count()
    print(f"Using {numProcesses} CPU cores for simulation.")

    with Pool(processes=numProcesses) as pool: #thread pool to run processes at the same time
        args = [(pokerSim, trial + 1) for trial in range(numSimulations)]
        results = pool.map(run_simulation, args)

    finalTime = time.time()
    print(f"Simulation completed in {finalTime-startTime:.2f} seconds.")
    pokerSim.save_results(results)
