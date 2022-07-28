import librosa
import sys
import numpy as np
from sklearn.cluster import KMeans
import os
import os.path
import datetime
import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
  args = sys.argv
  if len(args) == 2:
    y, sr = librosa.load(args[1])
    #common argsort
    y_argsort = y.argsort()[::-1]

    #diff argsort
    yd = np.diff(y)
    yd_argsort = yd.argsort()[::-1]

    #k-mean clustering
    pred_y = KMeans(n_clusters=10).fit_predict(y_argsort[0:1000].reshape(-1,1))
    pred_yd = KMeans(n_clusters=10).fit_predict(yd_argsort[0:1000].reshape(-1,1))
    
    #pred new cluster index
    s = set()
    yl = []
    for i in range(len(pred_y)):
      if pred_y[i] not in s:
        s.add(pred_y[i])
        yl.append(i)
    s = set()
    ydl = []
    for i in range(len(pred_yd)):
      if pred_yd[i] not in s:
        s.add(pred_yd[i])
        ydl.append(i)

    #ffmpeg
    for i in yl:
      cmd = "ffmpeg -ss {} -t 240 -i {} -c copy {}".format(
        int(y_argsort[i]/sr),
        args[1],
        "kaiseki_"+os.path.splitext(os.path.basename(args[1]))[0].split("_")[0]+"_"+str(i)+"_"+str(datetime.timedelta(seconds=int(y_argsort[i]/sr)))+".mp4")
      print(cmd)
      os.system(cmd)
    for i in ydl:
      cmd = "ffmpeg -ss {} -t 240 -i {} -c copy {}".format(
        int(yd_argsort[i]/sr),
        args[1],
        "kaisekid_"+os.path.splitext(os.path.basename(args[1]))[0].split("_")[0]+"_"+str(i)+"_"+str(datetime.timedelta(seconds=int(yd_argsort[i]/sr)))+".mp4")
      print(cmd)
      os.system(cmd)
  else:
    print("you must input an argument of movie file name")
