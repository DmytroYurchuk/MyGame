from . import set_test_settings

from game import utils

def init(number):
    utils.clear_base()
    utils.set_players(number)

def test_player_one():
    init(1)
    player = utils.get_player(0)
    assert utils.get_player(99999) is None
    assert player.get("id") == 0
    assert len(player.get("tasks")) == 1
    assert player.get("tasks")[0].get("tasks") == []
    assert utils.task(999999, "task_5", 1000).get("modified") is False
    for i in range(4):
        assert utils.task(0, "task_{}".format(i), 1000).get("modified") is True
    assert len(utils.get_player(0).get("tasks")[0].get("tasks")) == 4
    assert utils.task(0, "task_5", 1000).get("modified") is False
    for i in range(4):
        assert utils.task(0, "task_{}".format(i), 1000, delete=True).get("modified") is True
    assert len(utils.get_player(0).get("tasks")[0].get("tasks")) == 0

def get_tasks_by_p_id(tasks, p_id):
    return [t for t in tasks if t.get("player_id") == p_id][0]

def test_player_many():
    init(100)
    player = utils.get_player(0)
    assert utils.get_player(99999) is None
    assert player.get("id") == 0
    assert len(player.get("tasks")) == 100
    assert get_tasks_by_p_id(player.get("tasks"), 0).get("tasks") == []
    assert utils.task(999999, "task_5", 1000).get("modified") is False
    for i in range(4):
        assert utils.task(0, "task_{}".format(i), 1000).get("modified") is True
        assert utils.task(1, "task_{}".format(i), 1000).get("modified") is True
    assert len(get_tasks_by_p_id(utils.get_player(0).get("tasks"), 0).get("tasks")) == 4
    assert utils.task(0, "task_5", 1000).get("modified") is False
    for i in range(4):
        assert utils.task(0, "task_{}".format(i), 1000, delete=True).get("modified") is True
    player = utils.get_player(0)
    assert len(get_tasks_by_p_id(player.get("tasks"), 1).get("tasks")) == 4
    assert get_tasks_by_p_id(player.get("tasks"), 0).get("tasks") == []
