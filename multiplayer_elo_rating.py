import pandas as pd
from matplotlib import pyplot as plt
import math


def init():
    global data, ratings, names, data_length, ratings_length

    ratings = pd.read_csv("ratings.csv", index_col='Index')

    for i in range(ratings.shape[0]):
        if pd.isna(ratings.loc[i, 'jai']):
            ratings_length = i
            break

    names = ratings.columns.tolist()

    data = pd.read_csv("scores.csv", index_col='Index')

    for i in range(data.shape[0]):
        if pd.isna(data.loc[i, 'quiz creator']):
            data_length = i
            break

    data.drop(columns=['quiz creator'],inplace=True)


def count(row):
    POINT_CONST = 1024
    current_players = []
    current_outcome = []
    current_ratings = []

    for i in names:
        if not pd.isna(data.at[row,i]):
            current_players.append(i)
            current_outcome.append(data.at[row,i])
            current_ratings.append(ratings.at[row, i])

    rating_sum = sum(current_ratings)
    outcome_sum = sum(current_outcome)
    expectation = []
    performance = []

    for i in range(len(current_players)):
        expectation.append(current_ratings[i]/rating_sum)
        performance.append(current_outcome[i] / outcome_sum)

    ratings.loc[row + 1] = ratings.loc[row]

    for i in range(len(current_players)):
        ratings.at[row+1,current_players[i]] += POINT_CONST*(performance[i]-expectation[i])


def graph():
    y_values = []
    x_values = [j for j in range(data_length+1)]
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i in names:
        temp = [int(j) for j in ratings[i].to_list() if not math.isnan(j)]
        y_values.append(temp)
        plt.plot(x_values, y_values[-1])
        for xy in zip(x_values, y_values[names.index(i)]):
            ax.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')

    plt.legend(names)
    plt.show()


def main():
    init()
    if ratings_length - 1 == data_length:
        print(ratings)
        graph()
        return 0

    for i in range(ratings_length-1, data_length):
        count(i)

    print(ratings)
    ratings.to_csv("ratings.csv")
    graph()


main()