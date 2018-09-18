class WorkflowActiveSteps():
    def __init__(self):
        self.registered_steps = []
        self.registered_steps.append("dummy - 0")
        self.registered_steps.append("dummy - 1")

    def is_enabled(self, step_label):
        return self.registered_steps.__contains__(step_label)