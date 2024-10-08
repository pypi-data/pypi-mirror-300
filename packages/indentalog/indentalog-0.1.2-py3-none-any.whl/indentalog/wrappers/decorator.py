import functools
from types import TracebackType
from typing import Any, Callable, Optional, Type

from rich.console import RenderableType
from rich.spinner import Spinner
from rich.table import Table

from indentalog.wrappers.callpoint import CallPoint
from indentalog.wrappers.endpoint import EndPoint


class DecoratorCallPoint(CallPoint):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.spinner = Spinner(self.ilog.config.spinner_type, text=self.name)

    def render(self) -> RenderableType:
        if self.finished:
            text = self.offset()
            text.append(
                f"{self.ilog.config.end_symbol} {self.name}",
                style=self.ilog.config.end_color,
            )
            return text
        elif self.depth == 0:
            return self.spinner
        else:
            grid = Table.grid()
            grid.add_column(justify="left")
            grid.add_column(justify="left")
            grid.add_row(self.offset(), self.spinner)
            return grid


class DecoratorEndPoint(EndPoint):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __call__(self, func: Callable) -> Callable:
        if self.name is None:
            self.name = func.__name__

        @functools.wraps(func)
        def wrap(*args, **kwargs) -> Any:
            # Create a new call point
            call_point = DecoratorCallPoint(
                ilog=self.ilog,
                leave=self.leave,
                name=self.name,
            )
            # Call the function
            output = func(*args, **kwargs)
            # Stop the call point
            call_point.stop()

            return output

        return wrap

    def __enter__(self):
        if self.name is None:
            self.name = self.ilog.config.context_manager_name
        self.call_point = DecoratorCallPoint(
            ilog=self.ilog,
            leave=self.leave,
            name=self.name,
        )

    def __exit__(
        self,
        exctype: Optional[Type[BaseException]],
        excinst: Optional[BaseException],
        exctb: Optional[TracebackType],
    ):
        self.call_point.stop()
