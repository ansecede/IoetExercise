from exercise import getIntervalHours
"""
Cases:
['10:00', '10:15']
['10:00', '11:00']
['10:00', '12:00']
['20:00', '00:00']
['00:00', '01:00']
['00:00', '00:30']
"""
def test_getIntervalHours():
    assert getIntervalHours(['12:00', '18:15'], 6) == [12, 13, 14, 15, 16, 17, 18]
    assert getIntervalHours(['10:00', '10:15'], 0) == [10]
    assert getIntervalHours(['20:00', '00:00'], 4) == [20, 21, 22, 23, 0]
    assert getIntervalHours(['00:00', '01:00'], 1) == [0, 1]
    assert getIntervalHours(['00:00', '00:30'], 0) == [0]
    assert getIntervalHours(['22:00', '02:30'], 4) == [22, 23, 0, 1, 2]