from typing import Iterable

from rich.progress import Progress
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from indentalog.wrappers.callpoint import CallPoint
from indentalog.wrappers.endpoint import EndPoint


class IterableCallPoint(CallPoint):
    def __init__(self, total: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.total = total
        self.progress = Progress()
        self.task_id = self.progress.add_task("", total=total)
        self.spinner = Spinner(self.ilog.config.spinner_type)

    def render(self) -> Progress:
        self.progress.update(self.task_id)
        grid = Table.grid()

        # Create the elements in the correct order
        elements = []
        if self.depth > 0:
            elements.append(self.offset())
        if self.finished:
            elements.append(
                Text(
                    f"{self.ilog.config.end_symbol} {self.name}",
                    style=self.ilog.config.end_color,
                )
            )
        else:
            elements.append(self.spinner)
            elements.append(Text(f" {self.name}"))
        elements.append(self.progress)

        # Add the elements to the grid
        for _ in elements:
            grid.add_column(justify="left")
        grid.add_row(*elements)

        return grid

    def clear_call_stack(self) -> None:
        if not self.progress.finished:
            while self.ilog.call_stack[-1] != self:
                self.ilog.call_stack.pop()

    def advance(self) -> None:
        self.progress.advance(self.task_id)
        self.clear_call_stack()


class IterableEndPoint(EndPoint):
    def __init__(
        self,
        iterable: Iterable,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.iterable = iterable
        if self.name is None:
            self.name = ""

    def __iter__(self):
        call_point = IterableCallPoint(
            total=len(self.iterable),
            ilog=self.ilog,
            leave=self.leave,
            name=self.name,
        )
        for item in self.iterable:
            yield item
            call_point.advance()
        call_point.stop()
