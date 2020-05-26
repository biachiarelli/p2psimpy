from goald.quality.pragmatic.model.context import Context
from goald.quality.pragmatic.model.pragmatic import Pragmatic
from goald.quality.pragmatic.model.goal import Goal
from goald.quality.pragmatic.model.decomposition import Decomposition
from goald.quality.pragmatic.model.task import Task
from goald.quality.pragmatic.model.metric import Metric
from goald.quality.pragmatic.model.quality_constraint import QualityConstraint
from goald.quality.pragmatic.model.comparison import Comparison
from goald.quality.pragmatic.model.interpretation import Interpretation
from tests.utils.assert_util import assertPlan
from tests.test_data.mpers_metric import MpersMetrics
from tests.test_data.mpers_model import MpersModel
from goald.quality.common.planning.planning import Planning
import pytest

# Contexts
c1 = Context("c1")
c2 = Context("c2")
c3 = Context("c3")
c4 = Context("c4")

task1 = Task("task1")
task2 = Task("task2")
task3 = Task("task3")
task4 = Task("task4")

task1.addApplicableContext(c1)

task1.setProvidedQuality(None, MpersMetrics.SECONDS, 80)
task2.setProvidedQuality(None, MpersMetrics.SECONDS, 60)
task3.setProvidedQuality(None, MpersMetrics.SECONDS, 100)
task4.setProvidedQuality(None, MpersMetrics.SECONDS, 200)

goal = Pragmatic(Decomposition.OR, "g1")

goal.addDependency(task1)
goal.addDependency(task2)
goal.addDependency(task3)
goal.addDependency(task4)

qc1 = QualityConstraint(None, MpersMetrics.SECONDS, 180, Comparison.LESS_THAN)
qc2 = QualityConstraint(c2, MpersMetrics.SECONDS, 90, Comparison.LESS_THAN)
goal.interp.addQualityConstraint(qc1)
goal.interp.addQualityConstraint(qc2)


def test_C1():
    fullContext = [c1, c2, c3, c4]

    plan = Planning().isAchievable(goal, fullContext, goal.interp)

    assert plan is not None

    assert True is assertPlan(
        plan, [task2])
