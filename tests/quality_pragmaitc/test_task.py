from goald.quality.common.model.task import Task
from goald.quality.common.model.context import Context
from goald.quality.common.model.decomposition import Decomposition
from goald.quality.common.model.comparison import Comparison
from goald.quality.common.model.quality_constraint import QualityConstraint
from tests.test_data.mpers_metric import MpersMetrics
from tests.test_data.mpers_model import MpersModel
from goald.quality.planning.pragmatic.pragmatic import Pragmatic
from goald.quality.planning.pragmatic.pragmatic_planning import PragmaticPlanning

import pytest


@pytest.fixture
def mpers():
    mpers = MpersModel()

    return mpers


def test_shouldProvideCorrectValueForMetric():
    task = Task("T1")
    currentContext = Context("C1")
    fullContext = []

    fullContext.append(currentContext)

    task.setProvidedQuality(currentContext, MpersMetrics.METERS, 30)

    assert 30 == PragmaticPlanning().myProvidedQuality(task, MpersMetrics.METERS, fullContext)


def text_shouldProvideMetricForBaseline():
    task = Task("t1")

    current = Context("C1")
    fullContext = []
    fullContext.append(current)

    task.setProvidedQuality(None, MpersMetrics.METERS, 30.0)

    assert 30.0 == PragmaticPlanning().myProvidedQuality(task, MpersMetrics.METERS, fullContext)


def metricNotFound():
    task = Task("T1")
    currentContext = Context("C1")
    fullContext = []

    fullContext.append(currentContext)

    task.setProvidedQuality(currentContext, MpersMetrics.METERS, 30.0)

    result = PragmaticPlanning().myProvidedQuality(task, MpersMetrics.SECONDS, fullContext)
    assert result is None


def test_OnlyBaselineDefined():
    task = Task("T1")
    baseline = Context(None)
    fullContext = []

    fullContext.append(baseline)

    task.setProvidedQuality(baseline, MpersMetrics.METERS, 50.0)

    assert 50.0 == PragmaticPlanning().myProvidedQuality(task, MpersMetrics.METERS, fullContext)


def test_shouldProvideSpecificContextMetric():
    task = Task("T2")
    currentContext = Context("C1")
    baseline = None
    fullContext = []

    fullContext.append(currentContext)
    fullContext.append(baseline)

    task.setProvidedQuality(currentContext, MpersMetrics.METERS, 50)
    task.setProvidedQuality(baseline, MpersMetrics.METERS, 30)

    assert 50 == PragmaticPlanning().myProvidedQuality(task, MpersMetrics.METERS, fullContext)


def test_abidesByInterpretation_passing_baseline(mpers):
    isNotifiedAboutEmergencyGoal = mpers.goals.isNotifiedAboutEmergencyGoal
    notifyByMobileVibrationTask = mpers.tasks.notifyByMobileVibrationTask
    c1 = mpers.contexts.c1
    c9 = mpers.contexts.c9

    context = [c1]
    result = PragmaticPlanning().abidesByInterpretation(notifyByMobileVibrationTask, 
        isNotifiedAboutEmergencyGoal.interp, context)
    assert result == True

    context = [c9]
    result = PragmaticPlanning().abidesByInterpretation(notifyByMobileVibrationTask, 
        isNotifiedAboutEmergencyGoal.interp, context)
    assert result == True


def test_abidesByInterpretation_not_passing_baseline(mpers):
    isNotifiedAboutEmergencyGoal = mpers.goals.isNotifiedAboutEmergencyGoal
    notifyBySoundAlertTask = mpers.tasks.notifyBySoundAlertTask
    c6 = mpers.contexts.c6
    c1 = mpers.contexts.c1

    context = [c6]
    result = PragmaticPlanning().abidesByInterpretation(notifyBySoundAlertTask, 
        isNotifiedAboutEmergencyGoal.interp, context)
    assert result == True

    context = [c1]
    result = PragmaticPlanning().abidesByInterpretation(notifyBySoundAlertTask, 
        isNotifiedAboutEmergencyGoal.interp, context)
    assert result == False


def test_abidesByInterpretation_only_baseline(mpers):
    considerLastKnownLocationTask = mpers.tasks.considerLastKnownLocationTask
    locationIsIdentifiedGoal = mpers.goals.locationIsIdentifiedGoal
    context = []

    result = PragmaticPlanning().abidesByInterpretation(considerLastKnownLocationTask, 
        locationIsIdentifiedGoal.interp, context)
    assert result == True


def test_abidesByInterpretation_only_baseline_context(mpers):
    considerLastKnownLocationTask = mpers.tasks.considerLastKnownLocationTask
    locationIsIdentifiedGoal = mpers.goals.locationIsIdentifiedGoal
    c1 = mpers.contexts.c1
    c2 = mpers.contexts.c2
    c3 = mpers.contexts.c3

    context = [c1, c2, c3]

    result = PragmaticPlanning().abidesByInterpretation(considerLastKnownLocationTask, 
        locationIsIdentifiedGoal.interp, context)
    assert result == True


def test_abidesByInterpretation_context_not_passing(mpers):
    identifyLocationByVoiceCallTask = mpers.tasks.identifyLocationByVoiceCallTask
    locationIsIdentifiedGoal = mpers.goals.locationIsIdentifiedGoal
    c5 = mpers.contexts.c5

    context = []

    result = PragmaticPlanning().abidesByInterpretation(identifyLocationByVoiceCallTask, 
        locationIsIdentifiedGoal.interp, context)
    assert result == True

    context.append(c5)

    result = PragmaticPlanning().abidesByInterpretation(identifyLocationByVoiceCallTask, 
        locationIsIdentifiedGoal.interp, context)
    assert result == False


def test_abidesByInterpretation_only_baseline_not_passing(mpers):
    locationIsIdentifiedGoal = mpers.goals.locationIsIdentifiedGoal
    context = []

    LongSecondsTask = Task("LongSecondsTask")
    LongSecondsTask.setProvidedQuality(
        None, MpersMetrics.SECONDS, 1500)

    result = PragmaticPlanning().abidesByInterpretation(LongSecondsTask, 
        locationIsIdentifiedGoal.interp, context)
    assert result == False


def test_myQualityBaseline(mpers):
    accessLocationFromTriangulationTask = mpers.tasks.accessLocationFromTriangulationTask
    c2 = mpers.contexts.c2
    c11 = mpers.contexts.c11

    context = [c2]
    result = PragmaticPlanning().myProvidedQuality(accessLocationFromTriangulationTask, 
        MpersMetrics.DISTANCE_ERROR, context)
    assert result == 40

    context.append(c11)
    result = PragmaticPlanning().myProvidedQuality(accessLocationFromTriangulationTask, 
        MpersMetrics.DISTANCE_ERROR, context)
    assert result == 400
