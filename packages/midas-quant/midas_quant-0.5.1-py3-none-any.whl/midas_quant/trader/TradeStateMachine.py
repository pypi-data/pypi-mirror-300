from transitions.extensions import GraphMachine
from io import BytesIO
from IPython.display import Image, display


class TradeStateMachine:
    def __init__(self, transitions=None, initial_state=None) -> None:
        """
        Initialize the TradeStateMachine with optional transitions and an initial state.
        
        Args:
            transitions (list, optional): A list of transition dictionaries.
            initial_state (str, optional): The initial state of the state machine.
        """
        if transitions is not None and initial_state is not None:
            self.setTransitions(transitions, initial_state)

    def setTransitions(self, transitions, initial_state) -> None:
        """
        Define the transitions and initialize the state machine.
        
        Args:
            transitions (list): A list of transition dictionaries.
            initial_state (str): The initial state of the state machine.
        """
        states = set()
        for transition in transitions:
            states.add(transition["source"])
            states.add(transition["dest"])

        self._states = list(sorted(states))
        self._transitions = transitions
        self._machine = GraphMachine(
            model=self,
            states=self._states,
            transitions=self._transitions,
            initial=initial_state,
            ignore_invalid_triggers=True
        )

    def getStates(self) -> list:
        """
        Get the list of states in the state machine.
        
        Returns:
            list: A list of state names.
        """
        return self._states

    def getTransitions(self) -> list:
        """
        Get the list of transitions in the state machine.
        
        Returns:
            list: A list of transition dictionaries.
        """
        return self._transitions

    def graph(self) -> Image:
        """
        Generate a graphical representation of the state machine.
        
        Returns:
            Image: An image of the state machine graph.
        """
        graph = self._machine.get_graph()
        buf = BytesIO()
        graph.draw(buf, format='png', prog='dot')
        buf.seek(0)
        
        return Image(buf.read())
