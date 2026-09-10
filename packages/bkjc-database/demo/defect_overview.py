import os

from demo._demo_config import bootstrap_dbm, print_banner


def parse_seq_list(raw_value: str):
    seq_list = []
    for chunk in raw_value.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            seq_list.append(int(chunk))
        except ValueError:
            raise ValueError(f"Invalid sequence number: {chunk}")
    return seq_list


def main():
    seq_values = parse_seq_list(os.getenv("BKJC_SEQ_LIST", "1,2,3"))
    if not seq_values:
        raise ValueError("Provide at least one sequence number in BKJC_SEQ_LIST")

    db = bootstrap_dbm()
    print_banner("Defect overview", f"sequences={seq_values}")

    for seq_no in seq_values:
        payload = db.getDefectBySeqNo(seq_no)
        up = payload.get("upCount")
        down = payload.get("downCount")
        per_camera = {
            cam_id: camera_info["count"]
            for cam_id, camera_info in payload.items()
            if isinstance(camera_info, dict) and "count" in camera_info
        }
        print(f"Seq {seq_no}: up={up} down={down} cameras={per_camera}")


if __name__ == "__main__":
    main()
