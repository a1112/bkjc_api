import logging
import os
import time

from demo._demo_config import bootstrap_dbm, print_banner

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def summarize_grade(grade):
    if not grade:
        return "grade info not found"
    return {
        "steel_no": getattr(grade, "SteelID", None),
        "seq_no": getattr(grade, "SequeceNo", None),
        "steel_use": getattr(grade, "SteelUse", "").strip(),
        "quality": getattr(grade, "Quality", "").strip(),
    }


def main():
    os.environ.setdefault("BKJC_DRIVE", "sqlserver")
    db = bootstrap_dbm()

    limit = int(os.getenv("BKJC_STEEL_LIMIT", "20"))
    seq_no = int(os.getenv("BKJC_SEQ_NO", "1"))
    steel_no = os.getenv("BKJC_STEEL_NO", "3A15150400")

    print_banner("SQL Server smoke", f"limit={limit} seq_no={seq_no}")
    start = time.time()

    recent = db.getSteelByNum(limit, defectOnly=True)
    print(f"Recent defect steels: {len(recent)}")
    if recent:
        item = recent[0][0]
        print(
            "Sample record:",
            getattr(item, "SteelID", "unknown"),
            getattr(item, "TopDefectNum", 0),
            getattr(item, "BottomDefectNum", 0),
        )

    print("Seq lookup:", db.getSteelBySeqNo(seq_no))
    seq_id = db.getSeqIdBySteelNo(steel_no) or "n/a"
    print(f"Seq id for steel {steel_no}: {seq_id}")
    print("Grade info:", summarize_grade(db.getGradeInfo(seq_no)))
    print("Camera list:", db.getCameraList())

    defect_map = db.getDefectBySeqNo(seq_no)
    camera_counts = {
        cam_id: payload["count"]
        for cam_id, payload in defect_map.items()
        if isinstance(payload, dict) and "count" in payload
    }
    print("Per camera defect counts:", camera_counts)

    info = db.getSteelInfo(steel_no)
    print(f"Expanded info rows: {len(info)}")

    print(f"Elapsed: {time.time() - start:.2f}s")


if __name__ == "__main__":
    main()
