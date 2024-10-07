import time

from cval_lib.models.annotation import ImageSegAnnotation

if __name__ == '__main__':
    from cval_lib.connection import CVALConnection
    from cval_lib.models.annotation import SegmentationAnnotation

    USER_API_KEY = ...
    CVAL = CVALConnection(USER_API_KEY)
    DS_ID = CVAL.dataset().create()

    ANN = CVAL.seg_annotation(dataset_id=DS_ID).create(
        annotation=SegmentationAnnotation(
            train=[ImageSegAnnotation(image_id='1.png', masks=[{'label': 0, 'mask': [.0, .5, .5, .0, .5, .5]}])],
            test=[ImageSegAnnotation(image_id='2.png', masks=[{'label': 0, 'mask': [.0, .5, .5, .0, .5, .5]}])],
            val=[[ImageSegAnnotation(image_id='2.png', masks=[{'label': 0, 'mask': [.0, .5, .5, .0, .5, .5]}])]]
        )
    )

    RES = CVAL.segmentation().saas(dataset_id=DS_ID, model='yolo')
    time.sleep(60 * 120 * 600)
    print(CVAL.result().get(RES.task_id))
