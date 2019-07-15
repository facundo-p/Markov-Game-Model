
import matplotlib.pyplot as plt
from collections import defaultdict
from game import Game
#from parameters4 import Parameters as p
from parametersExample import Parameters as pExample
from paramsCaseStudy import Parameters as pCaseStudy
from strategy import *


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))
    
def plot_states(gammas, values, states, strategies, gameName = ''):
    lines = ['ro:', 'bo-', 'go--']
    titles = ['S3', 'S0', 'S1', 'S2']
    for state in states:
        i = 0
        for strategy in strategies:
            #print('State {} - Strat {}: {}'.format(state, strategy, values[state][strategy]))
            plt.plot(gammas, values[state][strategy], lines[i])
            i+=1
        plt.title('State {}'.format(titles[state]))
        plt.xlabel("Gamma")
        plt.ylabel("Defender´s utility")
        plt.savefig('{}_state{}_values.png'.format(gameName, titles[state]))
        plt.show()
        #print()
         
def print_iteration_info(gamma, strategyName, k, V, pi):
    print ('---------------')
    print('Discount Factor: {}'.format(gamma))
    print('Strategy: {}'.format(strategyName))
    print("Itreation -- {}".format(k))
    print ('---------------')
    for s in range(len(V)):
        print("V({})  : {}".format(s, V[s]))
        print("pi({}) : {}".format(s, pi[s]))
    print()
        
def simulate(game, strategies):
    gammas = []
    strategyNames = []
    values = nested_dict(2, list)
    
    for gamma in range(50, 85, 5):
        gammas.append(gamma/100.0)
        
    for strategy in strategies:     
        strategyNames.append(strategy.get_name())
        game.set_strategy(strategy)
        
        for gamma in gammas:
            game.strategy.set_gamma(gamma) 
            V, pi = game.run()
            print_iteration_info(gamma, strategy.get_name(), game.MAX_RUNS, V, pi)
            for state in V.keys():
                values[state][game.strategy.get_name()].append(V[state])
                
    plot_states(gammas, values, game.params.get_states(), strategyNames, game.name)
                

strategies = [MaxMinPure(), UniformRandom(), OptimalMixed()]
game = Game(pExample(), 'example')
simulate(game, strategies)

strategies = [UniformRandom(), OptimalMixed()]
game = Game(pCaseStudy(), 'caseStudy')
#simulate(game, strategies)