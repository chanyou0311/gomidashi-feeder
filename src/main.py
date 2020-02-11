import base64
import os
import json
import datetime
import dataclasses
from enum import Enum, auto
from pytz import timezone

import requests
import pandas as pd
import numpy as np


JST = timezone("Asia/Tokyo")


class ContextInterface:
    event_id: str
    timestamp: str
    event_type: str
    resource: str


def hello_pubsub(event: dict, context: ContextInterface):
    if "data" in event:
        text = base64.b64decode(event["data"]).decode("utf-8")
    else:
        text = "Hello World!!"
    url = os.getenv("SLACK_WEBHOOK_URL")

    tommorow = datetime.datetime.now(tz=JST) + datetime.timedelta(days=1)
    garbage_schedule = GarbageSchedule(tommorow)
    if garbage_schedule.garbage_type == GarbageType.NON:
        return None
    message = f"<!channel> 明日のゴミは `{garbage_schedule.garbage_type.name}`  です"

    data = json.dumps({"text": message})
    response = requests.post(url, data=data)
    print(response.ok)


class GarbageType(Enum):
    BURNABLE = auto()
    NON_BURNABLE = auto()
    RECYCLE_PLASTIC = auto()
    OTHER_PLASTIC = auto()
    RECYCLABLE = auto()
    NON = auto()

    @staticmethod
    def create_from_name(name: str) -> "GarbageType":
        if name == "":
            return GarbageType.NON
        if name == "可燃":
            return GarbageType.BURNABLE
        if name == "不燃":
            return GarbageType.NON_BURNABLE
        if name == "リプラ":
            return GarbageType.RECYCLE_PLASTIC
        if name == "他プラ":
            return GarbageType.OTHER_PLASTIC
        if name == "資源":
            return GarbageType.RECYCLABLE
        raise Exception("不明なゴミ種別です。{}".format(name))


class GarbageSchedule:
    date: datetime.datetime
    garbage_type: GarbageType

    def __init__(self, dt: datetime.datetime):
        value = self.__get_garbage_type_value(dt)
        self.date = dt
        self.garbage_type = GarbageType.create_from_name(value)

    def __get_garbage_type_value(self, dt: datetime.datetime) -> str:
        header = self.__get_header_from_dt(dt)
        df = pd.read_csv("./gomi.csv")
        s = df[df["年月日"] == header]["8"]
        value = s.values[0]

        if value is np.nan:
            return ""
        return value

    def __get_header_from_dt(self, dt: datetime.datetime) -> str:
        return f"{dt.year}/{dt.month}/{dt.day}"

