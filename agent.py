from __future__ import division
import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.reward = 0
	self.next_waypoint = None
        self.success = []

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.state = None
	self.next_waypoint = None
                

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
         

        # TODO: Update state
        #self.state = (self.next_waypoint, inputs['light'])
        self.state = inputs
	self.state['next_waypoint'] = self.next_waypoint
	self.state = tuple(sorted(self.state.items()))

        print self.state
        # TODO: Select action according to your policy
        action = random.choice(Environment.valid_actions)


        # Execute action and get reward
        reward = self.env.act(self, action)
        #self.reward = self.reward + reward


        # TODO: Learn policy based on state, action, reward

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]

        location = self.env.agent_states[self]["location"] 
	print "location = {}".format(location)
	
	destination = self.env.agent_states[self]["destination"]
	print "destination = {}".format(destination)

	if location==destination:
		self.success.append(1)	
              

def run():
    """Run the agent for a finite number of trials."""
    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.001, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line
    
    print "success rate {}%".format((a.success.count(1)/100)*100)

if __name__ == '__main__':
    run()
