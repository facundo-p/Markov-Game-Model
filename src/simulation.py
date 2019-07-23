
import matplotlib.pyplot as plt
from collections import defaultdict
from game import Game
from parametersExample import Parameters as pExample
from paramsCaseStudy import Parameters as pCaseStudy
from strategy import *


def nested_dict(n, type):
    if n == 1:
        return defaultdict(type)
    else:
        return defaultdict(lambda: nested_dict(n-1, type))
    
def plot_states(gammas, values, states, strategies, gameName = ''):
    styles = ['ro:', 'bo-', 'go--']
    titles = ['S3', 'S0', 'S1', 'S2']
    lines = []
    for state in states:
        i = 0
        for strategy in strategies:
            line, = plt.plot(gammas, values[state][strategy], styles[i], label=strategy)
            lines.append(line)
            i+=1
        plt.title('State {}'.format(titles[state]))
        plt.legend(handles=lines)
        plt.xlabel("Gamma")
        plt.ylabel("Defender´s utility")
        plt.savefig('../img/{}_state{}_values.png'.format(gameName, titles[state]))
        plt.show()
        lines = []
         
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
simulate(game, strategies)
