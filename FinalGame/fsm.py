"""
Finite State Machine

@author: Dorothy Zhang
@version: 2023
courtesy of MangoGame 
"""


class FSM:
    def __init__(self, initial_state):
        # Dictionary (input_symbol, current_state) --> (action, next_state).
        self.state_transitions = {}
        self.current_state = initial_state

    def add_transition(self, input_symbol, state, action=None, next_state=None):
        """
        Adds a transition to the instance variable state_transitions
        that associates: (input_symbol, current_state) --> (action, next_state)

        """
        # if there is an input and state, we will do another action and set to the next state
        if next_state == None:
            self.state_transitions[(input_symbol, state)] = (action, state)
        else:
            self.state_transitions[(input_symbol, state)] = (action, next_state)

    def get_transition(self, input_symbol, state):
       
        # Returns tuple (action, next state) given an input_symbol and state.

        return self.state_transitions[(input_symbol, state)]

    def process(self, input_symbol):
        """
        Main method to process input.
        Finds the action and next_state associated with the input_symbol and current_state.

        """

        action_state = self.get_transition(input_symbol, self.current_state)
        # if the action is None, then only the current state is changed
        if action_state[0] == None:
            self.current_state = action_state[1]
        # for all others, change the state and call an action
        else:
            self.current_state = action_state[1]
            action_state[0]()
