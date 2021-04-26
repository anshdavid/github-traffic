# -*- coding: utf-8 -*-

import argparse
import os.path

from run import main


def SanityCheck(args):

    if not os.path.exists(args.config):
        raise FileExistsError(f"unable to locate {args.config}")

    main(args=args)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="command line arguments")

    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="path to config with credentials",
    )

    parser.add_argument(
        "--api",
        type=str,
        required=False,
        default="all",
        help="api to call",
    )

    args = parser.parse_args()

    SanityCheck(args=args)