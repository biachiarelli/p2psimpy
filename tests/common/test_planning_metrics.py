from goald.quality.common.model.context import Context
from goald.quality.common.model.goal import Goal
from goald.quality.common.model.decomposition import Decomposition
from goald.quality.common.model.task import Task
from goald.quality.common.model.metric import Metric
from goald.quality.common.model.quality_constraint import QualityConstraint
from goald.quality.common.model.comparison import Comparison
from goald.quality.common.model.interpretation import Interpretation
from tests.utils.assert_util import assertPlan
from tests.test_data.mpers_metric import MpersMetrics
from tests.test_data.mpers_model import MpersModel
from goald.quality.planning.pragmatic.pragmatic import Pragmatic
from goald.quality.planning.optimized_planning import Planning

import pytest

# Contexts
c1 = Context("c1")
c2 = Context("c2")
c3 = Context("c3")
c4 = Context("c4")

task1 = Task("task1")
task2 = Task("task2")
task3 = Task("task3")

task2.addApplicableContext(c2)

task1.setProvidedQuality(None, MpersMetrics.SECONDS, 30)
task1.setProvidedQuality(None, MpersMetrics.ERROR, 30)
task2.setProvidedQuality(None, MpersMetrics.SECONDS, 70)
task2.setProvidedQuality(None, MpersMetrics.ERROR, 10)
task3.setProvidedQuality(None, MpersMetrics.SECONDS, 10)
task3.setProvidedQuality(None, MpersMetrics.ERROR, 70)

goal = Pragmatic(Decomposition.OR, "g1")

goal.addDependency(task1)
goal.addDependency(task2)
goal.addDependency(task3)

qc1 = QualityConstraint(None, MpersMetrics.SECONDS, 100, Comparison.LESS_THAN)
qc1 = QualityConstraint(None, MpersMetrics.ERROR, 90, Comparison.LESS_THAN)
qc2 = QualityConstraint(c2, MpersMetrics.SECONDS, 40, Comparison.LESS_THAN)
qc3 = QualityConstraint(c4, MpersMetrics.ERROR, 40, Comparison.LESS_THAN)

goal.interp.addQualityConstraint(qc1)
goal.interp.addQualityConstraint(qc2)
goal.interp.addQualityConstraint(qc3)

def test_error():
    fullContext = [c1, c2, c4]

    plan = Planning().isAchievable(goal, fullContext, goal.interp)

    assert plan is not None

    assert True is assertPlan(plan, [task1])


def test_faster():
    fullContext = [c1, c3, c2]

    plan = Planning().isAchievable(goal, fullContext, goal.interp)

    assert plan is not None

    assert True is assertPlan(plan, [task1])


def test_better():
    fullContext = [c1, c3, c4, c2]

    plan = Planning().isAchievable(goal, fullContext, goal.interp)

    assert plan is not None

    assert True is assertPlan(plan, [task1])
