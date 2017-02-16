import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
import pprint

class QLearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(QLearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.reward = 0
	self.next_waypoint = None
        self.success = []
        self.qTable = dict() 

	self.alpha = 0.9 # learning rate
	self.epsilon = 0.05 # probability of flipping the coin
	self.gamma = 0.2 #discount factor
	
	self.state = None
	self.next_state = None
        self.reward = None
	self.action = None										
        self.t = None
	self.total_reward = None

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.state = None
	self.next_waypoint = None
        self.next_state = None
	self.list_actions = Environment.valid_actions
        self.action = None
	self.t = 0
	self.total_reward=0
	    
    def getQvalue(self, state, action):
    	key = (state, action)	
	return self.qTable.get(key, 12.0)

    def getMaxQvalue(self, state):
	q = [self.getQvalue(state, a) for a in self.list_actions]
	return max(q)

    def QLearn(self, state, action, nextState, reward):
    	key = (state, action)
	if (key not in self.qTable):
		# initialize the q values
	        self.qTable[key] = 12.0
	else:
		self.qTable[key] = self.qTable[key] + self.alpha * (reward + self.gamma*self.getMaxQvalue(nextState) - self.qTable[key])
    
    def next_action(self, state):
    	#Greedy epsilon approach for picking next action
	
	if random.random() < self.epsilon: 
	#choose randomly
		action = random.choice(self.list_actions)
	        print "random action"
	else: 
	#choose based on q value
	        print "greedy action"
		q = [self.getQvalue(state, a) for a in self.list_actions]
	        max_q = max(q)
	        
	        if q.count(max_q) > 1: 
	        # pick randomly
		        next_actions = [i for i in range(len(self.list_actions)) if q[i] == max_q]                       
		        action_index = random.choice(next_actions)
                else:
	                action_index = q.index(max_q)
		action = self.list_actions[action_index]
	return action
    	


    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        print "self.next_waypoint {}".format(self.next_waypoint)
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
         

        # TODO: Update state
        self.next_state = inputs

       	self.next_state['next_waypoint'] = self.next_waypoint
	self.next_state = tuple(sorted(self.next_state.items()))
        
        # TODO: Select action according to your policy
        action = self.next_action(self.next_state)


        # Execute action and get reward
        next_reward = self.env.act(self, action)
        
        #Update Q table 
       
        self.QLearn(self.state, self.action, self.next_state, self.reward)

        self.state =  self.next_state
	self.action = action
	self.reward = next_reward
	self.t = self.t+1
	self.total_reward=self.total_reward+self.reward
	

        # TODO: Learn policy based on state, action, reward

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, next_reward)  # [debug]

        location = self.env.agent_states[self]["location"] 
	#print "location = {}".format(location)
	
	destination = self.env.agent_states[self]["destination"]
	#print "destination = {}".format(destination)

	if location==destination:
		self.success.append(1)	
                print "total time steps {}".format(self.t)

		print "total rewards {}".format(self.total_reward)
        
        	print "success rate {}".format(self.success.count(1))

                print "Final Q table {}"

                pp = pprint.PrettyPrinter(indent=4)
                pp.pprint(self.qTable) 



def run():
    """Run the agent for a finite number of trials."""
    
    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(QLearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
