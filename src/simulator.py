import pandas as pd
import scipy.stats as stats
import copy
import numpy as np


def team_sample_2(spread_df,team1,team2,year,avgs,weight=.5,samples=1,games=100):
    
    df = copy.deepcopy(spread_df[(spread_df.team == team) & (spread_df.year == year)])


    team1_points =  (2 * (weight * pd.DataFrame(avgs[team1][year]).fg.values[0] \
                        + (1 - weight) * (pd.DataFrame(avgs[team2][year]).opp_fg.values[0])))  \
                        + (.5   * (weight * pd.DataFrame(avgs[team1][year]).fg3.values[0] + (1-weight) \
                        * pd.DataFrame(avgs[team2][year]).opp_fg3.values[0])) + \
                    (1  * (weight * pd.DataFrame(avgs[team1][year]).ft.values[0] + (1-weight) \
                        * pd.DataFrame(avgs[team2][year]).opp_ft.values[0]))
            
    team1_points_std = pd.DataFrame(avgs[team1][year]).pts.values[1]
    
    team2_points     = 2 * (weight * pd.DataFrame(avgs[team2][year]).fg.values[0] + (1-weight) \
                         * pd.DataFrame(avgs[team1][year]).opp_fg.values[0]) + \
                       .5* (weight * pd.DataFrame(avgs[team2][year]).fg3.values[0] + (1-weight) \
                         * pd.DataFrame(avgs[team1][year]).opp_fg3.values[0]) + \
                         (weight * pd.DataFrame(avgs[team2][year]).ft.values[0] + (1-weight) \
                         * pd.DataFrame(avgs[team1][year]).opp_ft.values[0])
    
    team2_points_std =  pd.DataFrame(avgs[team2][year]).pts.values[1]
    
    
    diff = (stats.norm(team1_points,team1_points_std).rvs(samples).mean() - \
           stats.norm(team2_points,team2_points_std).rvs(samples).mean())
    diff_std = (team1_points_std ** 2 + team2_points_std ** 2) **.5
    #print(diff)
    #pred = stats.norm.sf(spread,diff,diff_std)
    #print(team1_points_std,team2_points_std,diff_std)
    if (diff > 0) and (spread > 0):
        return stats.norm.cdf((spread+diff),diff,diff_std)
    elif (diff > 0) and (spread < 0):
        return stats.norm.sf(-(spread + diff),diff,diff_std)
    elif (diff < 0) and (spread > 0):
        return stats.norm.sf((spread + diff),diff,diff_std)
    elif (diff < 0) and (spread < 0):
        return stats.norm.sf(-(spread + diff),diff,diff_std)

def final_df_creator(team:str,year:str,spread_df,team_avg:dict,weight=.5,samples=1):
    '''
    takes 3 letter team abbreviation, the year as a string, the cleaned spread_df, dictionary and returns
    2 dataframes; final_df: all the transformed features and y_df: the labels ; final_df, y_df
    
    weight: is the weighted distribution of the home team, currently it weights each season but feature implementations
    will attempt to adjust individual games, default = .5 (even weight for both team)

    sample: number of random samples from generated distributions to average, default = 1
    '''

    df = copy.deepcopy(spread_df[(spread_df.team == team) & (spread_df.year == year)])
    ats_record = np.insert((np.cumsum(df.ats.values[1:]))/range(1,82),0,0.0)
    df['ats_record'] = ats_record
    df.index = range(1,len(df)+1)
    opp = df.opp.values
    new_df = create_dataframe_matchups(team,opp,team_avg,year,weight,samples)
    final_df = pd.concat([df[['spread','home','ats_record']],new_df],axis=1)
    y_df = df.ats
    return final_df, y_df



#------------------------------------------------------------------------
#added boxscores_2014_2018.pkl file that has cleaned boxscore data for appropriate years

def spread_prediction_creator(spread_df,home,year,team_avg,weight=.5,samples=1):
    df = copy.deepcopy(spread_df[(spread_df.team == team) & (spread_df.year == year)])
    ats_record = np.insert((np.cumsum(df.ats.values[:81]))/range(1,82),0,0.0)
    df['ats_record'] = ats_record
    df.index = range(1,len(df)+1)
    opp = df.opp.values
    spread = df.spread.values
    spread_list =[]
    diff_list = []
    for s,o in zip(spread,opp):
        s_pred, d_pd = team_sample_2(s,home,o,year,team_avg,weight,samples)
        spread_list.append(round(s_pred,4))
        diff_list.append(round(d_pd,4))
    df['spread_pred'] = spread_list
    df['diff_pred'] = diff_list
    #new_df = create_dataframe_matchups(team,opp,team_avg,year,weight,samples)
    #final_df = pd.concat([df[['spread','home','ats_record','spread_pred']],new_df],axis=1)
    y_df = df.ats
    return copy.deepcopy(df[['spread','total','diff_pred','ats_record']]), y_df
