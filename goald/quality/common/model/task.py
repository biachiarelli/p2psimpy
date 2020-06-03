from goald.quality.common.model.refinement import Refinement
from goald.quality.common.model.plan import Plan
from goald.quality.common.exceptions.metric_not_found import MetricNotFoundException


class Task(Refinement):
    def __init__(self, identifier):
        Refinement.__init__(self, identifier)
        self.providedQualityLevels = {}
        self.identifier = identifier

    def myType(self):
        return Refinement().TASK

    # Set task provided quality from baseline or context
    def setProvidedQuality(self, context, metric, value):
        metricMap = {}
        # Check if the metric was already in Provided Qualities
        if metric in self.providedQualityLevels:
            metricMap = self.providedQualityLevels[metric]
            # if yes, replace with new value
            metricMap[context] = value
            self.providedQualityLevels[metric] = metricMap
        else:
            metricMap[context] = value
            # if no, add
            self.providedQualityLevels[metric] = metricMap