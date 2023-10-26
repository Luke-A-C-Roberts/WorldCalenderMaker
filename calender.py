from dataclasses import dataclass
from typing import Optional
from pickle import dump, load

from colours import *
from tables import *

@dataclass
class Date:
    day  : int
    month: int
    year : int


class DateSystem:
    def __init__(self, month_names: list[str], month_lengths: list[int]) -> None:
        try   : assert len(month_lengths) == len(month_names)
        except: ValueError(
            "DateSystem lengths of \"month_names\" and \"month_lengths\" must be equal"
        )
        self.month_names = month_names
        self.month_lengths = month_lengths

    def valid_date(self, date: Date) -> bool:
        if date.month - 1 >= len(self.month_names): return False
        if self.day - 1 >= self.month_lengths[date.month - 1]: return False
        return True

    def represent_date(self, date: Date) -> str:
        try   : assert self.valid_date(date)
        except: ValueError("The date inputted is not valid")
        return f"{date.day} of {self.month_names[date.month - 1]}, {date.year}"


@dataclass(repr=False)
class Tag:
    name  : str
    colour: str

    def __repr__(self) -> str:
        return colourise(self.name, self.colour)


@dataclass
class Event:
    date       : Date
    name       : str
    tags       : Optional[list[Tag]]
    description: Optional[str]
    colour     : str = "none"

    def make_row(self) -> tuple[Date, str, Optional[list[Tag]], Optional[str]]:
        return (
            self.date,
            colourise(self.name, self.colour),
            self.tags if self.tags else None,
            self.description if self.description else None
        )


@dataclass(repr=False)
class Calender:
    date_system: DateSystem
    events     : list[Event]

    def event(self, index: int) -> Event:
        assert 0 <= index < len(self.events)
        return self.events[index]

    def __repr__(self) -> str:
        headings = ["Date", "Name", "Tags", "Description"]
        table_rows = []
        for event in self.events:
            (date, name, tags, description) = event.make_row()
            date = self.date_system.represent_date(date)

            if not tags:
                tags = ""
            else:
                temp_tags = ""
                for tag in tags:
                    temp_tags += colourise(tag.name, tag.colour) + " "
                tags = temp_tags

            if not description:
                description = ""

            table_rows.append([date, name, tags, description])

        return(repr(unicode_table(headings, table_rows)))


def save_calender(calander: Calender, path: str) -> None:
    dump(calander, path)


event1 = Event(Date(10, 4, 16), "Olmuk", [Tag("festival", "red")], "a festival of fire", "yellow")
event2 = Event(Date(2, 3, 18), "Tuurunid", [Tag("festival", "red")], "a festival of water", "blue")
months = {
    "Armrok":20,
    "Tenuli":43,
    "Sampirin":25,
    "Yavil":40,
    "Goru":30,
    "Tuhu":28,
    "Kaibaiz":32,
    "Hajimu":33,
    "Dexuur":43,
    "Cxholu":22
}
date_system = DateSystem(list(months.keys()), list(months.values()))
calander = Calender(date_system, [event1, event2])
print(repr(calander))