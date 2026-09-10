"""Incremental defect synchronization using the maintained database package."""
import logging
from threading import Event, Thread

from bkjc_database.sync import sync_defects_once

logger = logging.getLogger(__name__)


class DefectSynchronizer(Thread):
    def __init__(self, source=None, steels=None, destination=None, interval=60, batch_size=500):
        super().__init__()
        self.source, self.steels, self.destination = source, steels, destination
        self.interval, self.batch_size = interval, batch_size
        self.stop_event = Event()

    def run_once(self):
        # Model imports follow explicit configuration in core.init.initDataBase.
        if self.source is None:
            from bkjc_database.NerCarDataBase.mysql.Ncdhotstripdefect import defectDb
            self.source = defectDb
        if self.steels is None:
            from bkjc_database.NerCarDataBase.mysql.Ncdhotstrip import steelDb
            self.steels = steelDb
        if self.destination is None:
            from bkjc_database.NerCarDataBase.mysql.defectinfodatabase import defectInfoDb
            self.destination = defectInfoDb
        return sync_defects_once(self.source, self.steels, self.destination, self.batch_size)

    def stop(self):
        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():
            try:
                self.run_once()
            except Exception:
                logger.exception("Defect synchronization failed; the current surface batch was rolled back")
            self.stop_event.wait(self.interval)
