

from mitigation_action.models import MitigationAction
from mitigation_action.workflow.states import States
from .workflow import WorkFlow as MitigationActionWorkflow

class MitigationActionWorkflowStep:
    
    workflow_state = MitigationActionWorkflow

    def update_fsm_state(self, record: MitigationAction ,new_state: States):
        print(f'The mitigation action is transitioning from <{record.fsm_state}> to <{new_state}>')