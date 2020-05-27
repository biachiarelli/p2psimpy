class Refinement():

    def __init__(self, identifier=""):
        self.GOAL = 1
        self.TASK = 2
        self.DELEGATION = 3

        self.applicableContext = None

        self.nonapplicableContexts = []

        self.dependencies = []

        self.identifier = identifier

    def addNonapplicableContext(self, context):
        self.nonapplicableContexts.append(context)

    def addDependency(self, goal):
        self.dependencies.append(goal)

    def addApplicableContext(self, context):
        if self.applicableContext is None:
            self.applicableContext = []
        if isinstance(context, list):
            self.applicableContext.extend(context)
        else:
            self.applicableContext.append(context)

    def getApplicableContext(self):
        return self.applicableContext

    # Return list of refinements(goals/tasks) with the applicable context in the active contexts
    def getApplicableDependencies(self, current):
        applicableDeps = []

        # itarates over dependencies(goals/tasks) to add them in applicable
        for dep in self.dependencies:
            if dep.applicableContext is None:
                applicableDeps.append(dep)
                continue
            # check if current context is in dep applicable context and if isnt already in applicabledeps
            for context in current:
                if context in dep.applicableContext and dep not in applicableDeps:
                    applicableDeps.append(dep)

        return applicableDeps
