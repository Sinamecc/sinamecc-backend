

from mitigation_action.models import MitigationAction, ChangeLog
from .states import States
from .workflow import WorkFlow as MitigationActionWorkflow
from django.contrib.auth.models import AbstractUser
from viewflow.fsm import Transition
class MitigationActionWorkflowStep:
    
    workflow_state: MitigationActionWorkflow

    def __init__(self, mitigation_action: MitigationAction):
        self.workflow_state = MitigationActionWorkflow(mitigation_action)
    
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

        transition_list = MitigationActionWorkflow.state.get_available_transitions(obj, state, user)

        return {transition.target: transition for transition in transition_list}
    
    def get_next_states(self) -> list[States]:
        """
        Retrieve the next possible states for the current workflow state.

        Returns:
            list[States]: A list of possible next states.
        """

        obj = self.workflow_state.obj

        transition_list = MitigationActionWorkflow.state.get_outgoing_transitions(obj.fsm_state)

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

        self._add_change_log(
            user=user,
            mitigation_action_id=self.workflow_state.obj.id,
            previous_state=previous_state,
            current_state=next_state
        )
        ## Here we need to add an error handling mechanism to handle the case where the transition fails

        return True, None
    
    def _add_change_log(self,
        user: type[AbstractUser],
        mitigation_action_id: str,
        previous_state: States,
        current_state: States,
        ) -> None:
        """
        Add a change log entry for the state transition.

        Args:
            user (type[AbstractUser]): The user performing the transition.
            mitigation_action_id (str): The ID of the mitigation action.
            previous_state (States): The previous state.
            current_state (States): The current state.

        Returns:
            None
        """

        change_log_obj = ChangeLog.objects.create(
            user=user,
            mitigation_action_id=mitigation_action_id,
            previous_state=previous_state,
            current_state=current_state
        )