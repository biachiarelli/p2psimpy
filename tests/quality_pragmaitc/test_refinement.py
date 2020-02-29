from goald.quality.pragmatic.model.refinement import Refinement
from goald.quality.pragmatic.model.task import Task
from goald.quality.pragmatic.model.delegation import Delegation
from goald.quality.pragmatic.model.decomposition import Decomposition
from goald.quality.pragmatic.model.context import Context
from goald.quality.pragmatic.model.common_metrics import CommonMetrics
from goald.quality.pragmatic.model.decomposition import Decomposition
from goald.quality.pragmatic.model.goal import Goal
from goald.quality.pragmatic.model.interpretation import Interpretation
from goald.quality.pragmatic.model.quality_constraint import QualityConstraint
from goald.quality.pragmatic.model.comparison import Comparison
from goald.quality.pragmatic.model.pragmatic import Pragmatic


def test_refinement():
    refinement = Refinement()
    task = Task("T1")
    delegation = Delegation("D1")
    goal = Goal(Decomposition.AND, "G1")

    assert task.myType() is refinement.TASK
    assert delegation.myType() is refinement.DELEGATION
    assert goal.myType() is refinement.GOAL


def test_shouldBeApplicable():
    goal = Goal(Decomposition.AND, "G1")
    task = Task("T1")
    delegation = Delegation("D1")

    contextCurrent = Context("C1")
    fullContext = []

    fullContext.append(contextCurrent)

    goal.addApplicableContext(contextCurrent)
    task.addApplicableContext(contextCurrent)
    delegation.addApplicableContext(contextCurrent)

    assert True is goal.isApplicable(fullContext)
    assert True is task.isApplicable(fullContext)
    assert True is delegation.isApplicable(fullContext)


def test_shouldBeNotApplicable():
    goal = Goal(Decomposition.AND, "G1")
    task = Task("T1")
    delegation = Delegation("D1")

    context = Context("C1")

    task.addApplicableContext(context)

    goal.addApplicableContext(context)

    delegation.addApplicableContext(context)

    wrongContext = Context("C2")
    fullContext = []
    fullContext.append(wrongContext)

    assert False is goal.isApplicable(fullContext)
    assert False is task.isApplicable(fullContext)
    assert False is delegation.isApplicable(fullContext)


def test_aTaskShouldBeAchievable():
    task = Task("T1")

    currentContext = Context("C1")
    fullContext = []
    fullContext.append(currentContext)

    qc = QualityConstraint(
        currentContext, CommonMetrics.SECONDS, 15, Comparison.LESS_OR_EQUAL_TO)

    task.addApplicableContext(currentContext)
    task.setProvidedQuality(currentContext, CommonMetrics.SECONDS, 12)

    interp = Interpretation()
    interp.addQualityConstraint(qc)

    assert task in task.isAchievable(
        fullContext, interp).getTasks()


def aTaskMayNotBeAchievable():
    task = Task("T1")

    current = Context("C1")
    fullContext = []
    fullContext.append(current)

    qc = QualityConstraint(current, CommonMetrics.SECONDS, 15, Comparison.LESS_OR_EQUAL_TO)

    task.addApplicableContext(current)
    task.setProvidedQuality(current, CommonMetrics.SECONDS, 16)

    interp = Interpretation()
    interp.addQualityConstraint(qc)

    assert task.isAchievable(fullContext, interp) is None


def test_shouldAddSeveralContextsAtOnce():
    context1 = Context("C1")
    context2 = Context("C2")

    task = Task("T1")

    assert task.applicableContext is None

    task.addApplicableContext([context1, context2])

    assert 2 == len(task.applicableContext)


def test_aNonApplicableRootGoalIsNotAchievable():
    goal = Goal(Decomposition.AND, "G1")
    current = Context("C1")
    fullContext = []

    qc = QualityConstraint(current, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)
    goal.addApplicableContext(Context("C2"))

    interp = Interpretation()
    interp.addQualityConstraint(qc)

    assert goal.isAchievable(fullContext, interp) is None


def test_aGoalWithATaskMayBeAchievable():
    goal = Goal(Decomposition.AND, "Root")

    task = Task("T1")

    current = Context("C1")
    fullContext = []
    fullContext.append(current)

    qc = QualityConstraint(current, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)
    interp = Interpretation()
    interp.addQualityConstraint(qc)

    task.addApplicableContext(current)
    task.setProvidedQuality(current, CommonMetrics.SECONDS, 13)

    goal.addDependency(task)
    goal.addApplicableContext(current)

    plan = goal.isAchievable(fullContext, interp)
    assert len(plan.getTasks()) == 1


