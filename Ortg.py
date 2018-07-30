'''
100 x Pts / (0.5 * ((Tm FGA + 0.4 * Tm FTA - 1.07 * (Tm ORB / (Tm ORB + Opp DRB)) * (Tm FGA - Tm FG) + Tm TOV) + 
(Opp FGA + 0.4 * Opp FTA - 1.07 * (Opp ORB / (Opp ORB + Tm DRB)) * (Opp FGA - Opp FG) + Opp TOV)))
'''
#calculate team Ortg with respect to opponent
def ortg(team,opp):
    return 100 * team['Pts'] / (0.5 * ((team['FGA'] + 0.4 * team['FTA'] - 1.07 * (team['ORB'] / (team['ORB'] + opp['DRB'])) \
    * (team['FGA'] - team['FG']) + team['TOV']) + (opp['FGA'] + 0.4 * opp['FTA'] - 1.07 * (opp['ORB'] / (opp['ORB'] + team['DRB']))\
    * (opp['FGA'] - opp['FG']) + opp['TOV'])))
 

