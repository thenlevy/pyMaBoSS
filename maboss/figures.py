"""Tools to draw figures from the MaBoSS results."""


import pandas as pd
import matplotlib.pylab as plt
import numpy as np

def make_plot_trajectory(time_table, ax, palette):
    color_list = []
    for idx in time_table.index.values:
        add_color(idx, color_list, palette)

    time_table.plot(ax=ax, color=color_list)


def make_trajectory(time_table, palette):
    color_list = []
    for idx in time_table.index.values:
        add_color(idx, color_list, palette)
    plot_table.plot(color=color_list)
    plt.legend(loc='best')
    plt.show()


def plot_node_prob(time_table, ax, palette):
    """Plot the probability of each node being up over time."""
    color_list = []
    for idx in time_table.index.values:
        add_color(idx, color_list, palette)
    time_table.plot(ax=ax, color=color_list)


def plot_piechart(plot_table, ax, palette):
    plot_line = plot_table.iloc[-1].rename("")  # Takes the last time point
    plot_line = plot_line[plot_line > 0.01]
    plotting_labels = []
    color_list = []
    for value_index, value in enumerate(plot_line):
        state = plot_line.index.values[value_index]
        add_color(state, color_list, palette)
        if value >= 0.1:
            plotting_labels.append(state)
        else:
            plotting_labels.append("")
    ax.pie(plot_line, labels=plotting_labels, radius=1.2, labeldistance=0.4,
           startangle=90, colors=color_list)
    ax.legend(plot_line.index.values, loc=(0.9, 0.8), fontsize=8)


def plot_fix_point(table, ax, palette):
    """Plot a piechart representing the fixed point probability."""
    palette['no_fp'] = '#121212'
    prob_list = []
    color_list = []
    labels = []
    for i in range(len(table)):
        prob = table['Proba'][i]
        state = table['State'][i]
        prob_list.append(prob)
        add_color(state, color_list, palette)
        labels.append('FP '+str(i+1))
    prob_ns = 1 - sum(prob_list)
    if prob_ns > 0.01:
        prob_list.append(prob_ns)
        add_color('no_fp', color_list, palette)
        labels.append('no_fp')
    ax.pie(prob_list, labels=labels, colors=color_list)




    
def add_color(state, color_list, palette):
    """Add the color corresponding to state to color_list and update palette."""
    if state in palette:
        color_list.append(palette[state])
    else:
        n = (len(palette) + 1) % 10  # We cycle over 10 possible color_list
        color = 'C' + str(n)
        palette[state] = color
        color_list.append(color)


