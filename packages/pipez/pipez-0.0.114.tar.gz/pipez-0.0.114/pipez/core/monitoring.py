from typing import Optional
import logging
import signal
import time
import os

from pipez.core.batch import Batch
from pipez.core.enums import NodeType
from pipez.core.node import Node


class Monitoring(Node):
    def __init__(self, **kwargs):
        super().__init__(name=self.__class__.__name__, type=NodeType.PROCESS, timeout=10.0, **kwargs)

    def processing(self, data: Optional[Batch]) -> Optional[Batch]:
        logging.info(self.shared_memory)
