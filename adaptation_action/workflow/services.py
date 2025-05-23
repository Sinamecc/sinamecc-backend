

from django.contrib.auth.models import AbstractUser
from viewflow.fsm import Transition

from adaptation_action.models import AdaptationAction, ChangeLog

from .states import States
from .workflow import WorkFlow as AdaptationActionWorkflow


class AdaptationActionWorkflowStep:
    
    def __init__(self, adaptation_action: AdaptationAction):
        self.workflow_state = AdaptationActionWorkflow(adaptation_action)
    
    def _get_available_transitions(self, user: type[AbstractUser]) -> dict[States, Transition]:
        """
        Retrieve available transitions for the current workflow state and user.

        Args:
            user (type[AbstractUser]): The user for whom to retrieve available transitions.

        Returns:
            dict[States, Transition]: A dictionary mapping target states to their corresponding transitions.
        """
        obj = self.workflow_state.obj
        state = self.workflow_state.state

        transition_list = AdaptationActionWorkflow.state.get_available_transitions(obj, state, user)

        return {transition.target: transition for transition in transition_list}
    
    def get_next_states(self) -> list[States]:
        """
        Retrieve the next possible states for the current workflow state.

        Returns:
            list[States]: A list of possible next states.
        """

        obj = self.workflow_state.obj

        transition_list = AdaptationActionWorkflow.state.get_outgoing_transitions(obj.fsm_state)

        return [
            transition.target
            for transition in transition_list
        ]


    def update_fsm_state(self, next_state: States, user: type[AbstractUser]) -> None:
        """
        Update the FSM state of the mitigation action

        Args:
            next_state (States): The state to transition to.
            user (type[AbstractUser]): The user performing the transition.

        Returns:
            None
        """
        transition_dict = self._get_available_transitions(user)

        if next_state not in transition_dict:
            raise ValueError(f'Invalid transition to state <{next_state}>')
        
        transition = transition_dict[next_state]
        transition_function = getattr(self.workflow_state, transition.func.__name__)
        
        previous_state = self.workflow_state.state

        print(f"Transitioning from {self.workflow_state.state} to {next_state} using {transition.func.__name__}")
        transition_function(user)

        self._add_changelog(
            user=user,
            adapt_action_id=self.workflow_state.obj.id,
            previous_state=previous_state,
            current_state=next_state
        )
        ## Here we need to add an error handling mechanism to handle the case where the transition fails

        return True, None
    
    def _add_changelog(self, 
        user: type[AbstractUser],
        adapt_action_id: str,
        previous_state: States,
        current_state: States,) -> None:
        """
        Add a new changelog entry to the adaptation action

        Args:
            user (type[AbstractUser]): The user adding the changelog entry.
            comment (str): The comment to add to the changelog.

        Returns:
            None
        """
        print(f'Adding changelog entry for adaptation action {adapt_action_id}')
        print(f'Previous state: {previous_state}', f'Current state: {current_state}')
        change_log_obj = ChangeLog.objects.create(
            user=user,
            adaptation_action_id=adapt_action_id,
            previous_status=previous_state,
            current_status=current_state
        )
