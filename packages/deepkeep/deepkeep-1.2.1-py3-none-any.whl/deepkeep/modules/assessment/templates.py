from ..base_module import BaseModule


def get_root_path(assessment_id: str) -> str:
    return f"assessment/{assessment_id}/report"


class Templates(BaseModule):
    root_path: str = get_root_path("assessment_id")

    def get(self, assessment_id: str):
        return self._make_request(method="GET", path=f"{get_root_path(assessment_id)}/list/templates")