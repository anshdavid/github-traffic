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

ntRepos = NamedTuple(
    "ntRepos",
    [
        ("name", str),
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