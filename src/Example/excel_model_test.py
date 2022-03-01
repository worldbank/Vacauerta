'''
Created on 27 Jul. 2011
This file illustrated the use the EMA classes for a model in Excel.
It used the excel file provided by
`A. Sharov <http://home.comcast.net/~sharov/PopEcol/lec10/fullmod.html>`_
This excel file implements a simple predator prey model.
.. codeauthor:: jhkwakkel <j.h.kwakkel (at) tudelft (dot) nl>

# SDT: note the above excel sheet is no longer located at the location above. 
# Am using an older version by the same author
'''
from ema_workbench import (RealParameter, TimeSeriesOutcome, ema_logging,
                           perform_experiments)

from ema_workbench.connectors.excel import ExcelModel
from ema_workbench.em_framework.evaluators import MultiprocessingEvaluator
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Print the current working directory
print("Current working directory: {0}".format(os.getcwd()))


if __name__ == "__main__":
    ema_logging.log_to_stderr(level=ema_logging.INFO)

    model = ExcelModel("predatorPrey", wd="./models",
                       model_file='lotka.xlsx')
    model.uncertainties = [RealParameter("rrr", 0.01, 0.2), #reproduction rate of prey
                           # we can refer to a cell in the normal way
                           # we can also use named cells
                           RealParameter("aaa", .01, .05), #consumption rate of prey
                           RealParameter("bbb", 0.2, 0.4), #reproduction rate of predators
                           RealParameter("mmm", 0.01, 0.05), #mortality rate of predators
                           RealParameter("B4", 30, 70), #starting prey pop
                           RealParameter("C4", 10, 20) #starting predator pop
                           ]

    # specification of the outcomes
    model.outcomes = [TimeSeriesOutcome("B5:B201"),
                      # we can refer to a range in the normal way
                      TimeSeriesOutcome("C5:C201")]  # we can also use named range

    # name of the sheet
    model.default_sheet = "Sheet1"

    with MultiprocessingEvaluator(model) as evaluator:
        results = perform_experiments(model, 2, reporting_interval=1,
                                      evaluator=evaluator)

    experiments, outcomes = results
    print(experiments.shape)
    print(list(outcomes.keys()))
    print(outcomes)
    print(experiments)

    policies = experiments['policy']
    print(policies)
    for i, policy in enumerate(np.unique(policies)):
        experiments.loc[policies==policy, 'policy'] = str(i)

    # data = pd.DataFrame(outcomes)
    # data['policy'] = policies

    # sns.pairplot(data, hue='policy', vars=list(outcomes.keys()))
    # plt.show()