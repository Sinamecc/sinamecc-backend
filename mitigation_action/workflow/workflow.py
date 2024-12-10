from viewflow import fsm
from .states import States
from ..models import MitigationAction
from django.contrib.auth import get_user_model


class WorkFlow:

    state = fsm.State(States, default=States.NEW)

    def __init__(self, obj: MitigationAction):
        self.obj = obj
    
    @state.getter
    def _get_state(self):
        return self.obj.fsm_state


    @state.setter
    def _set_state(self, value):
        self.obj.fsm_state = value
        

    @state.transition(source=(States.NEW, States.UPDATING_BY_REQUEST_DCC), target=States.SUBMITTED)
    def submit(self, user_approver):
        # new --> submitted        
        # send email to user that submitted the action
        print(f'The mitigation action is transitioning from <{self.fsm_state}> to <submitted>')
        email_function = {
            States.NEW: self.email_service.notify_dcc_responsible_mitigation_action_submission,
            States.UPDATING_BY_REQUEST_DCC: self.email_service.notify_dcc_responsible_mitigation_action_update,
        }

        email_status, email_data = email_function.get(self.fsm_state)(self, user_approver)
        if email_status:
            return email_status, email_data
        else:
            ...
            ## maybe raise exception

    
    @state.transition(source=(States.SUBMITTED), target=States.IN_EVALUATION_BY_DCC)
    def evaluate_by_DCC(self, user_approver):
        # submitted --> in_evaluation_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <submitted> to <in_evaluation_by_DCC>')

        email_status, email_data = self.email_service.notify_contact_responsible_mitigation_action_evaluation_by_dcc(self)
        if email_status:
            return email_status, email_data
        else:
            ...
            ## maybe raise exception

    ##
    ## rejected_by_DCC, requested_changes_by_DCC, accepted_by_DCC
    ##
    @state.transition(source=(States.IN_EVALUATION_BY_DCC), target=States.REJECTED_BY_DCC)
    def evaluate_by_DCC_rejected(self, user_approver):
        # in_evaluation_by_DCC --> rejected_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <in_evaluation_by_DCC> to <rejected_by_DCC>')
        email_status, email_data = self.email_service.notify_contact_responsible_mitigation_action_rejection(self)
        if email_status:
            return email_status, email_data
        else:
            ...
            ## maybe raise exception
    
    @state.transition(source=(States.IN_EVALUATION_BY_DCC), target=States.REQUESTED_CHANGES_BY_DCC)
    def evaluate_by_DCC_requested_changes(self, user_approver):
        # in_evaluation_by_DCC --> requested_changes_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <in_evaluation_by_DCC> to <requested_changes_by_DCC>')
        email_status, email_data = self.email_service.notify_dcc_responsible_mitigation_action_request_changes(self)
        if email_status:
            return email_status, email_data
        else:
            ...
    
    @state.transition(source=(States.IN_EVALUATION_BY_DCC), target=States.ACCEPTED_BY_DCC)
    def evaluate_by_DCC_accepted(self, user_approver):
        # in_evaluation_by_DCC --> accepted_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <in_evaluation_by_DCC> to <accepted_by_DCC>')
        email_status, email_data = self.email_service.notify_contact_responsible_mitigation_action_approval(self)
        if email_status:
            return email_status, email_data
        else:
            ...
            ## maybe raise exception
    
    ## rejected by DCC to end
    @state.transition(source=(States.REJECTED_BY_DCC), target=States.END)
    def rejected_by_DCC_to_end(self, user_approver):
        # rejected_by_DCC --> rejected_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <rejected_by_DCC> to <end>')
        ...
    
    @state.transition(source=(States.REQUESTED_CHANGES_BY_DCC), target=States.UPDATING_BY_REQUEST_DCC)
    def update_by_DCC_request(self, user_approver):
        # requested_changes_by_DCC --> updating_by_request_DCC
        # send email to user that submitted the action
        email_status, email_data = self.email_service.notify_dcc_responsible_mitigation_action_update(self, user_approver)
        if email_status:
            return email_status, email_data
        else:
            ...
        
    ## accepted_by_DCC to	registered_by_DCC
    @state.transition(source=(States.ACCEPTED_BY_DCC), target=States.REGISTERED_BY_DCC)
    def registered_by_DCC(self,user_approver):
        # accepted_by_DCC --> registered_by_DCC
        # send email to user that submitted the action
        print('The mitigation action is transitioning from <accepted_by_DCC> to <registered_by_DCC>')
        ...
