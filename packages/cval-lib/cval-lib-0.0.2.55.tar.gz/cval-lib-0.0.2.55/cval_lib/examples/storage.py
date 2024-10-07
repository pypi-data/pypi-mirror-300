import timeit

if __name__ == '__main__':
    from cval_lib.connection import CVALConnection
    import json
    with open('creds.json') as f:
        CREDS_JSON = json.load(f)
    CVAL = CVALConnection(...)
    DS = CVAL.dataset()
    DS_ID = DS.create()

    STORAGE = CVAL.storage().create(**CREDS_JSON)
    DS.synchronize(STORAGE)
    COUNT = 10_000
    train = {'frames_quantity': 0}
    while train['frames_quantity'] != COUNT:
        train = CVAL.frames(DS_ID, 'training').read_meta(1)
