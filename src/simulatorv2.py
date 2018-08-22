def box_score_grabber(boxscore,team,year,spread_df):
    df = copy.deepcopy(boxscore[(boxscore.team==team) & (boxscore.year==year)])
    df.index = range(len(df))
    df_new = copy.deepcopy(df[['fg_pct','fg3_pct','orb','drb','ast','stl','blk','tov','pf'\
              ,'opp_fg_pct','opp_fg3_pct','opp_orb','opp_drb','opp_ast'\
              ,'opp_stl','opp_blk','opp_tov','opp_pf']])
    spread = copy.deepcopy(spread_df[(spread_df.team==team)&(spread_df.year==year)])
    spread.index = range(len(spread))
    ats_record = np.insert((np.cumsum(spread.ats.values[:81]))/range(1,82),0,0.0)
    spread['ats_record'] = ats_record
    y_df = spread.ats.values
    return pd.concat([spread[['spread','ats_record']],df_new],axis=1), y_df

def spread_prediction_creator(home,year,team_avg,spread_df,weight=.5,samples=1):
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
    return pd.concat([df[['spread','ats_record']],pd.DataFrame(lst,columns=['fg_pct','fg3_pct','orb','drb','ast','stl','blk','tov'\
              ,'opp_fg_pct','opp_fg3_pct','opp_orb','opp_drb','opp_ast'\
              ,'opp_stl','opp_blk','opp_tov','opp_pf'])],axis=1), y_df

def team_sampler(team1:str,team2:str,avgs:dict,year:str,weight=.5,samples=1):
    '''
    takes two team inputs and a dictionary with teams as keys and values as averages and standard deviations
    it attempts to generate a sample game using the previous year's data
    the sample weight is with respect to team1
    '''
    year = str(int(year)-1)

    team1_fg_pct = stats.norm(weight * pd.DataFrame(avgs[team1][year]).fg_pct.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).opp_fg_pct.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).fg_pct.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).opp_fg_pct.values[1])).rvs(samples).mean()
    
    team2_fg_pct   = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_fg_pct.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).fg_pct.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_fg_pct.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).fg_pct.values[1])).rvs(samples).mean()
    
    team1_fg3_pct  = stats.norm(weight * pd.DataFrame(avgs[team1][year]).fg3_pct.values[0] + (1-weight) * pd.DataFrame(avgs[team2][year]).opp_fg3_pct.values[0]\
                          , (((weight**2) * pd.DataFrame(avgs[team1][year]).fg3_pct.values[1]) + ((1-weight)**2) \
                          * pd.DataFrame(avgs[team2][year]).opp_fg3_pct.values[1])).rvs(samples).mean()
    
    team2_fg3_pct  = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_fg3_pct.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).fg3_pct.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_fg3_pct.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).fg3_pct.values[1])).rvs(samples).mean()
    
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

    team1_pf     = stats.norm(weight * pd.DataFrame(avgs[team1][year]).pf.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).opp_pf.values[0] \
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).pf.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).opp_pf.values[1])).rvs(samples).mean()
    
    team2_pf     = stats.norm(weight * pd.DataFrame(avgs[team1][year]).opp_pf.values[0] + (1-weight) \
                            * pd.DataFrame(avgs[team2][year]).pf.values[0]\
                            , (((weight**2) * pd.DataFrame(avgs[team1][year]).opp_pf.values[1]) + ((1-weight)**2) \
                            * pd.DataFrame(avgs[team2][year]).pf.values[1])).rvs(samples).mean()
   
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
    return [team1_fg_pct, team1_fg3_pct, team1_orb,team1_drb,team1_ast,team1_stl \
          , team1_blk,team1_tov, team1_pf, \
            team2_fg_pct, team2_fg3_pct, team2_orb,team2_drb,team2_ast,team2_stl\
           ,team2_blk,team2_tov,team2_pf]