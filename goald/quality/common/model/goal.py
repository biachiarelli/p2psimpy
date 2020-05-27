from goald.quality.common.model.refinement import Refinement
from goald.quality.common.model.plan import Plan
from goald.quality.common.model.decomposition import Decomposition


class Goal(Refinement):
    def __init__(self, decomposition, identifier):
        Refinement.__init__(self, identifier)
        self.decomposition = decomposition

    def myType(self):
        return Refinement().GOAL