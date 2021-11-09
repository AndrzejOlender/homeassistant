"""QueueManager::factory"""

import logging
import time
from datetime import timedelta
import asyncio

from queueman.exceptions import QueueManagerExecutionStillInProgress


class QueueManager:
    """The QueueManager class."""

    logger = logging.getLogger(__name__)

    running = False
    queue = []

    @property
    def pending_tasks(self):
        """Return a count of pending tasks in the queue."""
        return len(self.queue)

    @property
    def has_pending_tasks(self):
        """Return a count of pending tasks in the queue."""
        return self.pending_tasks != 0

    def clear(self):
        """Clear the queue."""
        self.queue = []

    def add(self, task):
        """Add a task to the queue."""
        self.queue.append(task)

    async def execute(self, number_of_tasks=None):
        """Execute the tasks in the queue."""
        if self.running:
            self.logger.debug("Execution is allreay running")
            raise QueueManagerExecutionStillInProgress
        if len(self.queue) == 0:
            self.logger.debug("The queue is empty")
            return

        self.running = True

        self.logger.debug("Checking out tasks to execute")
        local_queue = []

        if number_of_tasks:
            for task in self.queue[:number_of_tasks]:
                local_queue.append(task)
        else:
            for task in self.queue:
                local_queue.append(task)

        for task in local_queue:
            self.queue.remove(task)

        self.logger.debug("Starting queue execution for %s tasks", len(local_queue))
        start = time.time()
        await asyncio.gather(*local_queue)
        end = time.time() - start

        self.logger.debug(
            "Queue execution finished for %s tasks finished in %.2f seconds",
            len(local_queue),
            end,
        )
        if self.has_pending_tasks:
            self.logger.debug("%s taks remaining in the queue", len(self.queue))
        self.running = False
