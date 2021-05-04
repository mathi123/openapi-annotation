from datetime import datetime
from dateutil import parser


class DateFilter:
    def __init__(self, exactly: datetime = None, start: datetime = None, end: datetime = None,
                 include_start: bool = True, include_end: bool = True, *args, **kwargs):
        self._exactly = exactly
        self._start = start
        self._end = end
        self._include_start = include_start
        self._include_end = include_end

    @staticmethod
    def from_str(text: str):
        if text is None:
            return None

        result = DateFilter()

        try:
            exact = parser.parse(text)
            result.exactly = exact
            return result
        except:
            text = text.strip()

            result.include_start = not text.startswith(']')
            result.include_end = not text.endswith('[')

            text = text.strip('[').strip(']')
            split = text.split(',')

            if split[0]:
                result.start = parser.parse(split[0])

            if len(split) > 1 and split[1]:
                result.end = parser.parse(split[1])

            return result

    @property
    def exactly(self) -> datetime:
        return self._exactly

    @exactly.setter
    def exactly(self, value: datetime):
        self._exactly = value

    @property
    def start(self) -> datetime:
        return self._start

    @start.setter
    def start(self, start: datetime):
        self._start = start

    @property
    def end(self) -> datetime:
        return self._end

    @end.setter
    def end(self, end: datetime):
        self._end = end

    @property
    def include_start(self) -> bool:
        return self._include_start

    @include_start.setter
    def include_start(self, value: bool):
        self._include_start = value

    @property
    def include_end(self) -> bool:
        return self._include_end

    @include_end.setter
    def include_end(self, value: bool):
        self._include_end = value
