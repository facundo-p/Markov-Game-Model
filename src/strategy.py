import importlib
import numpy as np

class Strategy(object):

    def __init__ (self, gamma = 0.5):
        self.DISCOUNT_FACTOR = gamma
        self.lib = importlib.import_module('gurobi')
        
    def set_params(self, params):
        self.states = params.get_states()
        self.deffenderActions = params.get_actions(1) ## Defender Action Set
        self.attackerActions = params.get_actions(0) ## Attacker Action Set
        self.rewards = params.get_rewards()
	
    def set_gamma(self, discountFactor):
        self.DISCOUNT_FACTOR = discountFactor

    def initilize_V(self):
        V = {}
        for s in self.states:
            V[s] = 0
        return V

    def update_Q(self, T, V):
        S 	= self.states
        A1 	= self.deffenderActions
        A2 	= self.attackerActions
        R	= self.rewards
        Q 	= {}
        # Update the Q values for each state
        for s in S:
            for d in range(len(A1[s])):
                for a in range(len(A2[s])):
                    sda = '{}_{}_{}'.format(s, A1[s][d], A2[s][a])
                    Q[sda] = R[s][a][d]
                    for s_new in S:
                        Q[sda] += T[s][a][d][s_new] * self.DISCOUNT_FACTOR * V[s_new]
        return Q

    '''
    Given the new Q values, updates the optimal values for each state.
    Each strategy type defines the implementation of this method.
    '''
    def get_value(self, s, T, Q):
       raise NotImplementedError
       
    def get_name(self):
       raise NotImplementedError
	   
	   
class MaxMinPure(Strategy):
    
    def get_name(self):
        return 'MMP'
    
    def get_value(self, s, T, Q):
        A1 = self.deffenderActions[s]
        A2 = self.attackerActions[s]
        num_d = len(A1)
        num_a = len(A2)

        def_options = []
        policy = {}
        for d in range(num_d):
            def_options.append(
                min(
                    [Q['{}_{}_{}'.format(s, A1[d], A2[a])] for a in range(num_a)]
                )
            )
            policy[A1[d]] = 0.0

        value = max(def_options)
        policy[A1[np.argmax(def_options)]] = 1.0

        return (float(value), policy)


class UniformRandom(Strategy):
    
    def get_name(self):
        return 'URS'
    
    def get_value(self, s, T, Q):
        A1 = self.deffenderActions[s]
        A2 = self.attackerActions[s]
        num_d = len(A1)
        num_a = len(A2)

        p = 1.0/num_d
        policy = {}
        for d in range(num_d):
            policy[A1[d]] = p

        min_v = +100000
        for a in range(num_a):
            v = 0
            for d in range(num_d):
                v += p * Q['{}_{}_{}'.format(s, A1[d], A2[a])]
            min_v = min(min_v, v)

        return(float(min_v), policy)


class OptimalMixed(Strategy):
    
    def get_name(self):
        return 'OPT'
    
    def get_value(self, s, T, Q):
        A1 = self.deffenderActions[s]
        A2 = self.attackerActions[s]
        num_d = len(A1)
        num_a = len(A2)

        # Solve a optimization problem with Gurobi to find:
        # (1) The optimal value of the state (and update it)
        # (2) The optimal mixed strategy in the state
        m = self.lib.Model('LP')
        m.setParam('OutputFlag', 0)
        m.setParam('LogFile', '')
        m.setParam('LogToConsole', 0)
        v = m.addVar(name='v', vtype=self.lib.GRB.CONTINUOUS, lb=-1*self.lib.GRB.INFINITY)
        pi = {}
        for d in range(num_d):
            pi[d] = m.addVar(lb=0.0, ub=1.0, name='pi_{}'.format(A1[d]))
        m.update()
        for a in range(num_a):
            m.addConstr(
                self.lib.quicksum(pi[d] * Q['{}_{}_{}'.format(s, A1[d], A2[a])] for d in range(num_d)) >= v,
                name='c_ai_{}'.format(A2[a]))
        m.addConstr(self.lib.quicksum(pi[d] for d in range(num_d)) == 1, name='c_pi')
        m.setParam('DualReductions', 0)
        m.setObjective(v, sense=self.lib.GRB.MAXIMIZE)
        m.optimize()

        policy = {}
        for var in m.getVars():
            if 'pi_' in var.varName:
                policy[var.varName] = float(var.x)

        return (float(m.ObjVal), policy)

