import numpy as np
import pandas as pd 
import pickle
import plotly
import plotly.graph_objects as go
import os

EXPERIMENT_DONE    = True
EPOCHS             = 101
BOIDS              = 200
COHESION           = 2.0
ALIGNMENT          = 1.0
SEPARATION         = 2.0
DESIRED_SEPARATION = 25.0
DETECTION_RADIUS   = 50.0

if not EXPERIMENT_DONE:
    num_experiments = 0 

    exp_results = {
        'goal_pct_awareness':[],
        'avg_pct_reached':   [],
        'success_pct':       [],
        'is_avg_successful': []
    }

    goal_awareness = 0.0
    for epoch in range(EPOCHS):
        exp_results['goal_pct_awareness'].append(goal_awareness)
        reached_results = []
        success_pct = []

        print(f'GOAL AWARENESS: {goal_awareness}')

        for _ in range(5):
            pct_reached = float(input("pct reached the target: "))
            if pct_reached >= 90.0:
                success_pct.append(1.0)

            else:
                success_pct.append(0.0)

            reached_results.append(pct_reached)

            num_experiments += 1

        reached_results = np.array(reached_results)
        avg_reached = reached_results.mean()
        exp_results['avg_pct_reached'].append(avg_reached)

        success_pct = np.array(success_pct)
        pct_success = success_pct.mean() * 100
        exp_results['success_pct'].append(pct_success)

        print(goal_awareness, avg_reached, pct_success)

        if pct_success >= 90.0:
            exp_results['is_avg_successful'].append(True)

        else:
            exp_results['is_avg_successful'].append(False)

        goal_awareness += 1.0

    with open('experiment_results.pickle', 'wb') as handle:
        pickle.dump(exp_results, handle, protocol=pickle.HIGHEST_PROTOCOL)


pd.options.plotting.backend = 'plotly'

with open('experiment_results.pickle', 'rb') as handle:
    df = pd.DataFrame(pickle.load(handle))

fig = df.plot(
    x='goal_pct_awareness', 
    y='avg_pct_reached',
    title='Percentage of Boids Reaching the Target vs Goal Percentage Awareness')

x = np.array([31])
y = df['avg_pct_reached'][x].values
fig.add_trace(go.Scatter(x=x, y=df['avg_pct_reached'][x], mode='markers+text', text=[f'Goal Awareness Pct: 31.0, Average Pct Reached: {y}'],
                            textposition='top right'))

fig.update_layout(xaxis=dict(tickmode='array', tickvals=tuple(range(0, 110, 10))))

fig.show()

if not os.path.exists('plots'):
    os.mkdir('plots')

fig.write_image('plots/results.png')






