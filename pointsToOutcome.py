from createTable import *
import matplotlib.pyplot as plt

def rankResult(results):
    headings=['PointDiff','PointDiffPerGame','PointDiffRounded','Result']
    numbers=[]
    for row in results.loc[50:].iterrows():
        row = row[1]
        table = createTable(results,row['Date'])
        homeInd = table[table['Team']==row['HomeTeam']].index
        awayInd = table[table['Team']==row['AwayTeam']].index
        highInd = max(homeInd, awayInd)[0]
        lowInd = min(homeInd, awayInd)[0]
        diff = table.iloc[lowInd]['Points'] - table.iloc[highInd]['Points']
        avDiff = 2 * diff/(table.iloc[lowInd]['Played'] + table.iloc[highInd]['Played'])
        if row['FTHG'] == row['FTAG']:
            numbers.append([diff, avDiff, round(avDiff, 2), 'Draw'])
        elif (row['FTHG'] < row['FTAG']) & (homeInd == lowInd):
            numbers.append([diff, avDiff, round(avDiff, 2), 'Win'])
        elif (row['FTHG'] > row['FTAG']) & (homeInd == highInd):
            numbers.append([diff, avDiff, round(avDiff, 2), 'Win'])
        else:
            numbers.append([diff, avDiff, round(avDiff, 2), 'Loss'])
    return DataFrame(columns=headings,data=numbers)

def plotRankResult(results):
    plot = rankResult(results).plot(x='PointDiffRounded',y='Result',kind='barh')
    plt.show()
    return

results = readResults('C:/Users/peter/PL program/18-19 results.csv')
plotRankResult(results)
print(plotRankResult(results))
