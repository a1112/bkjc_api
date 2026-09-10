import json
from pathlib import Path

from demo._demo_config import bootstrap_dbm, print_banner

OUTPUT_DIR = Path(__file__).with_name("output")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "defect_classes.json"


def serialize_defect_class(defect):
    return {
        "id": getattr(defect, "ID", None),
        "name": getattr(defect, "Name", None),
        "level": getattr(defect, "ClassLevel", None),
        "color": getattr(defect, "DisplayColor", None),
    }


def main():
    db = bootstrap_dbm()
    print_banner("Defect class export", f"target={OUTPUT_FILE.name}")

    defect_classes = db.getDefectClass() or []
    payload = [serialize_defect_class(item) for item in defect_classes]

    OUTPUT_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(payload)} defect classes to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