def test_aGoalAndDecomposedWithTwoTasksMayBeAchievable():
    goal = Goal(Decomposition.AND, "Root")

    task1 = Task("T1")
    task2 = Task("T2")

    current = Context("C1")
    fullContext = []
    fullContext.append(current)

    qc = QualityConstraint(current, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)

    interp = Interpretation()
    interp.addQualityConstraint(qc)

    task1.addApplicableContext(current)
    task1.setProvidedQuality(current, CommonMetrics.SECONDS, 13)

    task2.addApplicableContext(current)
    task2.setProvidedQuality(current, CommonMetrics.SECONDS, 11)

    goal.addDependency(task1)
    goal.addDependency(task2)

    goal.addApplicableContext(current)

    plan = goal.isAchievable(fullContext, interp)
    assert 2 == len(plan.getTasks())


def test_aGoalAndDecomposedWithTwoTasksMayNotBeAchievable():
    goal = Goal(Decomposition.AND, "Root")

    task1 = Task("T1")
    task2 = Task("T2")

    current = Context("C1")
    fullContext = []
    fullContext.append(current)

    qc = QualityConstraint(current, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)

    task1.addApplicableContext(current)
    task1.setProvidedQuality(current, CommonMetrics.SECONDS, 16)

    task2.addApplicableContext(current)
    task2.setProvidedQuality(current, CommonMetrics.SECONDS, 11)

    goal.addDependency(task1)
    goal.addDependency(task2)

    goal.addApplicableContext(current)

    interp = Interpretation()
    interp.addQualityConstraint(qc)

    plan = goal.isAchievable(fullContext, interp)

    assert plan is None


def test_aGoalOrDecomposedWithTwoTasksMayBeAchievable():
    goal = Goal(Decomposition.OR, "Root")
    assert goal.decomposition

    task1 = Task("T1")
    task2 = Task("T2")

    current = Context("C1")
    fullContext = []
    fullContext.append(current)

    qc = QualityConstraint(current, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)

    task1.addApplicableContext(current)
    task1.setProvidedQuality(current, CommonMetrics.SECONDS, 13)

    task2.addApplicableContext(current)
    task2.setProvidedQuality(current, CommonMetrics.SECONDS, 11)

    goal.addDependency(task1)
    goal.addDependency(task2)

    goal.addApplicableContext(current)

    interp = Interpretation()
    interp.addQualityConstraint(qc)

    plan = goal.isAchievable(fullContext, interp)
    assert len(plan.getTasks()) == 1


def test_aGoalOrDecomposedWithTwoTasksMayBeAchievableAtOnlyOneBranch():
    goal = Goal(Decomposition.OR, "Root")
    assert goal.decomposition

    task1 = Task("T1")
    task2 = Task("T2")

    current = Context("C1")
    fullContext = []
    fullContext.append(current)

    qc = QualityConstraint(current, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)

    task1.addApplicableContext(current)
    task1.setProvidedQuality(current, CommonMetrics.SECONDS, 16)

    task2.addApplicableContext(current)
    task2.setProvidedQuality(current, CommonMetrics.SECONDS, 11)

    goal.addDependency(task1)
    goal.addDependency(task2)

    goal.addApplicableContext(current)

    interp = Interpretation()
    interp.addQualityConstraint(qc)

    plan = goal.isAchievable(fullContext, interp)
    assert task2 in plan.getTasks()
    assert task1 not in plan.getTasks()


def test_aGoalOrDecomposedWithTwoTasksMayNotBeAchievable():
    goal = Goal(Decomposition.OR, "Root")

    task1 = Task("T1")
    task2 = Task("T2")
    current = Context("C1")
    fullContext = []
    fullContext.append(current)

    qc = QualityConstraint(current, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)

    task1.addApplicableContext(current)
    task1.setProvidedQuality(current, CommonMetrics.SECONDS, 16)

    task2.addApplicableContext(current)
    task2.setProvidedQuality(current, CommonMetrics.SECONDS, 17)

    goal.addDependency(task1)
    goal.addDependency(task2)

    goal.addApplicableContext(current)

    interp = Interpretation()
    interp.addQualityConstraint(qc)

    plan = goal.isAchievable(fullContext, interp)
    assert goal.decomposition is Decomposition.OR
    assert plan is None


