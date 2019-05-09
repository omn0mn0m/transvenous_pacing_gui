"""
.. module:: client
    :platform: Windows
    :synopsis: ECG signal lookup class with signal manipulation
 
.. moduleauthor:: Nam Tran, Brianna Cathey
"""

# Standard Library imports
import json
import os
import sys

class Signals():
    """ECG signal lookup class with signal manipulation
 
    This class reads in a JSON file as a dictionary and uses that for its base values.
    It then creates the an updated signal to account for heart rate.
    """

    # Position index to key
    signal_index = {
        0: 'RIP',
        1: 'SVC',
        2: 'HRA',
        3: 'MRA',
        4: 'LRA',
        5: 'RV',
        6: 'RVW',
        14: 'IVC',
        16: 'PA',
        26: 'RVW_PACED'
    }

    def __init__(self):
        """Constructor"""

        # Gets the JSON file path
        json_file = os.path.abspath('{}/../signals.json'.format(__file__))

        # Opens the JSON file
        with open(json_file) as f:
            # Creates the dictionary for the JSON file
            self.ecg_signals = json.load(f)

    def get_signal(self, location, rate, version=0):
        """Gets the ECG signal at a specified position with a specified rate
 
        Args:
            location (str): Heart position to display an ECG signal for
            rate (int): Heartrate to edit the signal to
            version (int): Either 0 or 1
        """

        # Get the signal dictionary entry
        signal = self.ecg_signals[location][version]

        # Break it up into an x and a y as a copy to avoid overwriting the base signals
        x = signal['x'].copy()
        y = signal['y'].copy()

        # If the position is not unknown
        if not location == 'RIP':
            # Match start and finish y values
            y[-1] = y[0]

            # Get the total duration of 1 heart beat
            time_beat = x[-1] - x[0]
            # Calculate the desired R-R interval
            r = 1 / (rate/60)

            # If the R-R interval is greater than the single heart beat
            if r > time_beat:
                # Append a new x value that is the start of the next beat
                x.append(x[0] + r)
                # Shift all x values to be at 0
                x = [xx - x[0] for xx in x]
                # Add in a y value to match the first one at the end
                y.append(y[-1])
            # If the R-R interval is less than or equal to a single heart beat
            else:
                # Get the length of 1 heart beat
                length = x[-1] - x[0]
                # Get a proportion to shrink the beats by to fit them
                d = r / length
                # Add in the last value to be just at the end
                x.append(x[0])
                # Compress the values so they fit with the desired heart rate
                x = [xx * d for xx in x]
                # Shift all x values to be at 0
                x = [xx - x[0] for xx in x]

        # Return the massaged values
        return x, y

# Code to run if the script is called by itself - for debugging
if __name__ == "__main__":
    # Class instantiation
    signals = Signals()

    # Test with SVC at 20 BPM
    [x,y] = signals.get_signal('SVC', 20)
    print(len(x))
    print(x[-1])
    print(x[-2])

    # Test with SVC at various BPM
    print(signals.get_signal('SVC', 20))
    print(signals.get_signal('SVC', 80))
    print(signals.get_signal('SVC', 140))
