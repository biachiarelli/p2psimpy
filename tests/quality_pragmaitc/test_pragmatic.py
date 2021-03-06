from goald.quality.common.model.context import Context
from goald.quality.common.model.quality_constraint import QualityConstraint
from goald.quality.common.model.common_metrics import CommonMetrics
from goald.quality.planning.pragmatic.pragmatic import Pragmatic
from goald.quality.common.model.comparison import Comparison
from goald.quality.common.model.decomposition import Decomposition


def test_shouldGetDifferentQualityConstraintsForDifferentContexts():
    aContext = Context("c1")
    anotherContext = Context("c2")

    aQC = QualityConstraint(aContext, CommonMetrics.METERS,
                            30, Comparison.LESS_OR_EQUAL_TO)
    anotherQC = QualityConstraint(
        anotherContext, CommonMetrics.METERS, 60, Comparison.LESS_OR_EQUAL_TO)

    goal = Pragmatic(Decomposition.AND, "G1")

    goal.interp.addQualityConstraint(aQC)
    goal.interp.addQualityConstraint(anotherQC)

    fullContext = []
    fullContext.append(aContext)

    assert aQC in goal.interp.getQualityConstraints(fullContext)

    anotherFullContext = []
    anotherFullContext.append(anotherContext)

    assert anotherQC in goal.interp.getQualityConstraints(anotherFullContext)
