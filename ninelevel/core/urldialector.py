import re
from enum import Flag
from typing import Optional, Dict, List, Union
from urllib.parse import urljoin
from dataclasses import dataclass, asdict


__all__ = ["NineLevelDialect", "URLDialector"]


# --------------------------------------------------------------------
# global varables


BASE_URL = "http://web.klokah.tw/ninew/php/"


# --------------------------------------------------------------------
# base class


class NineLevelInfo(Flag):
    @classmethod
    def get_info_dict(cls) -> Dict[str, int]:
        """The get_info_dict method converts the infromation to a dict.

        Returns:
            a dict
        """
        return {k: v.value for k, v in cls.__members__.items()}

    @classmethod
    def get_info(cls) -> List[str]:
        """The get_info method converts the information to a list.

        Returns:
            a list
        """
        return [k for k, v in cls.__members__.items()]


class NineLevelDialect(NineLevelInfo):
    卡那卡那富語 = 33
    撒奇萊雅語 = 38
    雅美語 = 29
    南王卑南語 = 3
    知本卑南語 = 2
    西群卑南語 = 1
    建和卑南語 = 4
    鄒語 = 32
    噶瑪蘭語 = 31
    太魯閣語 = 44
    東魯凱語 = 15
    霧台魯凱語 = 14
    大武魯凱語 = 41
    多納魯凱語 = 35
    茂林魯凱語 = 37
    萬山魯凱語 = 36
    東排灣語 = 11
    北排灣語 = 12
    中排灣語 = 13
    南排灣語 = 10
    卓群布農語 = 6
    卡群布農語 = 7
    丹群布農語 = 8
    巒群布農語 = 9
    郡群布農語 = 5
    都達語 = 22
    德固達雅語 = 20
    德路固語 = 21
    邵語 = 30
    賽考利克泰雅語 = 16
    澤敖利泰雅語 = 17
    汶水泰雅語 = 18
    萬大泰雅語 = 19
    宜蘭澤敖利泰雅語 = 42
    四季泰雅語 = 43
    秀姑巒阿美語 = 23
    南勢阿美語 = 24
    海岸阿美語 = 25
    馬蘭阿美語 = 26
    恆春阿美語 = 27
    賽夏語 = 28
    拉阿魯哇語 = 34


@dataclass
class URLCreator:
    """
    The URLCreator object converts the given dialecdt name to its corresponding url.
    """

    dialect_ch: str

    def __post_init__(self) -> None:
        self.dialect_id = NineLevelDialect[self.dialect_ch].value

    def merge_with_level_ids(self, level_id: int) -> str:
        """The merge_with_level_ids method combine the base url with `self.dialect_id` and `level_id` to form another url.

        Returns:
            a str
        """
        return urljoin(BASE_URL, f"getTextNew.php?d={self.dialect_id}&l={level_id}")

    def merge_with_class_ids(
        self, list_of_class_ids: list, url_with_level_ids: list
    ) -> List[str]:
        """The merge_with_class_ids method merge list of class ids with list of urls that have level ids

        Returns:
            a list
        """
        return [
            f"{url}&c={id_value}"
            for id_value in list_of_class_ids
            for url in url_with_level_ids
        ]

    def create(self) -> List[str]:
        """The create method creates the url.

        Returns:
            a list: [
                'http://web.klokah.tw/ninew/php/getTextNew.php?d=14&l=1&c=1',
                'http://web.klokah.tw/ninew/php/getTextNew.php?d=14&l=2&c=1',
                'http://web.klokah.tw/ninew/php/getTextNew.php?d=14&l=3&c=1',
                ...
            ]
        """
        list_of_level_ids = [*range(1, 10)]
        list_of_class_ids = [*range(1, 11)]
        url_with_level_ids = map(self.merge_with_level_ids, list_of_level_ids)
        return self.merge_with_class_ids(list_of_class_ids, list(url_with_level_ids))


# --------------------------------------------------------------------
# public interface


