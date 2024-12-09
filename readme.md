Hi, I created a new github repository for project 2. In it, I did the following:

I download one of the the BPIC (Business Process Intelligence Challenge) datasets

I have created: utils.py, in this, I created an evaluation function to evaluate fitness, simplicity, and generalization simultaneously.

Finally, I also have created:  automl.ipynb, in this, I used Hypertuna as an AutoML system to train the model. The objective function to optimize is:  -(fitness * 0.5 + simplicity * 0.3 + generalization * 0.2), It is just a simple example of multi-objective optimization (a priori).

Download data here, uncompress it, and move it to data folder:
https://data.4tu.nl/datasets/db35afac-2133-40f3-a565-2dc77a9329a3