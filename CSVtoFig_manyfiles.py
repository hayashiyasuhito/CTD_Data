#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import glob
from scipy.signal import find_peaks
from lmfit.models import GaussianModel
import datetime
import re
plt.style.use('ggplot')

File_num = int(input("連続ファイルは0,別は1を入力:"))
if File_num == 1:
    files = glob.glob('./*.Csv')
    files1 = pd.read_csv(files[0],encoding='cp932',header = 43)
    files2 = pd.read_csv(files[1],encoding = 'cp932',header = 43)
    dfall = pd.concat([files1,files2],ignore_index=True)
    
else:
    dfall = pd.read_csv(glob.glob('./*.Csv')[0],encoding='cp932',header = 43)    

data_which = input("湾内が先なら0, 湾外が先なら1を入力:")
if data_which == 0:
    a = 'Bay'
    b = 'Open Ocean'
else:
    a = 'Open Ocean'
    b = 'Bay'

Filename = glob.glob('./*.Csv')[0]
Exp_Date = re.findall(r'\d+', Filename)[0]


dfall['DateTime']=dfall['日付情報'].astype(str)+dfall['時刻情報'].astype(str)  # Combine Date and TIme as strings
dfall["DateTime"]=pd.to_datetime(dfall["DateTime"], format = '%Y/%m/%d%H:%M:%S')
dfall['index_d'] = dfall.index

peaks, _= find_peaks(dfall['深度 [m]'],prominence=5, distance = 30) #ピーク検出
data_li = []
for i in range(len(peaks)):
    if i == 0:
        data_li.append(dfall.iloc[:round(np.median(peaks))].reset_index())
    else:
        data_li.append(dfall.iloc[round(np.median(peaks)):].reset_index())
    
peak_data_li = []
for i in range(len(peaks)):
    x = data_li[i]['index_d']
    y = data_li[i]['深度 [m]']
    model = GaussianModel()
    params = model.guess(y,x)
    result = model.fit(y, params, x=x)
    max_depth = round(result.params.valuesdict()['center'])
    min_depth = round(result.params.valuesdict()['center']+result.params.valuesdict()['sigma']*2) #95%
    peak_data_li.append(dfall[max_depth:min_depth])

figs,axes = plt.subplots(nrows=3, ncols=2,figsize=(20,20))
plt.rcParams.update({'font.size': 18})
plt.subplots_adjust(wspace=0.4, hspace=0.4)
figs.suptitle("{}_CTD data".format(Exp_Date), size = 25)
#figs.tight_layout(rect=[0,0,1,0.93])

figs,axes = plt.subplots(nrows=3, ncols=2,figsize=(20,20))
plt.rcParams.update({'font.size': 18})
plt.subplots_adjust(wspace=0.4, hspace=0.4)
figs.suptitle("{}_CTD data".format(Exp_Date), size = 25)
#figs.tight_layout(rect=[0,0,1,0.93])
#plt.text(0.5,0.5,"Blue Dots: In the bay\nOrange Dots: Outside the bay", size=25, alpha=0.7, ha="center", va="center")
axes[0,0].scatter(peak_data_li[0]["水温 [℃]"], peak_data_li[0]["深度 [m]"])
axes[0,0].scatter(peak_data_li[1]["水温 [℃]"], peak_data_li[1]["深度 [m]"])
axes[0,0].invert_yaxis()
axes[0,0].xaxis.tick_top()
axes[0,0].xaxis.set_label_position('top')
axes[0,0].set_xlabel('Temperature [℃]',labelpad=10)
axes[0,0].set_ylabel('Depth [m]')
axes[0,0].patch.set_alpha(1)  
axes[0,0].legend(["{}".format(a), "{}".format(b)])

axes[0,1].scatter(peak_data_li[0]["塩分 [ ]"], peak_data_li[0]["深度 [m]"])
axes[0,1].scatter(peak_data_li[1]["塩分 [ ]"], peak_data_li[1]["深度 [m]"])
axes[0,1].invert_yaxis()
axes[0,1].xaxis.tick_top()
axes[0,1].xaxis.set_label_position('top')
axes[0,1].set_xlim(30,)
axes[0,1].set_xlabel('Salinity [‰]',labelpad=10)
axes[0,1].set_ylabel('Depth [m]')
axes[0,1].patch.set_alpha(1)  
axes[0,1].legend(["{}".format(a), "{}".format(b)])

axes[1,0].scatter(peak_data_li[0]["濁度中ﾚﾝｼﾞ [FTU]"], peak_data_li[0]["深度 [m]"])
axes[1,0].scatter(peak_data_li[1]["濁度中ﾚﾝｼﾞ [FTU]"], peak_data_li[1]["深度 [m]"])
axes[1,0].invert_yaxis()
axes[1,0].xaxis.tick_top()
axes[1,0].xaxis.set_label_position('top')
axes[1,0].set_xlabel(' Turbidity [FTU]',labelpad=10)
axes[1,0].set_xlim(0,4)
axes[1,0].set_ylabel('Depth [m]')
axes[1,0].patch.set_alpha(1)  
axes[1,0].legend(["{}".format(a), "{}".format(b)])


axes[1,1].scatter(peak_data_li[0]["Weiss-DO [mg/l]"], peak_data_li[0]["深度 [m]"])
axes[1,1].scatter(peak_data_li[1]["Weiss-DO [mg/l]"], peak_data_li[1]["深度 [m]"])
axes[1,1].invert_yaxis()
axes[1,1].xaxis.tick_top()
axes[1,1].xaxis.set_label_position('top')
axes[1,1].set_xlabel('DO [mg/l]',labelpad=10)
axes[1,1].set_xlim(0,8)
axes[1,1].set_ylabel('Depth [m]')
axes[1,1].patch.set_alpha(1)  
axes[1,1].legend(["{}".format(a), "{}".format(b)])


axes[2,0].scatter(peak_data_li[0]["Chl-a [μg/l]"], peak_data_li[0]["深度 [m]"])
axes[2,0].scatter(peak_data_li[1]["Chl-a [μg/l]"], peak_data_li[1]["深度 [m]"])
axes[2,0].invert_yaxis()
axes[2,0].xaxis.tick_top()
axes[2,0].xaxis.set_label_position('top')
axes[2,0].set_xlabel('Chl-a [μg/l]',labelpad=10)
axes[2,0].set_xlim(0.5,6)
axes[2,0].set_ylabel('Depth [m]')
axes[2,0].patch.set_alpha(1)  
axes[2,0].legend(["{}".format(a), "{}".format(b)])

axes[2,1].axis('off')

#figs.legend('','')
fname = "./{}_CTD.png".format(Exp_Date)
plt.savefig(fname)