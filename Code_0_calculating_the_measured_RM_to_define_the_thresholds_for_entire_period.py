import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np

clear_sky_days = ['2019-09-02', '2019-09-03', '2019-09-24', '2019-09-25',
                  '2019-09-26', '2019-09-27', '2019-09-28', '2019-09-29',
                  '2019-10-04', '2019-10-09', '2019-10-13', '2019-10-15',
                  '2019-10-16', '2019-10-24', '2019-10-25', '2019-10-26',
                  '2019-10-29', '2019-11-04', '2019-11-05', '2019-11-18',
                  '2019-11-27', '2019-11-29', '2019-11-30']

len(clear_sky_days)
overcast_days = ['2019-10-22']

df = pd.read_csv('Chu_Data.csv', parse_dates=True , index_col='Forecating Starting Time UTC')

df['day'] = df.index.day
df['month'] = df.index.month
df_clear = pd.DataFrame()

for days in clear_sky_days:
    day = int(days.split('-')[2])
    month = int(days.split('-')[1])
    df_day = df[(df['day'] == day) & (df['month'] == month)]
    df_clear = df_clear.append(df_day)

df_clear['RM_diff'].hist(bins=1000)

x1 = np.sort(df_clear['RM_diff']) 
N = len(df_clear['RM_diff'])
y = np.arange(N)/float(N)
 
q_95 = df_clear['RM_diff'].quantile(0.95)
q_75 = df_clear['RM_diff'].quantile(0.75)
q_99 = df_clear['RM_diff'].quantile(0.99)

plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

f, ax = plt.subplots(figsize = (12, 8))
plt.plot(x1, y, marker='o', color="k", markersize=8)
plt.axhline(y=0.95 , color='red', ls = "--")
plt.axvline(q_95 ,color='red',  ls = "--")
plt.text(q_95, 0.99, "ThrB =(" + str(round(q_95,4)) + ", " + str(0.95) + ")", color = 'tab:green', fontsize=14)
plt.axhline(y=0.75 , color='red', ls = "--")
plt.axvline(q_75 ,color='red',  ls = "--")
plt.text(q_75, 0.77, "ThrA =(" + str(round(q_75,4)) + ", " + str(0.75) + ")", color = 'tab:green', fontsize=14)
plt.ylabel("F(x)", fontsize= 24, fontweight= 'bold')
plt.xlabel('RM_diff', fontsize= 24,style='italic', fontweight= 'bold')
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.title('cleark-sky days', fontsize=25, style='italic', fontweight='bold', y=1.01)    
plt.savefig("CDF_clr_days.png", format = "png", dpi = 150, bbox_inches = "tight")   
plt.close()

plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"

for minute in df_clear['minute'].unique():

    f, ax = plt.subplots(figsize = (12, 8))
    plt.hist(df_clear['RM_diff'], bins=300)
    plt.ylabel("Counts", fontsize= 24, fontweight= 'bold')
    plt.xlabel('RM_diff', fontsize= 24,style='italic', fontweight= 'bold')
    plt.tick_params(axis='y', labelsize=20)
    plt.tick_params(axis='x', labelsize=20)
    plt.title('Clear-sky days', fontsize=25, style='italic', fontweight='bold', y=1.01)    
    plt.savefig("Hist_clr_days.png", format = "png", dpi = 150, bbox_inches = "tight")   
    plt.close()

plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
thr = []
for minute in df_clear['minute'].unique():
    
    df_minute = df_clear['RM_diff'][df_clear['minute'] == minute]
    q_95 = df_minute.quantile(0.95)
    q_75 = df_minute.quantile(0.75)
    q_99 = df_minute.quantile(0.99)
    
    thr.append({'q75':q_75, 'q95':q_95,'q99':q_99})
thr = pd.DataFrame(thr, index = df_clear['minute'].unique())
thr.plot()

thr.to_csv('Thr_Chu.csv')


f, ax = plt.subplots(figsize = (12, 8))
plt.errorbar(thr.index, thr['q75'], thr['q75']*0.1, lw=2, label = 'q75')
plt.errorbar(thr.index, thr['q95'], thr['q95']*0.1, lw=2, label = 'q95')
plt.errorbar(thr.index, thr['q99'], thr['q99']*0.1, lw=2, label = 'q99')
plt.tick_params(axis='y', labelsize=20)
plt.tick_params(axis='x', labelsize=20)
plt.xticks(thr.index)
plt.legend(loc='upper left')
plt.savefig("Thr.png", format = "png", dpi = 150, bbox_inches = "tight")   
plt.close()