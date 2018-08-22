import pandas as pd
import scipy.stats as stats
import copy
import numpy as np

#for teams
teams    =    ['ATL','BOS','BRK','CHI','CHO','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK',\
              'OKC','ORL', 'PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']
'''
#early work, tried to use sample from previous year's averages and then predict outcome using stats.norm.sf

def team_sample_2(spread_df,team1,team2,year,avgs,weight=.5,samples=1):
    
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
'''

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
#added 'boxscores_2014_2018.pkl' file that has cleaned boxscore data for appropriate years
#added 'team_avg.pkl' for team_avg input
#spread_df is from '../CapstoneProject/spread_df.pkl' it contains relevant spread data and will be the df used for spread_df

def box_score_grabber(boxscore,team,year,spread_df):
    df = copy.deepcopy(boxscore[(boxscore.team==team) & (boxscore.year==year)])
    df.index = range(len(df))
    df_new = copy.deepcopy(df[['fg','fga','fg3','fg3a','ft','fta','orb','drb','ast','stl','blk','tov'\
              ,'opp_fg','opp_fga','opp_fg3','opp_fg3a','opp_ft','opp_fta','opp_orb','opp_drb','opp_ast'\
              ,'opp_stl','opp_blk','opp_tov']])
    spread = copy.deepcopy(spread_df[(spread_df.team==team)&(spread_df.year==year)])
    spread.index = range(len(spread))
    ats_record = np.insert((np.cumsum(spread.ats.values[:81]))/range(1,82),0,0.0)
    spread['ats_record'] = ats_record
    y_df = spread.ats.values
    return pd.concat([spread[['spread','home','ats_record']],df_new],axis=1), y_df

def spread_prediction_creator(spread_df,home,year,team_avg,weight=.5,samples=1):
    df = copy.deepcopy(spread_df[(spread_df.team == team) & (spread_df.year == year)])
    ats_record = np.insert((np.cumsum(df.ats.values[:81]))/range(1,82),0,0.0)
    df['ats_record'] = ats_record
    df.index = range(len(df))
    opp = df.opp.values
    spread = df.spread.values
    lst = []
    y_df = df.ats
    for item in opp:
        lst.append(team_sampler(home,item,team_avg,year,weight=.5,samples=1))
    return pd.concat([df[['spread','ats_record']],pd.DataFrame(lst,columns=['fg','fga','fg3','fg3a','ft','fta','orb','drb','ast','stl','blk','tov'\
              ,'opp_fg','opp_fga','opp_fg3','opp_fg3a','opp_ft','opp_fta','opp_orb','opp_drb','opp_ast'\
              ,'opp_stl','opp_blk','opp_tov'])],axis=1), y_df
    #df['spread_pred'] = spread_list
    #df['diff_pred'] = diff_list
    #new_df = create_dataframe_matchups(team,opp,team_avg,year,weight,samples)
    #final_df = pd.concat([df[['spread','home','ats_record','spread_pred']],new_df],axis=1)
    #y_df = df.ats
    #return copy.deepcopy(df[['spread','total','diff_pred','ats_record']]), y_df


#second attempt to create X_test data(based on previous year's average)

def team_sampler(team1:str,team2:str,avgs:dict,year:str,weight=.5,samples=1):
    '''
    takes two team inputs and a dictionary with teams as keys and values as averages and standard deviations
    it attempts to generate a sample game using the previous year's data
    the sample weight is with respect to team1
    '''
    year = str(int(year)-1)

    team1_fg = stats.norm(weight * pd.DataFrame(avgs[team1][year]).fg.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).opp_fg.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).fg.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).opp_fg.values[1])).rvs(samples).mean()
    
    team2_fg   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_fg.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).fg.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_fg.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).fg.values[1])).rvs(samples).mean()
    
    team1_fga  = stats.norm(weight * pd.DataFrame(avgs[team1][year]).fga.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).opp_fga.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).fga.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).opp_fga.values[1])).rvs(samples).mean()
    
    team2_fga  = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_fga.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).fga.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_fga.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).fga.values[1])).rvs(samples).mean()
    
    team1_fg3  = stats.norm(weight * pd.DataFrame(avgs[team1][year]).fg3.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).opp_fg3.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).fg3.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).opp_fg3.values[1])).rvs(samples).mean()
    
    team2_fg3  = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_fg3.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).fg3.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_fg3.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).fg3.values[1])).rvs(samples).mean()
    
    team1_fg3a = stats.norm(weight * pd.DataFrame(avgs[team1][year]).fg3a.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_fg3a.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).fg3a.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_fg3a.values[1])).rvs(samples).mean()
    
    team2_fg3a = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_fg3a.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).fg3a.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_fg3a.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).fg3a.values[1])).rvs(samples).mean()
    
    team1_ft   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).ft.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_ft.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).ft.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_ft.values[1])).rvs(samples).mean()
    
    team2_ft    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_ft.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).ft.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_ft.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).ft.values[1])).rvs(samples).mean()
    
    team1_ft_pct = stats.norm(pd.DataFrame(avgs[team1][year]).ft_pct.values[0],pd.DataFrame(avgs[team1][year])\
                              .ft_pct.values[1]).rvs(samples).mean()
    
    team2_ft_pct = stats.norm(pd.DataFrame(avgs[team2][year]).ft_pct.values[0],pd.DataFrame(avgs[team2][year])\
                            .ft_pct.values[1]).rvs(samples).mean()
    
    team1_fta = team1_ft / team1_ft_pct
    team2_fta = team2_ft / team2_ft_pct
    
    
    team1_orb   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).orb.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_orb.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).orb.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_orb.values[1])).rvs(samples).mean()
    
    team2_orb   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_orb.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).orb.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_orb.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).orb.values[1])).rvs(samples).mean()
    
    team1_drb   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).drb.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_drb.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).drb.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_drb.values[1])).rvs(samples).mean()
    
    team2_drb   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_drb.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).drb.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_drb.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).drb.values[1])).rvs(samples).mean()
    
    #total rebounds should just be the sum of orb and drb which i will intially leave it out
    
    team1_ast    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).ast.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_ast.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).ast.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_ast.values[1])).rvs(samples).mean()
    
    team2_ast    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_ast.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).ast.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_ast.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).ast.values[1])).rvs(samples).mean()
    
    team1_stl    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).stl.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_stl.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).stl.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_stl.values[1])).rvs(samples).mean()
    
    team2_stl    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_stl.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).stl.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_stl.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).stl.values[1])).rvs(samples).mean()
    
    team1_blk    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).blk.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_blk.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).blk.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_blk.values[1])).rvs(samples).mean()
    
    team2_blk    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_blk.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).blk.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_blk.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).blk.values[1])).rvs(samples).mean()
    
    team1_tov    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).tov.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_tov.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).tov.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_tov.values[1])).rvs(samples).mean()
    
    team2_tov    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_tov.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).tov.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_tov.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).tov.values[1])).rvs(samples).mean()
    #team points should be an aggregation of other generated stats
    '''
    team1_pts    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).pts.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_pts.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).pts.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_pts.values[1])).rvs(samples).mean()
    
    team2_pts    = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_pts.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).pts.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_pts.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).pts.values[1])).rvs(samples).mean()
    '''
    return [team1_fg, team1_fga, team1_fg3, team1_fg3a, team1_ft,team1_fta,team1_orb,team1_drb,team1_ast,team1_stl \
          , team1_blk,team1_tov,
            team2_fg, team2_fga, team2_fg3, team2_fg3a, team2_ft,team2_fta,team2_orb,team2_drb,team2_ast,team2_stl\
           ,team2_blk,team2_tov]