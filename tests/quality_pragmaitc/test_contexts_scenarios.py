from goald.quality.common.model.context import Context
from goald.quality.planning.pragmatic.pragmatic import Pragmatic
from goald.quality.common.model.goal import Goal
from goald.quality.common.model.decomposition import Decomposition
from goald.quality.common.model.task import Task
from goald.quality.common.model.metric import Metric
from goald.quality.common.model.quality_constraint import QualityConstraint
from goald.quality.common.model.comparison import Comparison
from goald.quality.common.model.interpretation import Interpretation
from goald.utils.context_generator import ContextGenerator
from goald.utils.print import print_context
from tests.utils.assert_util import assertPlan
from tests.test_data.mpers_metric import MpersMetrics
from tests.test_data.mpers_model import MpersModel
import pytest


@pytest.fixture
def mpers():
    mpers = MpersModel()

    return mpers


def test_C1(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    plan = mpers.rootGoal.isAchievable(fullContext, None)

    assert plan is not None

    assert False is assertPlan(
        plan, [mpers.tasks.accessLocationFromGPSTask, mpers.tasks.centralCallTask])


def test_C2(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    tasks = mpers.rootGoal.isAchievable(fullContext, None)

    assert tasks is not None

    for task in mpers.rootGoal.isAchievable(fullContext, None).getTasks():
        found = 0

        if task.identifier == "acceptEmergency":
            found = 1
        if task.identifier == "notifyBySoundAlert":
            found = 1

        assert found == 0


def test_C3(mpers):
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c4,
                   mpers.contexts.c5, mpers.contexts.c6, mpers.contexts.c7, mpers.contexts.c8]

    tasks = mpers.rootGoal.isAchievable(fullContext, None)

    assert tasks is not None

    for task in mpers.rootGoal.isAchievable(fullContext, None).getTasks():
        found = 0

        if task.identifier == "acceptEmergency":
            found = 1

        assert found == 0


def test_C4(mpers):
    print("=========== Test C4 ================")
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    tasks = mpers.rootGoal.isAchievable(fullContext, None)

    assert tasks is not None

    for task in mpers.rootGoal.isAchievable(fullContext, None).getTasks():
        found = 0

        if task.identifier == "notifyCentralBySMS":
            found = 1
        if task.identifier == "confirmEmergencyByCall":
            found = 1
        if task.identifier == "notifyBySoundAlert":
            found = 1
        if task.identifier == "sendInfoBySMS":
            found = 1
        if task.identifier == "identifyLocationByVoiceCall":
            found = 1
        if task.identifier == "accessLocationFromTriangulation":
            found = 1

        assert found == 0


def test_C5(mpers):
    print("=========== Test C5 ================")
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    tasks = mpers.rootGoal.isAchievable(fullContext, None)

    assert tasks is not None

    for task in mpers.rootGoal.isAchievable(fullContext, None).getTasks():
        found = 0

        if task.identifier == "notifyCentralBySMS":
            found = 1
        if task.identifier == "notifyBySoundAlert":
            found = 1
        if task.identifier == "sendInfoBySMS":
            found = 1
        if task.identifier == "confirmEmergencyByCall":
            found = 1

        assert found == 0


def test_C6(mpers):
    print("=========== Test C6 ================")
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    tasks = mpers.rootGoal.isAchievable(fullContext, None)

    assert tasks is not None

    for task in mpers.rootGoal.isAchievable(fullContext, None).getTasks():
        found = 0

        if task.identifier == "notifyCentralBySMS":
            found = 1
        if task.identifier == "sendInfoBySMS":
            found = 1
        if task.identifier == "confirmEmergencyByCall":
            found = 1

        assert found == 0


def test_C7(mpers):
    print("=========== Test C7 ================")
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c6,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    tasks = mpers.rootGoal.isAchievable(fullContext, None)

    assert tasks is not None

    for task in mpers.rootGoal.isAchievable(fullContext, None).getTasks():
        found = 0

        if task.identifier == "notifyCentralBySMS":
            found = 1
        if task.identifier == "confirmEmergencyByCall":
            found = 1
        if task.identifier == "notifyBySoundAlert":
            found = 1
        if task.identifier == "sendInfoBySMS":
            found = 1
        if task.identifier == "identifyLocationByVoiceCall":
            found = 1
        if task.identifier == "accessLocationFromTriangulation":
            found = 1
        if task.identifier == "accessLocationFromGPS":
            found = 1

        assert found == 0


def test_C8(mpers):
    print("=========== Test C8 ================")
    fullContext = [mpers.contexts.c1, mpers.contexts.c4, mpers.contexts.c5,
                   mpers.contexts.c7, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    tasks = mpers.rootGoal.isAchievable(fullContext, None)

    assert tasks is not None

    for task in mpers.rootGoal.isAchievable(fullContext, None).getTasks():
        found = 0

        if task.identifier == "notifyCentralBySMS":
            found = 1
        if task.identifier == "confirmEmergencyByCall":
            found = 1
        if task.identifier == "notifyBySoundAlert":
            found = 1
        if task.identifier == "sendInfoBySMS":
            found = 1
        if task.identifier == "identifyLocationByVoiceCall":
            found = 1
        if task.identifier == "accessLocationFromTriangulation":
            found = 1

        assert found == 0


def test_C9(mpers):
    print("=========== Test C9 ================")
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c4,
                   mpers.contexts.c5, mpers.contexts.c6, mpers.contexts.c9]
    tasks = mpers.rootGoal.isAchievable(fullContext, None)

    assert tasks is not None

    for task in mpers.rootGoal.isAchievable(fullContext, None).getTasks():
        found = 0

        if task.identifier == "notifyByLightAlert":
            found = 1
        if task.identifier == "acceptsEmergency":
            found = 1

        assert found == 0


def test_C10(mpers):
    print("=========== Test C10 ================")
    fullContext = [mpers.contexts.c1, mpers.contexts.c2, mpers.contexts.c3, mpers.contexts.c5,
                   mpers.contexts.c6, mpers.contexts.c8, mpers.contexts.c10, mpers.contexts.c12]
    tasks = mpers.rootGoal.isAchievable(fullContext, None)

    assert tasks is not None

    for task in mpers.rootGoal.isAchievable(fullContext, None).getTasks():
        found = 0

        if task.identifier == "notifyByLightAlert":
            found = 1
        if task.identifier == "acceptEmergency":
            found = 1

        assert found == 0


def test_None(mpers):
    print("=========== Test None ================")
    fullContext = []
    tasks = mpers.rootGoal.isAchievable(fullContext, None)

    assert tasks is None
