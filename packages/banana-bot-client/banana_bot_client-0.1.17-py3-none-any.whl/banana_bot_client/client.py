import time

import requests

from .constants import (
    ACHIEVE_QUEST_API_URL,
    BANANA_LIST_API_URL,
    CLAIM_ADS_INCOME_API_URL,
    CLAIM_LOTTERY_API_URL,
    CLAIM_QUEST_API_URL,
    CLAIM_QUEST_LOTTERY_API_URL,
    DO_CLICK_API_URL,
    DO_LOTTERY_API_URL,
    DO_SPEEDUP_API_URL,
    EQUIP_BANANA_API_URL,
    LOTTERY_INFO_API_URL,
    QUEST_LIST_API_URL,
    SELL_BANANA_API_URL,
    USER_ADS_INFO_API_URL,
    USER_INFO_API_URL,
)
from .encrypt import encrypt_request_time
from .exceptions import ClaimIncompleteQuestError, UnknownBananaRequestError
from .models import (
    BananaListModel,
    ClaimAdsIncomeModel,
    ClaimQuestModel,
    ClickRewardModel,
    DoLotteryModel,
    LotteryInfoModel,
    QuestListModel,
    SellBananaResponseModel,
    SpeedupResponseModel,
    UserAdsInfoModel,
    UserInfoModel,
)


class BananaBotClient:
    def __init__(self, token: str, headers: None | dict = None):
        self.token = token
        self.headers = headers

    @property
    def default_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def _make_request(self, method: str, url: str, proxies=None, **kwargs):
        """
        expected proxies: https://stackoverflow.com/questions/8287628/proxies-with-python-requests-module
        """
        request_headers = self.default_headers.copy()
        if self.headers:
            request_headers.update(self.headers)
        request_headers["Request-Time"] = encrypt_request_time()

        response = requests.request(
            method,
            url,
            headers=request_headers,
            proxies=proxies,
            timeout=20,
            verify=False if proxies else True,
            **kwargs,
        )
        response.raise_for_status()
        response_json = response.json()
        # TODO: expend the error handling
        if response_json["code"] != 0 or response_json["msg"] != "Success":
            if response_json["code"] == 4404:
                raise ClaimIncompleteQuestError(response_json["msg"])
            code = response_json["code"]
            msg = response_json["msg"]
            raise UnknownBananaRequestError(f"code: {code}, msg: {msg}")
        return response_json["data"]

    def get_lottery_info(self, proxies=None) -> LotteryInfoModel:
        data = self._make_request("GET", LOTTERY_INFO_API_URL, proxies=proxies)
        return LotteryInfoModel(**data)

    def do_lottery(self, proxies=None) -> DoLotteryModel:
        """
        harvest and reveal a banana
        """
        data = self._make_request("POST", DO_LOTTERY_API_URL, proxies=proxies)
        return DoLotteryModel(**data)

    def claim_lottery(self, proxies=None) -> None:
        """
        claim a banana once the countdown is done
        """
        _ = self._make_request(
            "POST",
            CLAIM_LOTTERY_API_URL,
            proxies=proxies,
            json={"claimLotteryType": 1},
        )
        return None  # Since the response data is None, just return None

    def get_quest_list(self, proxies=None) -> QuestListModel:
        data = self._make_request("GET", QUEST_LIST_API_URL, proxies=proxies)
        return QuestListModel(**data)

    def achieve_quest(self, quest_id: int, proxies=None) -> None:
        """
        complete a request
        """
        _ = self._make_request(
            "POST",
            ACHIEVE_QUEST_API_URL,
            proxies=proxies,
            json={"quest_id": quest_id},
        )
        return None  # Since the response data is None, just return None

    def claim_quest(self, quest_id: int, proxies=None) -> ClaimQuestModel:
        """
        claim rewards for a completed quest
        """
        data = self._make_request(
            "POST",
            CLAIM_QUEST_API_URL,
            proxies=proxies,
            json={"quest_id": quest_id},
        )
        return ClaimQuestModel(**data)

    def claim_quest_lottery(self, proxies=None) -> None:
        """
        claim additional banana for every completed 3 quests
        """
        _ = self._make_request("POST", CLAIM_QUEST_LOTTERY_API_URL, proxies=proxies)
        return None  # Since the response data is None, just return None

    def click(self, click_count: int, proxies=None) -> ClickRewardModel:
        data = self._make_request(
            "POST",
            DO_CLICK_API_URL,
            proxies=proxies,
            json={"clickCount": click_count},
        )
        return ClickRewardModel(**data)

    def get_user_info(self, proxies=None) -> UserInfoModel:
        data = self._make_request("GET", USER_INFO_API_URL, proxies=proxies)
        return UserInfoModel(**data)

    def get_banana_list(self, proxies=None) -> BananaListModel:
        data = self._make_request("GET", BANANA_LIST_API_URL, proxies=proxies)
        return BananaListModel(**data)

    def equip_banana(self, banana_id: int, proxies=None) -> None:
        _ = self._make_request(
            "POST",
            EQUIP_BANANA_API_URL,
            proxies=proxies,
            json={"bananaId": banana_id},
        )
        return None

    def sell_banana(
        self, banana_id: int, quantity: int, proxies=None
    ) -> SellBananaResponseModel:
        data = {"bananaId": banana_id, "sellCount": quantity}
        response_data = self._make_request(
            "POST", SELL_BANANA_API_URL, proxies=proxies, json=data
        )
        return SellBananaResponseModel(**response_data)

    def do_speedup(self, proxies=None) -> SpeedupResponseModel:
        response_data = self._make_request("POST", DO_SPEEDUP_API_URL, proxies=proxies)
        return SpeedupResponseModel(**response_data)

    def get_user_ads_info(self, proxies=None) -> UserAdsInfoModel:
        response_data = self._make_request(
            "GET", USER_ADS_INFO_API_URL, proxies=proxies
        )
        return UserAdsInfoModel(**response_data)

    def claim_ads_income(self, claim_type: int, proxies=None) -> ClaimAdsIncomeModel:
        """
        set claim_type = 1 when claiming at do speed up
        set claim_type = 2 when claiming at do lottery
        """
        response_data = self._make_request(
            "POST",
            CLAIM_ADS_INCOME_API_URL,
            proxies=proxies,
            json={"type": claim_type},
        )
        return ClaimAdsIncomeModel(**response_data)
