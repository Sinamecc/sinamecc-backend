class WorkflowActiveSteps():
    def __init__(self):
        self.registered_steps = {}
        self.registered_steps["harmonization_ingei"] = "submit_INGEI_changes_evaluation"
        self.registered_steps["conceptual_proposal"] = "implement_submit_SINAMECC_conceptual_proposal_integration"

    def is_enabled(self, step_label):
        return self.registered_steps.keys().__contains__(step_label)

    def get_next_state(self, step_label):
        if self.is_enabled(step_label):
            return self.registered_steps.get(step_label)