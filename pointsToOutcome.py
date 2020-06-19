from createTable import *
import matplotlib.pyplot as plt

##Input list of match results and returns df recording the point difference
##before the match and the respective outcome. Also calculates the average
##difference per game played, and rounds this to 2dp
def pointsToOutcome(results):
    headings = ['PointDiff','PointDiffPerGame','PointDiffRounded','Outcome']
    df = DataFrame(columns=headings)
    START = 20
    ROUND_TO = 0.05
    date = 0
    for row in results.iloc[START:].iterrows():
        rowInd = row[0]
        row = row[1]
        if row['Date'] != date:
            date = row['Date']
            table = createTable(results,date)
        homeInd = table[table['Team']==row['HomeTeam']].index[0]
        awayInd = table[table['Team']==row['AwayTeam']].index[0]
        highInd = max([homeInd, awayInd])
        lowInd = min([homeInd, awayInd])
        diff = table.at[lowInd,'Points'] - table.at[highInd,'Points']
        avDiff = 2 * diff/(table.at[lowInd,'Played'] + table.at[highInd,'Played'])
        rounded = round(round(avDiff / ROUND_TO) * ROUND_TO, 2)
        if row['FTHG'] == row['FTAG']:
            df.loc[rowInd] = [diff, avDiff, rounded, 'Draw']
        elif (row['FTHG'] < row['FTAG']) & (homeInd == lowInd):
            df.loc[rowInd] = [diff, avDiff, rounded, 'Loss']
        elif (row['FTHG'] > row['FTAG']) & (homeInd == highInd):
            df.loc[rowInd] = [diff, avDiff, rounded, 'Loss']
        else:
            df.loc[rowInd] = [diff, avDiff, rounded, 'Win']
    return df

##Plots stacked bar chart of match outcomes for each point difference
def plotPointsToOutcome(results):
    headings = ['PointDiff','Win','Draw','Loss']
    df = DataFrame(columns=headings)
    for row in pointsToOutcome(results).iterrows():
        rowInd = row[0]
        row = row[1]
        df.loc[rowInd] = [row['PointDiff'], 0, 0, 0]
        df.loc[rowInd][row['Outcome']] = 1
    df = df.groupby(['PointDiff']).sum()
    df.plot.bar(stacked=True)
    plt.title('Match outcomes for higher ranked team')
    plt.xlabel('Point Difference')
    plt.ylabel('Number of Matches')
    plt.show()
    return

##Plots stacked bar chart of match outcomes for each average point
##difference(rounded)
def plotPointsPerMatchToOutcome(results):
    headings = ['PointDiffRounded','Win','Draw','Loss']
    df = DataFrame(columns=headings)
    for row in pointsToOutcome(results).iterrows():
        rowInd = row[0]
        row = row[1]
        df.loc[rowInd] = [row['PointDiffRounded'], 0, 0, 0]
        df.loc[rowInd][row['Outcome']] = 1
    df = df.groupby(['PointDiffRounded']).sum()
    df.plot.bar(stacked=True)
    plt.title('Match outcomes for higher ranked team')
    plt.xlabel('Point Difference per Match')
    plt.ylabel('Number of Matches')
    plt.show()
    return
