from configparser import ConfigParser
import time
from typing import Dict

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from src.dataclass import *
from src.gitapi import APIRegister, RequestHandler
from src.record import Record


def main(args):

    # * setup progress

    progressStat = Progress(
        "{task.description}",
        SpinnerColumn(),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    taskReferrals = progressStat.add_task("[green]Referrals", total=1)
    taskPaths = progressStat.add_task("[magenta]Paths", total=1)
    taskViews = progressStat.add_task("[cyan]Views", total=1)
    taskClones = progressStat.add_task("[purple]Clones", total=1)

    progressTotal = Progress()

    # * setup display grid

    progressTable = Table.grid()
    progressTable.add_row(
        Panel(
            progressTotal,  # type:ignore
            title="Overall Progress",
            border_style="green",
            padding=(2, 2),
        ),
        Panel(
            progressStat,  # type:ignore
            title="[b]Jobs",
            border_style="red",
            padding=(1, 2),
        ),
    )

    # * setup traffic

    instanceRecord = Record()

    config = ConfigParser()
    config.read_file(open(args.config))

    username = config.get("github", "username")
    token = config.get("github", "token")

    instanceRQ = RequestHandler(token=token, register=APIRegister())

    # * init from here

    repos = instanceRQ(
        call="repos",
        args={"username": username},
    )

    assert isinstance(repos, list)

    progressTotal.console.print(
        Panel(
            f"[bold blue] Fetching {len(repos)} repository(s) Insights",
            border_style="violet",
            padding=1,
        )
    )

    taskTotal = progressTotal.add_task(
        "Overall Progress", total=4 * len(repos)
    )
    taskRepo = progressTotal.add_task("Repository", total=4)

    # * start fetch

    with Live(progressTable, refresh_per_second=10):
        for repo in repos:

            assert isinstance(repo, ntRepos)

            progressTotal.reset(
                taskRepo,
                description=f"Repository [bold yellow]#{repo.name}",
            )
            progressStat.reset(taskReferrals)
            progressStat.reset(taskPaths)
            progressStat.reset(taskViews)
            progressStat.reset(taskClones)

            # ? taks referrals
            ret = instanceRQ(
                call="referrers",
                args={"username": username, "repo": repo.name},
            )
            instanceRecord.referrals.update(
                {repo.name: ret}
            )  # type:ignore
            progressTotal.advance(taskTotal)
            progressTotal.advance(taskRepo)
            progressStat.advance(taskReferrals)

            # ? taks paths
            ret = instanceRQ(
                call="paths",
                args={"username": username, "repo": repo.name},
            )
            instanceRecord.paths.update({repo.name: ret})  # type:ignore
            progressTotal.advance(taskTotal)
            progressTotal.advance(taskRepo)
            progressStat.advance(taskPaths)

            # ? taks views
            ret = instanceRQ(
                call="views",
                args={"username": username, "repo": repo.name},
            )
            instanceRecord.views.update({repo.name: ret})  # type:ignore
            progressTotal.advance(taskTotal)
            progressTotal.advance(taskRepo)
            progressStat.advance(taskViews)

            # ? taks clones
            ret = instanceRQ(
                call="clones",
                args={"username": username, "repo": repo.name},
            )
            instanceRecord.clones.update({repo.name: ret})  # type:ignore
            progressTotal.advance(taskTotal)
            progressTotal.advance(taskRepo)
            progressStat.advance(taskClones)
            time.sleep(0.25)

        progressTotal.reset(
            taskRepo, description=f"[bold yellow]#Completed", completed=4
        )

    Console().print(instanceRecord)
