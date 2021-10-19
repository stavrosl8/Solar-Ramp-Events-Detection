import pandas as pd
import numpy as np
import tqdm

df = pd.read_csv('All_ASIs.csv', parse_dates=True, index_col= 'Forecast starting date UTC')
df_clear = pd.read_csv('Data.csv', parse_dates=True, index_col= 'datetime')

data = []

ASI_names = {'ASI1':"$\mathbf{{ASI1}}$",'ASI2':"$\mathbf{{ASI2}}$",
             'ASI3':"$\mathbf{{ASI3}}$",'ASI4':"$\mathbf{{ASI4}}$",
             'ASI5':"$\mathbf{{ASI5}}$",'PSPI':"$\mathbf{{PSPI}}$",
             'Persistence':"$\mathbf{{Persistence}}$"}

for ASI in list(ASI_names.keys()):
    
    print(ASI)
    
    df_ASI = df[df['ASI'] == ASI_names[ASI]]
    
    for date in tqdm.tqdm(df_ASI.index.unique()):
        
        if date in df_clear.index:
            x_test = df_ASI.loc[date]
            x_test.index = pd.to_datetime(x_test['Forcast date UTC'])
            initial_value_measurements_clear = df_clear.loc[[date]]
            minute_initial = initial_value_measurements_clear.index.minute[0]
            GHI_clear_initial = float(initial_value_measurements_clear['GHI_clear'])
            GHI_measured_initial = float(initial_value_measurements_clear['GHI_measured'])
            SZA_initial = float(initial_value_measurements_clear['SZA'])
            
            for date_window_ASI in x_test.index:
                if date_window_ASI in df_clear.index:
                
                    GHI_measured_target = float(df_clear['GHI_measured'].loc[[date_window_ASI]])
                    GHI_clear_target = float(df_clear['GHI_clear'].loc[[date_window_ASI]])
                    GHI_ASI_target = float(x_test['GHI'].loc[[date_window_ASI]])
                    step = float(x_test['step'].loc[[date_window_ASI]])
                  
                    SZA_target = float(df_clear['SZA'].loc[[date_window_ASI]])
                    RM_measured = np.abs((GHI_measured_target - GHI_measured_initial))/GHI_clear_initial
                    RM_clear = np.abs((GHI_clear_target - GHI_clear_initial))/GHI_clear_initial
                    RM_ASI = np.abs((GHI_ASI_target - GHI_clear_initial))/GHI_clear_initial
                   
                    RM_measured_relative = np.abs(np.abs(GHI_measured_target - GHI_clear_target) - np.abs(GHI_measured_initial - GHI_clear_initial))/GHI_clear_initial
                    RM_ASI_relative = np.abs(np.abs(GHI_ASI_target - GHI_clear_target) - np.abs(GHI_measured_initial - GHI_clear_initial))/GHI_clear_initial
                    
                    SZA_dif = SZA_initial - SZA_target
                               
                    dif_window = {'Forecating Starting Time UTC': str(date),
                                  'Forecasted Time UTC': str(date_window_ASI),
                                  'GHI_clear_initial':GHI_clear_initial,
                                  'GHI_measured_initial':GHI_measured_initial,
                                  'SZA_initial':SZA_initial,
                                  'GHI_measured_target':GHI_measured_target,
                                  'GHI_clear_target':GHI_clear_target,
                                  'GHI_ASI_target':GHI_ASI_target,
                                  'SZA_target':SZA_target,
                                  'RM_measured': RM_measured,
                                  'RM_clear': RM_clear,
                                  'RM_ASI': RM_ASI,
                                  'RM_measured_relative':RM_measured_relative,
                                  'RM_ASI_relative':RM_ASI_relative,
                                  'step': int(step),
                                  'ASI': ASI_names[ASI]}
                    
                    data.append(dif_window)    
                else:
                    print(date)
        else:
            print(date)
        
df_all = pd.DataFrame(data)
     
df_all.to_csv('Chu_modified_results.csv', index=0)