from typing import List, Optional

from rich.console import RenderableType
from rich.text import Text

from indentalog.config import IndentedLoggerConfig


class PartialIndentedLogger:
    call_stack: List["CallPoint"] = []
    config: IndentedLoggerConfig

    def handle_start_live(self) -> None:
        pass

    def handle_stop_live(self) -> None:
        pass


class CallPoint:
    """A callpoint is a point in the call stack where we want to monitor the progress of a function or an iterable. It is created by an endpoint."""

    def __init__(
        self, ilog: PartialIndentedLogger, leave: bool, name: Optional[str] = None
    ) -> None:
        self.ilog = ilog
        self.leave = leave
        self.name = name

        self.start()

    def render(self) -> RenderableType:
        pass

    def start(self) -> None:
        self.finished = False
        self.ilog.call_stack.append(self)
        self.depth = self._compute_depth()
        self.ilog.handle_start_live()

    def stop(self) -> None:
        self.finished = True
        if not self._should_leave():
            self.ilog.call_stack.remove(self)
        self.ilog.handle_stop_live()

    def _compute_depth(self) -> int:
        depth = 0
        for call_point in self.ilog.call_stack:
            if call_point == self:
                return depth
            elif not call_point.finished:
                depth += 1

        raise ValueError("Expected to find the current call point in the stack.")

    def _should_leave(self) -> bool:
        # If the parent call point is not left, its children should not be left either.
        # We only need to check the previous call point because:
        # 1. Either it is the parent call point, in which case we can check if has leave=True
        # 2. Or it is a sibling call point that has been left, which means that the parent
        #    call point has leave=True
        if len(self.ilog.call_stack) > 1:
            previous_call_point = self.ilog.call_stack[
                self.ilog.call_stack.index(self) - 1
            ]
            return self.leave and previous_call_point.leave
        else:
            return self.leave

    def _depths_to_mark(self) -> bool:
        visits = [0] * (self.depth + 1)
        broken_flow = False
        for call_point in self.ilog.call_stack[self.ilog.call_stack.index(self) + 1 :]:
            if call_point.depth > self.depth:
                continue
            elif call_point.depth == self.depth:
                if not broken_flow:
                    visits[self.depth] += 1
            else:
                visits[call_point.depth] += 1
                broken_flow = True

        return [visit > 0 for visit in visits]

    def offset(self) -> Text:
        text = Text()
        if self.depth == 0:
            return text  # We don't want to add any offset for the root call point. However, don't add an empty offset in a rich table as it will still take up horizontal space.

        depths_to_mark = self._depths_to_mark()
        for depth in range(self.depth)[1:]:
            if depths_to_mark[depth]:
                text.append("│" + " " * self.ilog.config.offset)
            else:
                text.append(" " * (self.ilog.config.offset + 1))

        if depths_to_mark[self.depth]:
            text.append("├" + "─" * self.ilog.config.offset)
        else:
            text.append("└" + "─" * self.ilog.config.offset)

        return text
