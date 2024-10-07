"""
Introducing CVAL Rest API, a powerful tool for AI developers in the computer vision field.
Our service combines the concepts of human-in-the-loop and active learning to improve the quality of
your models and minimize annotation costs for classification, detection, and segmentation cases.

With CVAL, you can iteratively improve your models by following our active learning loop.
First, manually or semi-automatically annotate a random set of images.
Next, train your model and use uncertainty and diversity methods to score the remaining images for annotation.
Then, manually or semi-automatically annotate the images marked as more confident to increase the accuracy of the model.
Repeat this process until you achieve an acceptable quality of the model.

Our service makes it easy to implement this workflow and improve your models quickly and efficiently.
Try our demo notebook to see how CVAL can revolutionize your computer vision projects.

To obtain a client_api_key, please send a request to k.suhorukov@digital-quarters.com
"""
from typing import Literal

from cval_lib.handlers._based_on_json import BasedOnJSON
from cval_lib.models.result import ResultResponse


class Segmentation(BasedOnJSON):
    def saas_sampling(
            self,
            dataset_id: str,
            model: Literal['unet', 'yolo'],
            model_id: str | None = None,
            new_model_id: str | None = None,
            method: Literal['cval-custom'] | None = 'cval-custom',
            num_epochs: int = 100,
    ) -> ResultResponse:
        return self.__processing__(
            f'/dataset/sampling/{dataset_id}/segmentation',
            self._post,
            parser='ResultResponse',
            json={
                'model': model,
                'model_id': model_id,
                'new_model_id': new_model_id,
                'method': method,
                'num_epochs': num_epochs
            },
        )

    def saas_test(
            self,
            dataset_id: str,
            model: Literal['unet', 'yolo'],
            model_id: str | None = None,
    ) -> ResultResponse:
        return self.__processing__(
            f'/dataset/test/{dataset_id}/segmentation',
            self._post,
            parser='ResultResponse',
            json={
                'model': model,
                'model_id': model_id,
            },
        )
