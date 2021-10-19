import pandas as pd
import numpy as np
import tqdm

def flowchart(RR_value, Thres_data):
    if np.abs(RR_value) > Thres_data:
        flagg = "Ramp" ; flagg_type = 1
    else: 
        flagg = "No Ramp" ; flagg_type = 0
    return(flagg, flagg_type)

def confusion_matrix_timewindow(dif, sum_):
  
    if dif == 1:
        matrix_type = 'A2'
    elif dif == -1:
         matrix_type = 'B1'
    elif dif == 0:
        if sum_ == 0:
            matrix_type = 'B2'
        else:
            matrix_type = 'A1'
                
    return(matrix_type)

df_RM = pd.read_csv('Chu_modified_results.csv', parse_dates=True, index_col= 'Forecasting Starting Time UTC')
df_RM = df_RM[df_RM['step'] > 0]
df_thr = pd.read_csv('Thr_Chu.csv')

ASI_names = ["$\mathbf{{ASI1}}$","$\mathbf{{ASI2}}$","$\mathbf{{ASI3}}$","$\mathbf{{ASI4}}$","$\mathbf{{ASI5}}$","$\mathbf{{PSPI}}$", "$\mathbf{{Persistence}}$"]
    
step_range = np.arange(1,21,1)

df_all = pd.DataFrame()

for ASI in ASI_names:
    print(ASI)
    x_ASI = df_RM[df_RM['ASI'] == ASI]
        
    for step in step_range:  
        
        Thr_step = df_thr['q95'][df_thr['step'] == step].values[0] 
        Thr_step = Thr_step + 0.1 * Thr_step
        x_step =  x_ASI[x_ASI['step'] == step]
        x_step = x_step.reset_index()
        x_flagged = []
        
        for forc in tqdm.tqdm(range(0, len(x_step))): 
          
            x_ASI_RR = x_step['RM_ASI_relative'][forc]
            x_OBS_RR =  x_step['RM_measured_relative'][forc]
            x_others = x_step.loc[[forc]]
            Flag_ASI, Flag_ASI_type = flowchart(x_ASI_RR, Thr_step)
            Flag_OBS, Flag_OBS_type = flowchart(x_OBS_RR, Thr_step)
            dif = Flag_ASI_type - Flag_OBS_type
            sum_ = Flag_ASI_type + Flag_OBS_type
            Matrix_Flagging = confusion_matrix_timewindow(dif, sum_)

            starting = x_step['Forecasting Starting Time UTC'][forc]
            forecasting = x_step['Forecasted Time UTC'][forc]
            
            dictionary = {'Forecast starting date UTC':starting, 'Forcast date UTC':forecasting,
                          'GHI_clear_initial': float(x_others['GHI_clear_initial']),
                     'GHI_measured_initial': float(x_others['GHI_measured_initial']),
                     'GHI_measured_target':float(x_others['GHI_measured_target']),
                     'GHI_clear_target':float(x_others['GHI_clear_target']),
                     'GHI_ASI_target':float(x_others['GHI_ASI_target']),
                     'RM_measured':float(x_others['RM_measured']), 'RM_clear': float(x_others['RM_clear']),
                     'RM_ASI': float(x_others['RM_ASI']), 'RM_measured_relative': float(x_others['RM_measured_relative']),
                     'RM_ASI_relative': float(x_others['RM_ASI_relative']),
                     'SZA_initial': float(x_others['SZA_initial']),
                     'SZA_target': float(x_others['SZA_target']),
                     "Flag_ASI":Flag_ASI, "Flag_ASI_type":Flag_ASI_type,
                     "Flag_OBS":Flag_OBS, "Flag_OBS_type":Flag_OBS_type,
                     "Flag_ASI_type":Flag_ASI_type, 'Flag_OBS':Flag_OBS,
                     'Flag_OBS_type':Flag_OBS_type, 'Matrix_Flagging':Matrix_Flagging,
                     'step':step, 'ASI':ASI}
          
            x_flagged.append(dictionary)             
     
        df = pd.DataFrame(x_flagged)
    
        df_all = df_all.append(df) 

df_all.to_csv('Chu_flagged_q95.csv',index=0)  

