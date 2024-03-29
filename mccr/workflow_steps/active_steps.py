class WorkflowActiveSteps():
    def __init__(self):
        self.registered_steps = {}
        self.registered_steps["ovv_proposal"] = "mccr_ovv_upload_evaluation"
        self.registered_steps["monitoring_proposal"] = "mccr_upload_report_sinamecc"
        self.registered_steps["ovv_evaluation_monitoring"] = "mccr_ovv_upload_evaluation_monitoring"
     

    def is_enabled(self, step_label):
        return self.registered_steps.__contains__(step_label)
    
    def get_next_state(self, step_label):
        if self.is_enabled(step_label):
            return self.registered_steps.get(step_label)