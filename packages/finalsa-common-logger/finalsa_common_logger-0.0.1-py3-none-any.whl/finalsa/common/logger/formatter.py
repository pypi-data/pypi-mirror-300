from pythonjsonlogger import jsonlogger
from datetime import datetime, timezone


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
        if log_record.get('correlation_id'):
            log_record['correlation_id'] = str(log_record['correlation_id'])


formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
