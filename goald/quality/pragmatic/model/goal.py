from goald.quality.pragmatic.model.refinement import Refinement
from goald.quality.pragmatic.model.plan import Plan
from goald.quality.pragmatic.model.decomposition import Decomposition


class Goal(Refinement):
    def __init__(self, decomposition, identifier):
        Refinement.__init__(self, identifier)
        self.decomposition = decomposition

    def myType(self):
        return Refinement().GOAL

    # Recursive function to choose plan
    def isAchievable(self, current, interp):
        # Check if Goal is achievable for current context
        if not self.isApplicable(current):
            return None
        # Active taks or goals that are dendencies for self.goal achievement
        dependencies = self.getApplicableDependencies(current)

        if self.decomposition == Decomposition.OR:
            # if decomposition is OR return first achievable plan from dependencies list
            for dep in dependencies:
                plan = dep.isAchievable(current, interp)
                if plan:
                    return plan
            return None
        else:
            # else decomposition is AND return achievables plans list from dependencies list
            complete = Plan()
            for dep in dependencies:
                plan = dep.isAchievable(current, interp)
                if plan:
                    complete.add(plan)
                else:
                    return None
            if len(complete.getTasks()) > 0:
                return complete
            else:
                return None
