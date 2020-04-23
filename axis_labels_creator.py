class AxisLabelsCreator(object):

    def __init__(self, low, high):
        self.axis_labels = None
        self.high = high
        self.low = low
        self.axis_labels_summarising_metric = 1

    def create_display_labels(self):
        print("mini mongoose")
        print(len(self.axis_labels))
        return self.axis_labels
  
 
