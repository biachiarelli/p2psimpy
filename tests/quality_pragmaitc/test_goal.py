from goald.quality.common.model.task import Task
from goald.quality.common.model.goal import Goal
from goald.quality.common.model.context import Context
from goald.quality.common.model.delegation import Delegation
from goald.quality.common.model.decomposition import Decomposition
from goald.quality.planning.pragmatic.pragmatic_planning import PragmaticPlanning


def test_shouldGetDependencies():
    root = Goal(Decomposition.AND, "root")

    task = Task("T1")
    goal = Goal(Decomposition.AND, "G1")
    delegation = Delegation("D1")

    root.addDependency(task)
    root.addDependency(goal)
    root.addDependency(delegation)

    deps = []
    deps.append(delegation)
    deps.append(goal)
    deps.append(task)

    for d in deps:
        assert d in root.dependencies


def test_shouldBeAchievable():
    root = Goal(Decomposition.AND, "root")

    context = Context("c1")
    current = []
    current.append(context)

    task1 = Task("t1")
    task2 = Task("t2")

    task1.addApplicableContext(context)

    root.addDependency(task1)
    root.addDependency(task2)

    plan = PragmaticPlanning().isAchievable(root, current, None)
    assert plan

    assert task2 in plan.getTasks()


def test_shouldBeUnachievable():
    root = Goal(Decomposition.AND, "root")

    context1 = Context("c1")
    context2 = Context("c2")

    current = []
    current.append(context1)

    task1 = Task("T1")
    task2 = Task("T2")

    task1.addApplicableContext(context2)
    task2.addApplicableContext(context2)

    root.addDependency(task1)
    root.addDependency(task2)

    deps = []
    deps.append(task1)
    deps.append(task2)

    plan = PragmaticPlanning().isAchievable(root, current, None)

    assert plan is None


def test_shouldGetApplicableDependencies():
    root = Goal(Decomposition.AND, "root")

    context = Context("c1")
    current = []
    current.append(context)

    task = Task("t1")
    goal = Goal(Decomposition.AND, "g1")
    delegation = Delegation("D1")

    task.addApplicableContext(context)

    root.addDependency(task)
    root.addDependency(goal)
    root.addDependency(delegation)

    deps = []
    deps.append(task)

    assert 1 == len(deps)
    assert task in deps
