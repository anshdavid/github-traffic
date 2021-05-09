import json
from collections import defaultdict
from typing import DefaultDict, Dict, List, NamedTuple, Optional
from urllib import request
import rich
from rich import box
from rich.console import Console, ConsoleOptions, RenderResult
from rich.style import Style
from rich.table import Table

from .dataclass import ntClone, ntPath, ntReferral, ntView, ntRepo


class Record:
    def __init__(self) -> None:
        self.info: Dict[str, ntRepo] = dict()
        self.referrals: Dict[str, ntReferral] = dict()
        self.paths: DefaultDict[str, List[ntPath]] = defaultdict()
        self.views: Dict[str, ntView] = dict()
        self.clones: Dict[str, ntClone] = dict()

        self.table = Table(
            title="Repository Statistics",
            box=box.HORIZONTALS,
            show_edge=False,
            show_lines=False,
            show_footer=True,
            title_style=Style(bold=True, underline=True),
            expand=True,
        )

        self.table.add_column("Index", style="white", no_wrap=True)
        self.table.add_column("Name", style="cyan", no_wrap=True)
        self.table.add_column("View Count", style="magenta")
        self.table.add_column("View Unique", style="green")
        self.table.add_column("Clone Count", style="magenta")
        self.table.add_column("Clone Unique", style="green")
        self.table.add_column("Stargazers", style="magenta")
        self.table.add_column("Forks", style="green")
        self.table.add_column("Watchers", style="magenta")
        self.table.add_column("Open Issues", style="green")

    def RecordHandler(self, event: NamedTuple):
        pass

    def __rich_console__(
        self, console: Console, options: ConsoleOptions
    ) -> RenderResult:

        assert (
            len(self.views.keys()) == len(self.clones.keys()) == len(self.info.keys())
        )

        for index, keyv in enumerate(self.views.keys()):
            self.table.add_row(
                str(index + 1),
                keyv,
                str(self.views[keyv].count),
                str(self.views[keyv].uniques),
                str(self.clones[keyv].count),
                str(self.clones[keyv].uniques),
                str(self.info[keyv].stargazers_count),
                str(self.info[keyv].forks_count),
                str(self.info[keyv].watchers_count),
                str(self.info[keyv].open_issues_count),
            )

        yield self.table
