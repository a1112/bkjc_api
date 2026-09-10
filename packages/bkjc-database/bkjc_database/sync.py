"""Single-worker incremental synchronization with one transaction per surface."""


def sync_defects_once(source, steels, destination, batch_size=500):
    if not 1 <= batch_size <= 10000:
        raise ValueError("Invalid batch size")
    copied = 0
    for camera, is_top in ((1, 1), (2, 0)):
        with destination.Session() as session:
            with session.begin():
                cursor = destination.getLastDefectId(is_top, session)
                defects = source.getDefectsAfter(camera, cursor, batch_size)
                cache = {}
                previous = cursor
                for defect in defects:
                    if defect.defectID <= previous or defect.camNo != camera:
                        raise ValueError("Invalid source ordering or camera")
                    if defect.seqNo not in cache:
                        cache[defect.seqNo] = steels.getSteelBySeqNo(defect.seqNo)
                    destination.appendDefect(defect, cache[defect.seqNo], session)
                    previous = defect.defectID
                copied += len(defects)
    return copied
