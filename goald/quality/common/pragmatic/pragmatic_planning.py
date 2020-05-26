from goald.quality.pragmatic.model.refinement import Refinement
from goald.quality.pragmatic.model.plan import Plan
from goald.quality.pragmatic.model.decomposition import Decomposition
from goald.quality.pragmatic.exceptions.metric_not_found import MetricNotFoundException


class PragmaticPlanning:

    # Recursive function to choose plan
    def isAchievable(self, goal, current, interp):
        # Check if Goal is achievable for current context
        if not goal.isApplicable(current):
            return None
        # Active taks or goals that are dendencies for self.goal achievement
        dependencies = goal.getApplicableDependencies(current)

        if goal.decomposition == Decomposition.OR:
            # if decomposition is OR return first achievable plan from dependencies list
            for dep in dependencies:
                if(dep.myType() is Refinement().GOAL):
                    plan = self.isAchievable(dep, current, interp)
                elif(dep.myType() is Refinement().TASK):
                    plan = self.isAchievableTask(dep, current, interp)
                if plan:
                    return plan
            return None
        else:
            # else decomposition is AND return achievables plans list from dependencies list
            complete = Plan()
            for dep in dependencies:
                if(dep.myType() is Refinement().GOAL):
                    plan = self.isAchievable(dep, current, interp)
                elif(dep.myType() is Refinement().TASK):
                    plan = self.isAchievableTask(dep, current, interp)

                if plan:
                    complete.add(plan)
                else:
                    return None
            if len(complete.getTasks()) > 0:
                return complete
            else:
                return None

    def abidesByInterpretation(self, task, interp, current):
        # Return if the quality from the task is suitable
        feasible = True
        if interp is None:
            return True

        currentQcs = interp.getQualityConstraints(current)
        # get the qualities constraints from curent active context
        for qc in currentQcs:
            try:
                myQC = task.myProvidedQuality(qc.metric, current)
                if myQC is not None:
                    # check if metric fits the interpretation constrain
                    if not qc.abidesByQC(myQC, qc.metric):
                        feasible = False
            except MetricNotFoundException:
                pass
        # get the qualities constraints from baseline
        if interp.getQualityConstraints([None]):
            for qc in interp.getQualityConstraints([None]):
                try:
                    myQC = task.myProvidedQuality(qc.metric, current)
                    if myQC is not None:
                        if not qc.abidesByQC(myQC, qc.metric):
                            feasible = False
                except MetricNotFoundException:
                    pass

        return feasible

    def isAchievableTask(self, task, current, interp):
        # check if the task is applicable for that context
        if not task.isApplicable(current):
            return None
        # test if quality fit and if return it with Plan to be added
        if self.abidesByInterpretation(task, interp, current):
            return Plan(task)
        else:
            return None
            
