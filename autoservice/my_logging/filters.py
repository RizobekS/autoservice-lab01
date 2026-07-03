import logging


class SlowSQLQueryFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        # Select only sql queries
        attr = getattr(record, 'sql', False)
        if not attr:
            return False

        # Select only queries slower than 0.120s
        if isinstance(record.args[0], float) and record.args[0] > 0.120:
            return True

        return False
