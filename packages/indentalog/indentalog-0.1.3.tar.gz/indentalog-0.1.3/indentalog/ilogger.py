from typing import Callable, Iterable, List, Optional

from rich.console import Console, group
from rich.live import Live
from rich.text import Text

from indentalog.config import IndentedLoggerConfig
from indentalog.wrappers import (
    CallPoint,
    DecoratorEndPoint,
    IterableEndPoint,
    PartialIndentedLogger,
)


class IndentedLogger(PartialIndentedLogger):
    auto_start = True

    def __init__(self) -> None:
        self.config = IndentedLoggerConfig()
        self.is_live = False
        self.call_stack: List[CallPoint] = []
        self.console = Console()
        self.live = Live(
            refresh_per_second=10,
            console=self.console,
            get_renderable=self.render,
        )
        if self.auto_start:
            self.live.start()

    def __del__(self):
        # Stop live, especially useful for tests
        self.live.stop()

    def set_config(self, config: IndentedLoggerConfig) -> None:
        self.config = config

    def handle_start_live(self) -> None:
        if not self.is_live:
            for call_point in self.call_stack:
                if not call_point.finished:
                    self.live.auto_refresh = True
                    self.is_live = True
                    break

    def handle_stop_live(self) -> None:
        if self.is_live:
            for call_point in self.call_stack:
                if not call_point.finished:
                    return
            self.live.auto_refresh = False
            self.is_live = False
            self.live.refresh()

    @group()
    def render(self):
        for call_point in self.call_stack:
            yield call_point.render()

        if not self.is_live:
            yield Text()  # Add final newline to the output to avoid ugly % in the terminal

    def __call__(
        self,
        arg1: Optional[Iterable] = None,
        leave: bool = True,
        name: Optional[str] = None,
    ) -> Callable[[Callable], Callable]:
        if arg1 is None:
            endpoint = DecoratorEndPoint(ilog=self, leave=leave, name=name)
            return endpoint

        elif isinstance(arg1, Iterable):
            endpoint = IterableEndPoint(
                iterable=arg1, ilog=self, leave=leave, name=name
            )
            return endpoint

        else:
            raise ValueError(f"Invalid argument {arg1} for IndentedLogger class.")
