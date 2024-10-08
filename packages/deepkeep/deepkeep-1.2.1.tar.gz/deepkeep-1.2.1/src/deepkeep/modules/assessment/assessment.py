from ..base_module import BaseModule
from .report import Report
from .consts import ReportType

__all__ = ["Assessment"]


class Assessment(BaseModule):
    root_path: str = "assessment"
    report: Report

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.report = Report(self._client)

    def create(self, model_id: str, name: str, description: str = None, dataset_id: str = None,
               blank: bool = True, application_id: str = ""):
        json_params = {
            "name": name,
            "model_id": model_id,
            "dataset_id": dataset_id,
            "blank": blank,
            "application_id": application_id}
        if description:
            json_params["description"] = description
        data = self._make_request(method="POST", path=f"{self.root_path}/create",
                                  json_params=json_params)
        return data

    def get(self, assessment_id: str):
        return self._make_request(method="GET", path=f"{self.root_path}/{assessment_id}")

    def update(self, assessment_id: str, name: str = None, description: str = None, status: str = None):
        json_params = {}
        if name:
            json_params["name"] = name
        if description:
            json_params["description"] = description
        if status:
            json_params["status"] = status
        return self._make_request(method="PUT", path=f"{self.root_path}/{assessment_id}",
                                  json_params=json_params)

    def delete(self, assessment_id: str):
        return self._make_request(method="DELETE", path=f"{self.root_path}/{assessment_id}")

    def list(self, filter_by: dict = None):
        return self._make_request(method="POST", path=f"{self.root_path}/list",
                                  json_params=filter_by)

    def get_config(self, assessment_id: str, report_id: str):
        return self._make_request(method="GET", path=f"{self.root_path}/{assessment_id}/report/{report_id}/config/get")

    def set_config(self, assessment_id: str, report_id: str, updated_data: dict):
        return self._make_request(method="POST", path=f"{self.root_path}/{assessment_id}/report/{report_id}/config/set",
                                  json_params=updated_data)

    def run(self, assessment_id: str):
        return self._make_request(method="POST", path=f"{self.root_path}/{assessment_id}/run")

    def get_report_results(self, assessment_id: str, report_results_id: str):
        return self._make_request(method="GET", path=f"{self.root_path}/{assessment_id}/report/results/{report_results_id}")

    def get_report_results_topic(self, assessment_id: str, report_results_id: str, topic_id: str):
        return self._make_request(method="GET", path=f"{self.root_path}/{assessment_id}/report/results/{report_results_id}/topic/{topic_id}")

    def list_report_results(self, report_type: ReportType = ReportType.LLM):
        report_type = report_type.value
        return self._make_request(method="POST", path=f"{self.root_path}/report/results/list/{report_type}")
