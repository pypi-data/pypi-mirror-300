from ..base_module import BaseModule
from .templates import Templates


class Filter(BaseModule):
    root_path: str = "firewall/filter"
    templates: Templates

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.templates = Templates(self._client)

    def add(self, firewall_id: str, filter_template_id: str):
        """
        Add a filter to a firewall
        :param firewall_id: str: firewall id
        :param filter_template_id: str: filter template id
        :return: dict: response
        """
        return self._make_request(method="POST", path=f"{self.root_path}/{firewall_id}/{filter_template_id}")