@dataclass
class URLDialectorInfo:
    """
    The URLDialectorInfo object keeps track of an item in inventory, including id, dialect name, level id, class id and url.
    """

    dialect_name: str
    level_id: str
    class_id: str
    url: str


@dataclass
class URLDialector:
    """
    The URLDialector object allows the user to type the dialect name, level id and class id. Then, it generates the
    request information.
    """

    dialect_ch: str
    level_id: Optional[str] = None
    class_id: Optional[str] = None

    def create_list_of_urls(self) -> List[str]:
        """The create_list_of_urls method creates a list of urls based on the dialect name (i.e. `dialect_ch`).

        Returns:
            a list
        """
        return URLCreator(self.dialect_ch).create()

    def generate_request_info(self, url: str):
        """The generate_request_info method generates the request info based on the url.

        Args:
            url (str): the url that carries the major info

        Returns:
            a dict: {
                'dialect_name': '霧台魯凱語',
                'level_id': '1',
                'class_id': '1',
                'url': 'http://web.klokah.tw/ninew/php/getTextNew.php?d=14&l=1&c=1'
            }
        """
        specified_level_id = re.findall("""(?<=\&l\=)\d*""", url)[0]
        specified_class_id = re.findall("""(?<=\&c\=)\d*""", url)[0]
        data = URLDialectorInfo(
            dialect_name=self.dialect_ch,
            level_id=specified_level_id,
            class_id=specified_class_id,
            url=url,
        )
        return asdict(data)

    def find_particular_level(
        self, list_of_request_info: list, level_id: int
    ) -> List[Dict[str, str]]:
        """The find_particular_level method finds the request info based on the `level id`.

        Args:
            list_of_request_info (list): the list that carries all the request info
            level_id (int): the level id that the user specifies

        Returns:
            a list: [
                {
                    'dialect_name': '霧台魯凱語',
                    'level_id': '1',
                    'class_id': '1',
                    'url': 'http://web.klokah.tw/ninew/php/getTextNew.php?d=14&l=1&c=1'
                },
                {
                    'dialect_name': '霧台魯凱語',
                    'level_id': '1',
                    'class_id': '2',
                    'url': 'http://web.klokah.tw/ninew/php/getTextNew.php?d=14&l=1&c=2'
                },
                ...
            ]
        """
        return [
            request_info
            for request_info in list_of_request_info
            if request_info["level_id"] == str(level_id)
        ]

    def find_particular_level_and_class(
        self, list_of_request_info: list, level_id: int, class_id: int
    ) -> Dict[str, str]:
        """The find_particular_level_and_class method finds the request info based on `level_id` and `class_id`.

        Args:
            list_of_request_info (list): the list that carries all the request info
            level_id (int): the level id that the user specifies
            class_id (int): the class id that the user specifies

        Returns:
            a dict: {
                'dialect_name': '霧台魯凱語',
                'level_id': '2',
                'class_id': '4',
                'url': 'http://web.klokah.tw/ninew/php/getTextNew.php?d=14&l=2&c=4'
            }

        """
        for request_info in list_of_request_info:
            if request_info["level_id"] == str(level_id) and request_info[
                "class_id"
            ] == str(class_id):
                return request_info

    def generate(self) -> Union[List[Dict[str, str]], Dict[str, str]]:
        """The generate method generally generates all the request info. Once the class argument `level id` or
           `class id` is specified, the chosen request information will be selected from the list.

        Returns:
            a list or a dict
        """
        list_of_urls = self.create_list_of_urls()
        list_of_request_info = list(map(self.generate_request_info, list_of_urls))
        if isinstance(self.level_id, int) and self.class_id is None:
            return self.find_particular_level(list_of_request_info, self.level_id)
        if isinstance(self.level_id, int) and isinstance(self.level_id, int):
            return self.find_particular_level_and_class(
                list_of_request_info, self.level_id, self.class_id
            )
        return list_of_request_info
