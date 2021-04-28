from configparser import ConfigParser
from src.display import TrafficProgress
import time
from typing import Dict

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from src.dataclass import *
from src.gitapi import APIRegister, RequestHandler
from src.record import Record


def main(args):

    # * setup traffic

    config = ConfigParser()

    config.read_file(open(args.config))

    username = config.get("github", "username")
    token = config.get("github", "token")

    instanceRecord = Record()

    instanceRQ = RequestHandler(
        username=username, token=token, register=APIRegister()
    )

    # ! might display on header panel
    userInfo = instanceRQ(
        call="userInfo",
        args={},
    )
    print("----", userInfo)

    # * init from here

    repos = instanceRQ(
        call="repos",
        args={"username": username},
    )

    assert isinstance(repos, list)

    instanceConsole = TrafficProgress(numRepos=len(repos))

    instanceConsole.progressTotal.console.print(
        Panel(
            f"[bold blue] Github-Traffic v0.2.0",
            border_style="violet",
            padding=1,
        ),
    )

    # * start fetch

    with Live(
        instanceConsole.progressTable,
        refresh_per_second=144,
        console=Console(),
    ):
        for repo in repos:

            assert isinstance(repo, ntRepo)

            instanceConsole.UpdateRepoDescription(repo.name)

            # ? basic info
            instanceConsole.UpdateStatDescription("info")
            instanceRecord.info.update({repo.name: repo})
            instanceConsole.StepTotal()
            instanceConsole.StepStat()

            # ? taks referrals
            ret = instanceRQ(
                call="referrers",
                args={"repo": repo.name},
            )
            instanceConsole.UpdateStatDescription("referrers")
            instanceRecord.referrals.update(
                {repo.name: ret}
            )  # type:ignore
            instanceConsole.StepTotal()
            instanceConsole.StepStat()

            # ? taks paths
            ret = instanceRQ(
                call="paths",
                args={"repo": repo.name},
            )
            instanceConsole.UpdateStatDescription("paths")
            instanceRecord.paths.update({repo.name: ret})  # type:ignore
            instanceConsole.StepTotal()
            instanceConsole.StepStat()

            # ? taks views
            ret = instanceRQ(
                call="views",
                args={"repo": repo.name},
            )
            instanceConsole.UpdateStatDescription("views")
            instanceRecord.views.update({repo.name: ret})  # type:ignore
            instanceConsole.StepTotal()
            instanceConsole.StepStat()

            # ? taks clones
            ret = instanceRQ(
                call="clones",
                args={"repo": repo.name},
            )
            instanceConsole.UpdateStatDescription("clones")
            instanceRecord.clones.update({repo.name: ret})  # type:ignore
            instanceConsole.StepTotal()
            instanceConsole.StepStat()

            instanceConsole.ResetStatProgress()
            instanceConsole.StepRepo()

        instanceConsole.UpdateRepoDescription("Fetched")
        instanceConsole.CompleteStat()

    Console().print(instanceRecord)
