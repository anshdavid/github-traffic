from typing import List, NamedTuple, Tuple

ntReferral = NamedTuple(
    "ntReferral",
    [
        ("referrer", str),
        ("count", int),
        ("uniques", int),
    ],
)

ntPath = NamedTuple(
    "ntPath",
    [
        ("path", str),
        ("title", str),
        ("count", int),
        ("uniques", int),
    ],
)

ntView = NamedTuple(
    "ntView",
    [
        ("count", int),
        ("uniques", int),
    ],
)

ntClone = NamedTuple(
    "ntClone",
    [
        ("count", int),
        ("uniques", int),
    ],
)

ntRepo = NamedTuple(
    "ntRepo",
    [
        ("name", str),
        ("stargazers_count", int),
        ("forks_count", int),
    ],
)

ntUserInfo = NamedTuple(
    "ntUserInfo",
    [
        ("followers", int),
        ("following", int),
        ("public_repos", int),
        # ("total_private_repos", int),
    ],
)

ntApi = NamedTuple(
    "ntApi",
    [
        ("url", str),
        ("needs", List[str]),
        ("provides", List[str]),
        ("type", NamedTuple),
    ],
)