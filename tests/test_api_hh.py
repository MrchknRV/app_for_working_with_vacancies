from unittest.mock import patch

from requests import Response

from src.api_hh import HH
from src.base_classes import HeadHunterAPI


def test_hh_initialization():
    """Проверяет корректность инициализации класса HH."""
    hh = HH()
    assert hh._HH__url == "https://api.hh.ru/vacancies"
    assert hh._HH__params == {"text": "", "page": 0, "per_page": 100, "area": ["113"]}
    assert isinstance(hh, HeadHunterAPI)


@patch("requests.get")
def test_connect(mock_get):
    hh = HH()
    response = Response()
    response.status_code = 200
    mock_get.return_value = response
    mock_get.return_value.status_code = response.status_code
    assert hh._api_connect("test") == response
    mock_get.assert_called_once()
