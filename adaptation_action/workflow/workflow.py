from typing import Any
from viewflow import fsm

from general.services import EmailServices
from adaptation_action.email_services import AdaptationActionEmailServices
from .states import States
from adaptation_action.models import AdaptationAction

class WorkFlow:

    state = fsm.State(States, default=States.NEW)

    def __init__(self, obj: AdaptationAction):
        self.obj = obj

    @state.getter()
    def _get_state(self):
        return self.obj.fsm_state

    @state.setter()
    def _set_state(self, value):
        print(f'Changing state from <{self.obj.fsm_state}> to <{value}>')
        self.obj.fsm_state = value
    
    @state.on_success()
    def _on_success_transition(self, descriptor: Any, source: States, target: States) -> None:
        print(f'The adaptation action is saved with state <{target}>')
        self.obj.save()

    @state.transition(source=(States.NEW, States.UPDATING_BY_REQUEST_DCC), target=States.SUBMITTED, permission=None)
    def submit(self, user_approver):
        # new --> submitted        
        # send email to user that submitted the action
        print(f'The adaptation action is transitioning from <{self.state}> to <submitted>')
        _email_service = AdaptationActionEmailServices(EmailServices())

        email_function = {
            States.NEW: _email_service.notify_dcc_responsible_adaptation_action_submission,
            States.UPDATING_BY_REQUEST_DCC: _email_service.notify_contact_responsible_adaptation_action_update
        }

        email_status, email_data = email_function.get(self.fsm_state)(self.obj, user_approver)
        if email_status:
            return email_status, email_data
        else:
            ...
            ## maybe raise exception

    
    @state.transition(source=(States.SUBMITTED), target=States.IN_EVALUATION_BY_DCC, permission=None)
    def evaluate_by_DCC(self, user_approver):
        # submitted --> in_evaluation_by_DCC
        # send email to user that submitted the action
        print('The adaptation action is transitioning from <submitted> to <in_evaluation_by_DCC>')
        _email_service = AdaptationActionEmailServices(EmailServices())

        email_status, email_data = _email_service.notify_contact_responsible_adaptation_action_evaluation_by_dcc(self.obj, user_approver)
        print(email_status, email_data)
        if email_status:
            return email_status, email_data
        else:
            ...
            ## maybe raise exception

    ##
    ## rejected_by_DCC, requested_changes_by_DCC, accepted_by_DCC
    ##
    @state.transition(source=(States.IN_EVALUATION_BY_DCC), target=States.REJECTED_BY_DCC, permission=None)
    def evaluate_by_DCC_rejected(self, user_approver):
        # in_evaluation_by_DCC --> rejected_by_DCC
        # send email to user that submitted the action
        print('The adaptation action is transitioning from <in_evaluation_by_DCC> to <rejected_by_DCC>')
        _email_service = AdaptationActionEmailServices(EmailServices())

        email_status, email_data = _email_service.notify_contact_responsible_adaptation_action_rejection(self.obj, user_approver)
        if email_status:
            return email_status, email_data
        else:
            ...
            ## maybe raise exception
    
    @state.transition(source=(States.IN_EVALUATION_BY_DCC), target=States.REQUESTED_CHANGES_BY_DCC, permission=None)
    def evaluate_by_DCC_requested_changes(self, user_approver):
        # in_evaluation_by_DCC --> requested_changes_by_DCC
        # send email to user that submitted the action
        print('The adaptation action is transitioning from <in_evaluation_by_DCC> to <requested_changes_by_DCC>')
        _email_service = AdaptationActionEmailServices(EmailServices())

        email_status, email_data = _email_service.notify_contact_responsible_adaptation_action_requested_changes(self.obj, user_approver)
        if email_status:
            return email_status, email_data
        else:
            ...
    
    @state.transition(source=(States.IN_EVALUATION_BY_DCC), target=States.ACCEPTED_BY_DCC, permission=None)
    def evaluate_by_DCC_accepted(self, user_approver):
        # in_evaluation_by_DCC --> accepted_by_DCC
        # send email to user that submitted the action
        print('The adaptation action is transitioning from <in_evaluation_by_DCC> to <accepted_by_DCC>')
        _email_service = AdaptationActionEmailServices(EmailServices())

        email_status, email_data = _email_service.notify_contact_responsible_adaptation_action_approval(self.obj, user_approver)
        if email_status:
            return email_status, email_data
        else:
            ...
            ## maybe raise exception
    
    ## rejected by DCC to end
    @state.transition(source=(States.REJECTED_BY_DCC), target=States.END, permission=None)
    def rejected_by_DCC_to_end(self, user_approver):
        # rejected_by_DCC --> rejected_by_DCC
        # send email to user that submitted the action
        print('The adaptation action is transitioning from <rejected_by_DCC> to <end>')
        ...
    
    @state.transition(source=(States.REQUESTED_CHANGES_BY_DCC), target=States.UPDATING_BY_REQUEST_DCC, permission=None)
    def update_by_DCC_request(self, user_approver):
        # requested_changes_by_DCC --> updating_by_request_DCC
        # send email to user that submitted the action
        _email_service = AdaptationActionEmailServices(EmailServices())
        email_status, email_data = _email_service.notify_contact_responsible_adaptation_action_update(self.obj, user_approver)
        if email_status:
            return email_status, email_data
        else:
            ...
        
    ## accepted_by_DCC to	registered_by_DCC
    @state.transition(source=(States.ACCEPTED_BY_DCC), target=States.REGISTERED_BY_DCC, permission=None)
    def registered_by_DCC(self,user_approver):
        # accepted_by_DCC --> registered_by_DCC
        # send email to user that submitted the action
        print('The adaptation action is transitioning from <accepted_by_DCC> to <registered_by_DCC>')
        ...


