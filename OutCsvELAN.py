import xlrd
import csv
import os
import datetime
import numpy as np
import scipy as sp
from scipy import stats
import sys
import subprocess
import pandas as pd

#
#args1 = 'M5003.txt'
#args2 = 274
#MMDlogpath = args1
#print('MMDエージェントのログファイル '+args1+'からELAN用のCSVファイルを生成します')
#StartTime = float(args2)


args = sys.argv
MMDlogpath = args[1]
sys.stderr.write('MMDエージェントのログファイル '+args[1]+'からELAN用のCSVファイルを生成します\n')
StartTime = float(args[2])

StartSentence = 'これから本番の収録を開始します。'

OutFileName = MMDlogpath.replace('.txt', '_elan.csv') #MMDのログファイル名の拡張子（.txt）を（_elan.csv）とした名前をセーブファイルの名前とする．

  # MMDlogを読み込む (1行目はシステムのwindows時間となっており，キネクト時間であるAudioTimeと時間が揃っている（同じPCで処理している場合であれば）)
MMDlogData_pd = pd.read_csv(MMDlogpath, header=None, engine='python', encoding="utf8")
#print(MMDlogData_pd.head())
MMDlogData_pd.columns = ['datetime', 'speechtime', 'MMDspeechtext']

querysentence =  'MMDspeechtext == "' + StartSentence + '"'
Startlist=list(MMDlogData_pd.reset_index().query(querysentence).index)

StartIndex = list(MMDlogData_pd.loc[(MMDlogData_pd['MMDspeechtext'].str.contains(StartSentence)),'MMDspeechtext'].index)[0] #最初にStartSentenceが発言されるインデックスを返す
MMDlogData_pd = MMDlogData_pd.drop(range(0,StartIndex,1))
#print(MMDlogData_pd['MMDspeechtext'].head())
SpeechTime = MMDlogData_pd['speechtime'].values.astype(float)
SpeechTime = SpeechTime - SpeechTime[0] + StartTime #入力された時刻を基準とする．
SpeechSTTimeList_np = []
SpeechENTimeList_np = []
SpeechDurationList_np = []
SegmentNameList = []


#空白の行はあらかじめ消しておく
for index, row in MMDlogData_pd.iterrows():
   if len(row.tolist()[2]) == 1:
      print('space column', index, args[1])
      MMDlogData_pd.drop(index)



j = 0
count = 1
while j < len(SpeechTime)-2:


    # while True:
    #  if MMDlogData_pd['MMDspeechtext'].str.contains("\*").tolist()[j+endind]:
    #   break
    #  elif j + endind + 1 > len(SpeechTime)-1:
    #   break
    #  else:
    #   endind = endind + 1

 if MMDlogData_pd['MMDspeechtext'].str.contains("\*").tolist()[j+1]:
    #endind = 2

    ST_but = SpeechTime[j]
  #  np.append(SpeechSTTimeList_np, np.array([ST_but]))
    SpeechSTTimeList_np.append(ST_but)

    EN_but = SpeechTime[j+2]
   # np.append(SpeechENTimeList_np, np.array([EN_but]))
    SpeechENTimeList_np.append(EN_but)

    Du_but = SpeechTime[j+2] - SpeechTime[j]
    SpeechDurationList_np.append(Du_but)

    SegmentNameList.append(' ')
    count = count + 1
    j = j +2

    #アノテーション区間の間に空白がある場合，埋める．elseを通過した場合，空白が生まれるから．
    if len(SpeechENTimeList_np) > 2:
      if SpeechENTimeList_np[-2] < SpeechSTTimeList_np[-1]:
         SpeechENTimeList_np[-2] = SpeechSTTimeList_np[-1]
         SpeechDurationList_np[-2] = SpeechENTimeList_np[-2] - SpeechSTTimeList_np[-2]

 else:
    print('No end of utterance (*)', j+1, count, args[1], SpeechTime[j])
    ST_but = SpeechTime[j]
    #  np.append(SpeechSTTimeList_np, np.array([ST_but]))
    SpeechSTTimeList_np.append(ST_but)

    EN_but = SpeechTime[j + 1]
    # np.append(SpeechENTimeList_np, np.array([EN_but]))
    SpeechENTimeList_np.append(EN_but)

    Du_but = SpeechTime[j + 1] - SpeechTime[j]
    SpeechDurationList_np.append(Du_but)

    SegmentNameList.append(' ')
    count = count + 1
    j = j + 1



CSVList_pd = pd.DataFrame(SegmentNameList,columns={'A'})
CSVList_pd['B'] = pd.DataFrame(SpeechSTTimeList_np)
CSVList_pd['C'] = pd.DataFrame(SpeechENTimeList_np)
CSVList_pd['D'] = pd.DataFrame(SpeechDurationList_np)
CSVList_pd.to_csv(OutFileName, header=None, index=None)

sys.stderr.write(OutFileName+'というELAN用のCSVファイルの作成に成功しました．\n')
