from ..base_module import BaseModule
from .consts import IntegrationModels
from .utils import arrange_locals


class Model(BaseModule):
    root_path: str = "model"

    def __init__(self, client: 'DeepKeep'):
        super().__init__(client)
        self.package = 'deepkeep.modules.model.integration_models'
        self._modules = [integration_model.value for integration_model in IntegrationModels]
        self._load_modules()

    def create(self, title: str, model_framework: str, model_purpose: str, description: str = "Default description",
               model_source_path: str = None, source_type: str = "local", loading_option: str = "other", training_params: dict = None,
               requirements: list[str] = None, input_categories: list[dict] = None, output_categories: list[dict] = None,
               **kwargs):
        """
        Create a new model metadata object and save it to the metadata repository.
        :param title: Name of the model.
        :param model_framework: Framework used by the model. (Required)
        :param model_purpose: Purpose of the model. (Required)
        :param description: Description of the model.
        :param model_source_path: Path to where the model's data is stored.
        :param source_type: Type of source used to store the model. (Default: local)
        :param loading_option: How to load the model. (Default: framework)
        :param training_params: Training parameters.
        :param requirements: Requirements list for the model.
        :param input_categories: A list of dicts containing the name, type and shape of the inputs to the model.
        :param output_categories: A list of dicts containing the name, type and shape of the outputs of the model.
        :param kwargs: Optional additional keyword arguments:
           - model_loading_path: Path to the model loading file if LoadingOption is CODE
           - class_mapping: Class mapping for the model, in case of classification/object detection models.
        :return: The response from the API.
        """
        data = arrange_locals(locals(), filter_none=False)
        return self._make_request(method="POST", path=f"{self.root_path}/create", json_params=data)

    def get(self, model_id: str):
        """
        Get model metadata by model ID.
        :param model_id: string representing the model ID
        :return: dict with model metadata
        """
        return self._make_request(method="GET", path=f"{self.root_path}/{model_id}")

    def update(self, model_id: str, status: str = None, title: str = None, description: str = None,
               tags: list[str] = None):
        """
        Update model metadata by model ID.
        :param model_id: string representing the model ID
        :param status: string representing the status of the model
        :param title: string representing the title of the model
        :param description: string representing the description of the model
        :param tags: list of tags related to the model
        :return: dict with model metadata
        """
        data = arrange_locals(locals(), ["model_id"])
        return self._make_request(method="PUT", path=f"{self.root_path}/{model_id}",
                                  json_params=data)

    def delete(self, model_id: str):
        """
        Delete model metadata by model ID.
        :param model_id: string representing the model ID
        :return: delete response
        """
        return self._make_request(method="DELETE", path=f"{self.root_path}/{model_id}")
