import json
import os

class Signals():

    signal_index = {
        0: 'RIP',
        1: 'SVC',
        2: 'HRA',
        3: 'MRA',
        4: 'LRA',
        5: 'RV',
        6: 'RVW',
        15: 'IVC',
        16: 'PA'
    }

    def __init__(self):
        json_file = os.path.abspath('guiserver/signals.json')

        with open(json_file) as f:
            self.ecg_signals = json.load(f)

    def get_signal(self, location, rate, version=0):
        signal = self.ecg_signals[location][version]

        xx = signal['x']
        yy = signal['y']

        d = 60 / (rate * (xx[29]-xx[0]))
        new_first = xx[0] * d

        xx = [(w * d) - new_first for w in xx]

        yy.pop(29)
        yy.append(yy[0])

        return xx, yy
