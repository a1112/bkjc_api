import logging
import os
import time

from demo._demo_config import bootstrap_dbm, print_banner

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def summarize_steel(records):
    summary = []
    for steel_obj, steel_id in records:
        steel_no = getattr(steel_obj, "SteelID", getattr(steel_id, "SteelID", "unknown"))
        seq_no = getattr(steel_obj, "SequeceNo", "n/a")
        top_defects = getattr(steel_obj, "TopDefectNum", 0)
        bottom_defects = getattr(steel_obj, "BottomDefectNum", 0)
        summary.append(
            f"{steel_no} seq={seq_no} defects(top/bottom)={top_defects}/{bottom_defects}"
        )
    return summary


def main():
    limit = int(os.getenv("BKJC_STEEL_LIMIT", "10"))
    defect_only = os.getenv("BKJC_DEFECT_ONLY", "false").lower() == "true"

    db = bootstrap_dbm()
    start = time.time()
    print_banner("MySQL smoke", f"limit={limit} defect_only={defect_only}")

    print("Is SQL Server backend:", db.isSqlServer())
    recent = db.getSteelByNum(limit, defectOnly=defect_only)
    print(f"Fetched {len(recent)} recent steels")
    for line in summarize_steel(recent):
        print("  ", line)

    steel_id = int(os.getenv("BKJC_STEEL_ID", "1"))
    seq_no = int(os.getenv("BKJC_SEQ_NO", "1"))
    steel_no = os.getenv("BKJC_STEEL_NO", "QA2300220900")

    print("By ID:", summarize_steel(db.getSteelById(steel_id)))
    print("By SeqNo:", summarize_steel(db.getSteelBySeqNo(seq_no)))
    print("By SteelNo:", summarize_steel(db.getSteelBySteelNo(steel_no)))
    print("Date range count:", len(db.getSteelByDate("2019-01-01", "2025-01-02")))

    defect_map = db.getDefectBySeqNo(seq_no)
    print("Defect aggregate:", {k: v for k, v in defect_map.items() if isinstance(v, int)})
    # print("Defect classes:", len(db.getDefectClass()))
    print("Camera layout:", db.getCameraList())
    print(f"Elapsed: {time.time() - start:.2f}s")


if __name__ == "__main__":
    main()
