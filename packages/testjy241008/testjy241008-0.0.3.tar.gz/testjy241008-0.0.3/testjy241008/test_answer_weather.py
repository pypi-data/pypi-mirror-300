import pytest
import answer_weather


def test_func():
    assert answer_weather.query("내일 서울 날씨는 어때?")