def test_ApplicableDeps():
    goal = Pragmatic(Decomposition.AND, "Root")

    task = Task("T1")
    context = Context("C1")
    wrongContext = Context("C2")

    qc = QualityConstraint(context, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)

    task.addApplicableContext(context)
    task.setProvidedQuality(context, CommonMetrics.SECONDS, 13)

    goal.addDependency(task)
    goal.addApplicableContext(context)
    goal.interp.addQualityConstraint(qc)

    interp = Interpretation()
    interp.addQualityConstraint(qc)
    current = []
    current.append(wrongContext)
    assert goal.isAchievable(current, interp) is None

    current.append(context)
    assert len(goal.isAchievable(current, interp).getTasks()) == 1


def test_getApplicableQC():
    goal = Pragmatic(Decomposition.AND, "Root")

    task = Task("T1")
    context = Context("C1")
    anotherContext = Context("C2")

    fullContext = []

    qc = QualityConstraint(context, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)
    stricter = QualityConstraint(
        anotherContext, CommonMetrics.SECONDS, 10, Comparison.LESS_OR_EQUAL_TO)

    task.setProvidedQuality(context, CommonMetrics.SECONDS, 13)

    goal.addDependency(task)
    goal.addApplicableContext(context)
    goal.interp.addQualityConstraint(qc)
    goal.interp.addQualityConstraint(stricter)

    interp = Interpretation()
    interp.addQualityConstraint(qc)

    fullContext.append(context)

    assert stricter not in goal.interp.getQualityConstraints(
        fullContext)

    plan = goal.isAchievable(fullContext, interp)
    assert len(plan.getTasks()) == 1

    fullContext.append(anotherContext)
    assert qc in goal.interp.getQualityConstraints(
        fullContext)

    assert stricter in goal.interp.getQualityConstraints(
        fullContext)

    assert goal.isAchievable(fullContext, interp) is None

    fullContext.remove(context)
    assert qc not in goal.interp.getQualityConstraints(
        fullContext)

    assert stricter in goal.interp.getQualityConstraints(
        fullContext)


def test_shouldGetBaselineQC():
    goal = Pragmatic(Decomposition.AND, "Root")

    context = Context("C1")

    qc = QualityConstraint(context, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)
    baselineQC = QualityConstraint(
        None, CommonMetrics.SECONDS, 10, Comparison.LESS_OR_EQUAL_TO)

    goal.addApplicableContext(context)
    goal.interp.addQualityConstraint(qc)
    goal.interp.addQualityConstraint(baselineQC)

    assert baselineQC in goal.interp.getQualityConstraints([None])


def test_shouldThereBeMoreThanOneApplicableQCreturnTheStricterOne():
    goal = Pragmatic(Decomposition.AND, "Root")

    task = Task("T1")
    context = Context("C1")
    anotherContext = Context("C2")

    fullContext = []

    qc = QualityConstraint(context, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)
    stricter = QualityConstraint(
        anotherContext, CommonMetrics.SECONDS, 10, Comparison.LESS_OR_EQUAL_TO)

    goal.addDependency(task)
    goal.addApplicableContext(context)
    goal.interp.addQualityConstraint(qc)
    goal.interp.addQualityConstraint(stricter)

    assert stricter == qc.stricterQC(stricter)

    fullContext.append(context)
    assert qc in goal.interp.getQualityConstraints(fullContext)

    fullContext.append(anotherContext)
    assert stricter in \
        goal.interp.getQualityConstraints(fullContext)


def test_shouldIncludeNonApplicableContexts():
    goal = Pragmatic(False, "Root")

    task = Task("T1")
    context = Context("C1")
    wrongContext = Context("C2")
    current = []

    qc = QualityConstraint(context, CommonMetrics.SECONDS,
                           15, Comparison.LESS_OR_EQUAL_TO)

    task.addApplicableContext(context)
    task.setProvidedQuality(context, CommonMetrics.SECONDS, 13)

    goal.addDependency(task)
    goal.addNonapplicableContext(wrongContext)
    goal.interp.addQualityConstraint(qc)

    interp = Interpretation()
    interp.addQualityConstraint(qc)

    current.append(wrongContext)
    assert goal.isAchievable(current, interp) is None

    current.append(context)
    assert goal.isAchievable(current, interp) is None

    current.remove(wrongContext)
    assert goal.isAchievable(current, interp)
    assert goal.isAchievable(current, interp).getTasks()
    assert 1 == len(goal.isAchievable(current, interp).getTasks())
