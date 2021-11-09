"""QueueManager::exceptions"""


class QueueManagerBaseException(Exception):
    """Base exception for QueueManager."""


class QueueManagerExecutionStillInProgress(QueueManagerBaseException):
    """Exception to raise if execution is still in progress."""
