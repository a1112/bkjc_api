import datetime as dt
import os

from demo._demo_config import bootstrap_dbm, print_banner


def resolve_dates():
    if os.getenv("BKJC_START_DATE") and os.getenv("BKJC_END_DATE"):
        return os.getenv("BKJC_START_DATE"), os.getenv("BKJC_END_DATE")

    days = int(os.getenv("BKJC_TIMELINE_DAYS", "7"))
    end = dt.date.today()
    start = end - dt.timedelta(days=days)
    return start.isoformat(), end.isoformat()


def main():
    db = bootstrap_dbm()
    start_date, end_date = resolve_dates()
    print_banner("Steel timeline", f"{start_date} -> {end_date}")

    results = db.getSteelByDate(start_date, end_date)
    print(f"Fetched {len(results)} steels between {start_date} and {end_date}")
    for steel_obj, _ in results[:5]:
        print(
            "  ",
            getattr(steel_obj, "SteelID", "unknown"),
            getattr(steel_obj, "TopDetectTime", ""),
            getattr(steel_obj, "TopDefectNum", 0),
            getattr(steel_obj, "BottomDefectNum", 0),
        )


if __name__ == "__main__":
    main()
