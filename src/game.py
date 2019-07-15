
class Game(object):

    def __init__(self, params, gameName = '', runs = 300):
        self.params = params
        self.MAX_RUNS = runs
        self.name = gameName
        
    def set_strategy(self, strategy):
        strategy.set_params(self.params)
        self.strategy = strategy
	
    def run(self):
        S = self.params.get_states()
        T = self.params.get_transitions()

        V = self.strategy.initilize_V() 

        for k in range(self.MAX_RUNS+1):
            Q = self.strategy.update_Q(T, V)
           
            # Update Value function
            V_new = {}
            pi = {}
            for s in S:
                V_new[s], pi[s] = self.strategy.get_value(s, T[s], Q)
            V = V_new
            
        return (V, pi)

   