from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text


class TrafficProgress:
    def __init__(self, numRepos: int, numStat: int = 5) -> None:

        self.numStat = numStat
        self.numRepos = numRepos

        self.progressTable = Table.grid(expand=True)
        self.progressTotal = Progress()

        self.progressTable.add_row(
            Panel(
                Align.center(
                    Text(
                        """Placeholder""",
                        justify="center",
                    )
                ),
                title="[b]Info",
                border_style="red",
                padding=(2, 6),
            ),
            Panel(
                Align.center(
                    Text(
                        """Placeholder""",
                        justify="center",
                    )
                ),
                title="[b]Info",
                border_style="red",
                padding=(2, 6),
            ),
            Panel(
                self.progressTotal,  # type:ignore
                title="[b]Total Progress",
                border_style="green",
                padding=(1, 1),
                expand=True,
            ),
        )

        self.taskTotal = self.progressTotal.add_task(
            description="Progress", total=numStat * numRepos
        )
        self.taskRepo = self.progressTotal.add_task(
            description="Repository [bold yellow]#", total=numRepos
        )
        self.taskStat = self.progressTotal.add_task(
            description="Stat [bold violet]#", total=numStat
        )

    def UpdateRepoDescription(self, repo: str):
        self.progressTotal.update(
            self.taskRepo, description=f"Repository [bold yellow]#{repo}"
        )

    def UpdateStatDescription(self, stat: str):
        self.progressTotal.update(
            self.taskStat, description=f"Stat [bold violet]#{stat}"
        )

    def StepTotal(self):
        self.progressTotal.advance(self.taskTotal)

    def StepRepo(self):
        self.progressTotal.advance(self.taskRepo)

    def StepStat(self):
        self.progressTotal.advance(self.taskStat)

    def ResetStatProgress(self):
        self.progressTotal.reset(self.taskStat)

    def CompleteStat(self):
        self.progressTotal.reset(
            self.taskStat,
            description="Stat [bold violet]#Completed",
            completed=self.numStat,
        )
