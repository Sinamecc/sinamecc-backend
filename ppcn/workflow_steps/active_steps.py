class WorkflowActiveSteps():
    def __init__(self):
        self.registered_steps = []
        self.registered_steps.append("PPCN_form")
        self.registered_steps.append("OVV_Certificate")
        self.registered_steps.append("UCC_Certificate")

    def is_enabled(self, step_label):
        return self.registered_steps.__contains__(step_label)