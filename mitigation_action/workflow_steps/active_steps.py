class WorkflowActiveSteps():
    def __init__(self):
        self.registered_steps = []
        self.registered_steps.append("harmonization_ingei")
        self.registered_steps.append("conceptual_proposal")

    def is_enabled(self, step_label):
        return self.registered_steps.__contains__(step_label)