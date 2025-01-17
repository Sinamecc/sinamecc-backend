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
        print(f'Getting state <{self.obj.fsm_state}>')
        return self.obj.fsm_state

    @state.setter()
    def _set_state(self, value: States):
        print(f'Changing state from <{self.obj.fsm_state}> to <{value}>')
        # set the new state
        self.obj.fsm_state = value
    
    @state.on_success()
    def _on_success_transition(self, descriptor: Any, source: States, target: States) -> None:
        print(f'The adaptation action is saved with state <{target}>')
        self.obj.save()

    @state.transition(source=(States.NEW), target=States.SUBMITTED, permission=None)
    def submit_new_record(self, user_approver):
        # new --> submitted        
        # send email to user that submitted the action
        _email_service = AdaptationActionEmailServices(EmailServices())

        
        print(f'The adaptation action is transitioning from {States.NEW} to {States.SUBMITTED}')

        email_status, email_data = _email_service.notify_dcc_responsible_adaptation_action_submission(self.obj, user_approver)
        if email_status:
            return email_status, email_data
        else:
            ...
   

    @state.transition(source=(States.UPDATING_BY_REQUEST_DCC), target=States.SUBMITTED, permission=None)
    def submit_updated_record(self, user_approver):
        # updating_by_request_DCC --> submitted
        # send email to user that submitted the action
        _email_service = AdaptationActionEmailServices(EmailServices())
        print(f'The adaptation action is transitioning from {States.UPDATING_BY_REQUEST_DCC} to {States.SUBMITTED}')

        email_status, email_data = _email_service.notify_contact_responsible_adaptation_action_update(self.obj, user_approver)
        if email_status:
            return email_status, email_data
        else:
            ...


    @state.transition(source=(States.SUBMITTED), target=States.IN_EVALUATION_BY_DCC, permission=None)
    def evaluate_by_DCC(self, user_approver):
        # submitted --> in_evaluation_by_DCC
        # send email to user that submitted the action
        print(f'The adaptation action is transitioning from {States.SUBMITTED} to {States.IN_EVALUATION_BY_DCC}')
        _email_service = AdaptationActionEmailServices(EmailServices())

        email_status, email_data = _email_service.notify_contact_responsible_adaptation_action_evaluation_by_dcc(self.obj, user_approver)
        print(email_status, email_data)
        if email_status:
            return email_status, email_data
        else:
            ...
            # maybe raise exception

    ##
    ## rejected_by_DCC, requested_changes_by_DCC, accepted_by_DCC
    ##
    @state.transition(source=States.IN_EVALUATION_BY_DCC, target=States.REJECTED_BY_DCC, permission=None)
    def evaluate_by_DCC_rejected(self, user_approver):
        # in_evaluation_by_DCC --> rejected_by_DCC
        # send email to user that submitted the action
        print(f'The adaptation action is transitioning from {States.IN_EVALUATION_BY_DCC} to {States.REJECTED_BY_DCC}')
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
        print(f'The adaptation action is transitioning from {States.IN_EVALUATION_BY_DCC} to {States.REQUESTED_CHANGES_BY_DCC}')
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
        print(f'The adaptation action is transitioning from {States.IN_EVALUATION_BY_DCC} to {States.ACCEPTED_BY_DCC}')
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
        print(f'The adaptation action is transitioning from {States.REJECTED_BY_DCC} to {States.END}')
        ...
    
    @state.transition(source=(States.REQUESTED_CHANGES_BY_DCC), target=States.UPDATING_BY_REQUEST_DCC, permission=None)
    def update_by_DCC_request(self, user_approver):
        # requested_changes_by_DCC --> updating_by_request_DCC
        # send email to user that submitted the action
        print(f'The adaptation action is transitioning from {States.REQUESTED_CHANGES_BY_DCC} to {States.UPDATING_BY_REQUEST_DCC}')
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
        print(f'The adaptation action is transitioning from {States.ACCEPTED_BY_DCC} to {States.REGISTERED_BY_DCC}')
        ...


