import os
import pandas as pd
import matplotlib.pyplot as plt


results_path = './runs/detect/train_data_set_1/results.csv'

results = pd.read_csv(results_path,  skipinitialspace=True) 

plt.figure()
plt.plot(results['epoch'], results['train/cls_loss'], label='train loss')
plt.plot(results['epoch'], results['val/cls_loss'], label='val loss', c='red')
plt.grid()
plt.title('Loss vs epochs')
plt.ylabel('loss')
plt.xlabel('epochs')
plt.legend()


plt.figure()
plt.plot(results['epoch'], results['metrics/precision(B)'] * 100)
plt.grid()
plt.title('Validation accuracy vs epochs')
plt.ylabel('accuracy (%)')
plt.xlabel('epochs')

plt.show()