from logging import Filter
from typing import TYPE_CHECKING, Optional
from finalsa.traceability.context import (
    get_correlation_id,
    get_span_id,
    get_trace_id
)
if TYPE_CHECKING:
    from logging import LogRecord


class CorrelationIdFilter(Filter):
    """Logging filter to attached correlation IDs to log records"""

    def __init__(self, name: str = '', uuid_length: Optional[int] = None, default_value: Optional[str] = None):
        super().__init__(name=name)
        self.uuid_length = uuid_length
        self.default_value = default_value

    def filter(self, record: 'LogRecord') -> bool:
        record.correlation_id = get_correlation_id()
        record.trace_id = get_trace_id()
        record.span_id = get_span_id()
        return True
