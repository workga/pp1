'''
plots = [["D_fake", "D_real", "G_GAN"],
         ["D_T_fake0", "D_T_fake1", "D_T_real0", "D_T_real1"],
         ["G_T_GAN0", "G_T_GAN1"],
         ["G_GAN_Feat", "G_T_GAN_Feat0", "G_T_GAN_Feat1"],
         ["F_Flow", "F_Warp", "G_VGG", "G_Warp", "W"]]
'''

plots = [["D_fake", "D_real", "G_GAN"],
         ["D_T_fake0", "D_T_fake1", "D_T_real0", "D_T_real1"],
         ["G_T_GAN0", "G_T_GAN1"],
         ["G_GAN_Feat", "G_T_GAN_Feat0", "G_T_GAN_Feat1"],
         ["F_Flow", "F_Warp", "G_VGG", "G_Warp", "W"]]
         
axs   =  [2,
          0.2,
          0.5,
          10,
          5]

validate = False
fix_axes = False
n_epoches = 5
freq = 1

values = []
for p in plots: 
  values.extend(p)
losses = dict(zip(values, [0 for _ in range(0, len(values))]))

import re
import os
import matplotlib.pyplot as plt

dir  = str(input())
name = str(input())
if (name == ''):
  name = dir

root = "D:\\home\\study\\practice\\datasets\\results\\"

if validate:
  path    = root + dir + "\\loss_log_val.txt"
  n_iters   = 496
else:
  path    = root + dir + "\\loss_log.txt"
  n_iters   = 3004

xe_s = [e for e in range(1, n_epoches + 1)]
ye_s = [losses.copy() for l in range(0, n_epoches)]
  
with open(path, 'r') as file:
  print('file has been opened')
  lines = file.readlines()
  for line in lines:
    if (not re.search(r"(?<=G_GAN: )\d+", line)):
      continue

    cur_epoch = int(re.search(r"(?<=epoch: )\d+", line).group(0))
    cur_iter  = int(re.search(r"(?<=iters: )\d+", line).group(0))

    if (cur_epoch > n_epoches):
      break
        
    for k in losses:
      pattern = "(?<={0})\\d+\.\\d+".format((k + ": "))
      res = re.search(pattern, line)
      if res:
        ye_s[cur_epoch - 1][k] += float(res.group(0))
      
for e in ye_s:
  for k in losses:
    e[k] /= n_iters


for i in range(0, len(plots)):
  plt.figure(i)
  plt.figure(figsize=(15,5))
  labels = []
  for k in plots[i]:
    plt.plot(xe_s, [ye_s[i][k] for i in range(0, n_epoches)])
    labels.append(k)
  plt.legend(labels, loc='best', bbox_to_anchor=(1, 1))
  if fix_axes:
    plt.axis([1, n_epoches, 0, axs[i]])

  try:
    os.mkdir(root + dir + "\\plots")
  except:
    pass
  try:
    os.mkdir((root + dir + "\\plots" + name))
  except:
     pass
  plt.savefig((root + dir + "\\plots" + name + "\\plot_" + str(i)))

plt.show()
