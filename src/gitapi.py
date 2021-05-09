import json
from typing import Dict, List, Optional, Union
from urllib import request
from urllib.request import Request, urlopen
from collections import OrderedDict, namedtuple

from .dataclass import *
from pprint import pprint


class APIRegister:
    def __init__(self) -> None:
        self.apiRegister: Dict[str, ntApi] = dict()
        self._preInit()

    def _preInit(self):
        """
        default registered api's
        """

        self.apiRegister = {
            "userInfo": ntApi(
                "%s/user",
                ["baseurl"],
                list(ntUserInfo._fields),
                ntUserInfo,  # type:ignore
            ),
            "repos": ntApi(
                "%s/users/%s/repos",
                ["baseurl", "username"],
                list(ntRepo._fields),
                ntRepo,  # type:ignore
            ),
            "referrers": ntApi(
                "%s/repos/%s/%s/traffic/popular/referrers",
                ["baseurl", "username", "repo"],
                list(ntReferral._fields),
                ntReferral,  # type:ignore
            ),
            "paths": ntApi(
                "%s/repos/%s/%s/traffic/popular/paths",
                ["baseurl", "username", "repo"],
                list(ntPath._fields),
                ntPath,  # type:ignore
            ),
            "views": ntApi(
                "%s/repos/%s/%s/traffic/views",
                ["baseurl", "username", "repo"],
                list(ntView._fields),
                ntView,  # type:ignore
            ),
            "clones": ntApi(
                "%s/repos/%s/%s/traffic/clones",
                ["baseurl", "username", "repo"],
                list(ntClone._fields),
                ntClone,  # type:ignore
            ),
        }

    def RegisterAPI(self, key: str, api: ntApi):
        if key in self.apiRegister.keys():
            print(f"{key} already registered")
        else:
            self.apiRegister.update({key: api})

    def GetAPI(self, key: str):
        return self.apiRegister.get(key, None)

    def GetAvailableAPI(self):
        return self.apiRegister.keys()

    def GetAPISignature(self, api):
        return self.apiRegister.get(api, None)


class RequestHandler:
    def __init__(
        self,
        username: str,
        token: str,
        register: APIRegister,
        baseurl: str = "https://api.github.com",
    ) -> None:

        self.username = username
        self.token = token
        self.baseurl = baseurl
        self.apiRegister = register
        self.kwargs_ = {"baseurl": self.baseurl, "username": self.username}

    def ApiRquest(self, url):
        req = request.Request(
            url,
            headers={"Authorization": "token %s" % self.token},
        )
        return json.load(request.urlopen(req))

    # ? making it a __call__ enables to be used as a decorator in the future!!
    def __call__(self, call, args: Dict) -> Union[NamedTuple, List[NamedTuple], None]:

        api = self.apiRegister.GetAPI(call)
        if api is None:
            print(f"api {call} not registered")
            return None

        self.kwargs_.update(args)
        flag: bool = True

        args_: List[Optional[str]] = list()
        for need in api.needs:
            need_ = self.kwargs_.get(need, None)
            if need_ is None:
                flag = False
                print(f"missing argument {need}")
            else:
                args_.append(need_)

        if flag:
            result = []

            response = self.ApiRquest(api.url % tuple(args_))

            if isinstance(response, list):
                result = list(
                    map(
                        lambda ddict: api.type(  # type:ignore
                            **dict(
                                filter(
                                    lambda kv: kv[0] in api.provides,
                                    ddict.items(),
                                )
                            )
                        ),
                        response,
                    )
                )
            else:
                result = api.type(  # type:ignore
                    **dict(
                        filter(
                            lambda elem: elem[0] in api.provides,
                            response.items(),
                        )
                    )
                )

            return result

        return None
