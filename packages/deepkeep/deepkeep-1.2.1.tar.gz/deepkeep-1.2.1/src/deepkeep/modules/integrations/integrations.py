from ..base_module import BaseModule
from .consts import IntegrationsType


def arrange_locals(locals_dict: dict, exclude_keys: list = None, filter_none: bool = True):
    """
    Arrange locals dictionary to exclude keys and filter None values
    :param locals_dict: dictionary of locals
    :param exclude_keys: list of keys to exclude
    :param filter_none: boolean value that indicates if None values should be filtered
    :return: dictionary of arranged locals
    """
    if exclude_keys is None:
        exclude_keys = []
    return {k: v for k, v in locals_dict.items() if k != 'self' and k not in exclude_keys and
            (v is not None or not filter_none)}


class Integrations(BaseModule):
    root_path: str = "integrations"

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.package = 'deepkeep.modules.integrations.integrations_sources'
        self._modules = [integration_type.value for integration_type in IntegrationsType]
        self._load_modules()

    def get(self, integration_id: str):
        return self._make_request(method="GET", path=f"{self.root_path}/{integration_id}")

    def list(self, page: int = 1, size: int = 10):
        return self._make_request(method="GET", path=f"{self.root_path}", query_params={"page": page, "size": size})

    def delete(self, integration_id: str):
        return self._make_request(method="DELETE", path=f"{self.root_path}/{integration_id}")
