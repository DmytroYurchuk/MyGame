from . import set_test_settings

from game import utils

def test_init(number=10):
    pl_l, pl_d = utils.generate_players(number)
    assert len(pl_l) == number
    assert len(pl_d.keys()) == number

    assert utils.set_players(10000).get("created") is False

    utils.clear_base()
    assert utils.set_players(number).get("created") is True

def test_players_100():
    test_init(100)
    assert len(utils.get_players().get("players")) == 100

