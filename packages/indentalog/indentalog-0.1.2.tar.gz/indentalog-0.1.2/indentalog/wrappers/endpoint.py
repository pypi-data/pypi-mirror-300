from typing import Optional

from indentalog.wrappers.callpoint import PartialIndentedLogger


class EndPoint:
    """An endpoint is a point in the code where we want to monitor the progress of a function or an iterable."""

    def __init__(
        self,
        ilog: PartialIndentedLogger,
        leave: bool,
        name: Optional[str] = None,
    ) -> None:
        self.ilog = ilog
        self.leave = leave
        self.name = name
