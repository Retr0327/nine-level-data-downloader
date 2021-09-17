import json
import asyncio
import pandas as pd
from typing import Optional, Dict, List, Union, Any, Callable
from dataclasses import dataclass
from .core import NineLevelDataDownloader, URLDialector


# --------------------------------------------------------------------
# helper functions


async def jsonify(data, file_name: str):
    """The jsonify method converts the argument `data` to a JSON file.

    Args:
        data (dict): the data that is going to be converted
        dialect_ch (str): the chinese name of a dialect
    """
    title = data["title"]
    level_id = data["level_id"]
    class_id = data["class_id"]
    ninelevel_data = data["data"]
    with open(
        f"{file_name} - {title} ({level_id}階{class_id}課).json", "w", encoding="utf-8"
    ) as file:
        json.dump(ninelevel_data, file, ensure_ascii=False)


async def tablize(data, file_name: str):
    """The tablize method converts the argument `data` to a CSV file.

    Args:
        data (dict): the data that is going to be converted
        dialect_ch (str): the chinese name of a dialect
    """
    title = data["title"]
    level_id = data["level_id"]
    class_id = data["class_id"]
    ninelevel_data = data["data"]
    df = pd.DataFrame(ninelevel_data)
    df.to_csv(
        f"{file_name} - {title} ({level_id}階{class_id}課).csv",
        index=False,
        encoding="utf_8_sig",
    )


# --------------------------------------------------------------------
# public interface


@dataclass
class NineLevel:
    """
    The NineLevel object download the data based on `dialect_ch`, `level_id` and `class_id`.
    """

    dialect_ch: str
    level_id: Optional[str] = None
    class_id: Optional[str] = None

    def __post_init__(self) -> None:
        self.dialector = URLDialector(
            self.dialect_ch, level_id=self.level_id, class_id=self.class_id
        )

    def download_data(self) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """The download_data method downloads the data.

        Returns:
            a dict if both `level_id` and `class_id` are specified, a list otherwise
        """
        return asyncio.run(NineLevelDataDownloader(self.dialector).download())

    def convert_data(self, convert_func: Callable) -> None:
        """The convert_data method converts the data by calling helper functions.

        Args:
            convert_func (Callable): the name of the helper function
        """
        ninelevel_data = self.download_data()
        if isinstance(ninelevel_data, dict):
            asyncio.run(convert_func(ninelevel_data, self.dialect_ch))
        else:
            multiple_data = asyncio.gather(
                *[convert_func(data, self.dialect_ch) for data in ninelevel_data]
            )

            asyncio.run(multiple_data)

    def to_json(self):
        """The to_json method converts the data to JSON."""
        return self.convert_data(jsonify)

    def to_csv(self):
        """The to_json method converts the data to csv."""
        return self.convert_data(tablize)
