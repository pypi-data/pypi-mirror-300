from ..base_module import BaseModule
from .templates import Templates


def get_root_path(assessment_id: str) -> str:
    return f"assessment/{assessment_id}/report"


class Report(BaseModule):
    templates: Templates
    root_path = get_root_path("assessment_id")

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.templates = Templates(self._client)

    def add(self, assessment_id: str, report_template_id: str):
        return self._make_request(method="POST", path=f"{get_root_path(assessment_id)}/{report_template_id}")

    def get(self, assessment_id: str, report_id: str = None):
        if report_id:
            return self._make_request(method="GET", path=f"{get_root_path(assessment_id)}/{report_id}")
        return self._make_request(method="GET", path=f"{get_root_path(assessment_id)}/list")

    def delete(self, assessment_id: str, report_id: str):
        return self._make_request(method="DELETE", path=f"{get_root_path(assessment_id)}/{report_id}")


