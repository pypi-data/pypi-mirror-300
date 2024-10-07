
from cval_lib.handlers.dataset import Dataset
from cval_lib.handlers.embedding import Embedding
from cval_lib.handlers.detection import Detection
from cval_lib.handlers.classification import Classification
from cval_lib.handlers.result import Result
from cval_lib.handlers.frames import Frames

from cval_lib.handlers.annotation import (
    Detection as DetectionAnnotation,
    Classification as ClassificationAnnotation,
    Segmentation as SegmentationAnnotation,
)
from cval_lib.handlers.segmentation import Segmentation
from cval_lib.handlers.storage import Storage
from cval_lib.utils.base_conn import BaseConn


class CVALConnection(BaseConn):
    def dataset(self) -> Dataset:
        """
        actions with dataset: : create, get, delete, update by ID or all (with some limits)
        :return: Dataset
        """
        return Dataset(session=self.session, )

    def embedding(self, dataset_id: str, part_of_dataset: str) -> Embedding:
        """
        actions with embedding: create, get, delete, update by ID or all (with some limits)
        :param dataset_id: id of dataset
        :param part_of_dataset: type of dataset (training, test, validation)
        :return: Embedding
        """
        return Embedding(self.session, dataset_id=dataset_id, part_of_dataset=part_of_dataset, )

    def detection(self) -> Detection:
        """
        This method can be used to call a detection sampling or test
        :return: Detection
        """
        return Detection(self.session, )

    def result(self) -> Result:
        """
        This method can be used for polling
        :return: Result
        """
        return Result(self.session, )

    def frames(self, dataset_id: str, part_of_dataset: str = None) -> Frames:
        """
        This method can be used for raw frames data uploading and get metadata
        :return: Frames
        """
        return Frames(self.session, dataset_id=dataset_id, part_of_dataset=part_of_dataset)

    def det_annotation(self, dataset_id: str, ) -> DetectionAnnotation:
        """
        This method can be used for annotation uploading and get for detection tasks
        :return: DetectionAnnotation
        """
        return DetectionAnnotation(self.session, dataset_id=dataset_id, )

    def cls_annotation(self, dataset_id: str) -> ClassificationAnnotation:
        """
        This method can be used for annotation uploading and get for classification tasks
        :return: DetectionAnnotation
        """
        return ClassificationAnnotation(self.session, dataset_id)

    def seg_annotation(self, dataset_id: str) -> SegmentationAnnotation:
        """
        This method can be used for annotation uploading and get for segmentation tasks
        :return: DetectionAnnotation
        """
        return SegmentationAnnotation(self.session, dataset_id)

    def segmentation(self) -> Segmentation:
        """
        This method can be used to call a segmentation sampling or test
        :return: Segmentation
        """
        return Segmentation(self.session)

    def classification(self) -> Classification:
        """
        This method can be used to call a classification sampling or test
        :return: Classification
        """
        return Classification(self.session)

    def storage(self, _id: str = None):
        return Storage(self.session, _id)
