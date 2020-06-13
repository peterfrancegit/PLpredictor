from pandas import *
from numpy import *
import datetime as dt

##reads in list of match results downloaded from https://www.football-data.co.uk/englandm.php
def readResults(results):
    return read_csv(results)[['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG']]
      
##copy and paste location of downloaded results table here
results = readResults('C:/Users/peter/PL program/18-19 results.csv')

##makes list of teams involved in matches from results data
def teamList(results):
    teamList = []
    for team in results['HomeTeam'].append(results['AwayTeam']):
        if team not in teamList:
            teamList.append(team)
    return teamList

##creates PL table dataframe from results data up to chosen date
##Input date as string 'dd/mm/yyyy'
def createTable(results, date):
    table = DataFrame(columns=['Team','W','L','D','Scored','Conceded','Points'],
             data = transpose([teamList(results),[0]*len(teamList(results)),
                               [0]*len(teamList(results)),[0]*len(teamList(results)),[0]*len(teamList(results)),[0]*len(teamList(results)),[0]*len(teamList(results))]))
    table = table.set_index('Team').astype(int64)
    date = dt.datetime.strptime(date,'%d/%m/%Y')
    for i in range(0,len(results.index)):
        if dt.datetime.strptime(results.iloc[i]['Date'],'%d/%m/%Y') < date:
            table.at[results['HomeTeam'][i],'Scored'] = table.at[results['HomeTeam'][i],'Scored'] + results['FTHG'][i]
            table.at[results['HomeTeam'][i],'Conceded'] = table.at[results['HomeTeam'][i],'Conceded'] + results['FTAG'][i]
            table.at[results['AwayTeam'][i],'Scored'] = table.at[results['AwayTeam'][i],'Scored'] + results['FTAG'][i]
            table.at[results['AwayTeam'][i],'Conceded'] = table.loc[results['AwayTeam'][i],'Conceded'] + results['FTHG'][i]
            if results['FTHG'][i] > results['FTAG'][i]:
                table.at[results['HomeTeam'][i],'W'] = table.at[results['HomeTeam'][i],'W'] + 1
                table.at[results['AwayTeam'][i],'L'] = table.at[results['AwayTeam'][i],'L'] + 1
            elif results['FTHG'][i] < results['FTAG'][i]:
                table.at[results['HomeTeam'][i],'L'] = table.at[results['HomeTeam'][i],'L'] + 1
                table.at[results['AwayTeam'][i],'W'] = table.at[results['AwayTeam'][i],'W'] + 1
            else:
                table.at[results['HomeTeam'][i],'D'] = table.at[results['HomeTeam'][i],'D'] + 1
                table.at[results['AwayTeam'][i],'D'] = table.at[results['AwayTeam'][i],'D'] + 1
    for team in teamList(results):
        table.at[team,'Points'] = 3*table.at[team,'W'] + table.at[team,'D']
    table = table.sort_values(by='Points', ascending=False)
    return table


print(createTable(results,'12/1/2019'))


