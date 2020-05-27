from goald.quality.common.model.plan import Plan
from goald.quality.common.model.task import Task


def test_plan():
    task1 = Task("t1")
    task2 = Task("t2")
    task3 = Task("t3")

    plan1 = Plan(task1)
    plan2 = Plan(task2)
    plan3 = Plan(task3)

    plan1.add(plan2)
    plan2.add(plan1)

    plan3.addTask(task2)

    assert set(plan1.getTasks()) == set(plan2.getTasks())
    assert set(plan3.getTasks()) != set(plan2.getTasks())


    
