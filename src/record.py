import json
from collections import defaultdict
from typing import DefaultDict, Dict, List, NamedTuple, Optional
from urllib import request
import rich
from rich import box
from rich.console import Console, ConsoleOptions, RenderResult
from rich.style import Style
from rich.table import Table

from .dataclass import ntClone, ntPath, ntReferral, ntView


class Record:
    def __init__(self) -> None:
        self.referrals: Dict[str, Optional[ntReferral]] = dict()
        self.paths: DefaultDict[
            str, Optional[List[ntPath]]
        ] = defaultdict()
        self.views: Dict[str, Optional[ntView]] = dict()
        self.clones: Dict[str, Optional[ntClone]] = dict()

        self.table = Table(
            title="Git Traffic v0.1.3",
            box=box.HORIZONTALS,
            show_edge=False,
            show_lines=False,
            show_footer=True,
            title_style=Style(bold=True, underline=True),
        )
        self.table.add_column("Name", style="cyan", no_wrap=True)
        self.table.add_column("View Count", style="magenta")
        self.table.add_column("View Unique", style="green")
        self.table.add_column("Clone Count", style="magenta")
        self.table.add_column("Clone Unique", style="green")

    def RecordHandler(self, event: NamedTuple):
        pass

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        assert len(self.views.keys()) == len(self.clones.keys())

        for keyv in self.views.keys():
            self.table.add_row(
                keyv,
                str(self.views[keyv].count),
                str(self.views[keyv].uniques),
                str(self.clones[keyv].count),
                str(self.clones[keyv].uniques),
            )

        yield self.table
