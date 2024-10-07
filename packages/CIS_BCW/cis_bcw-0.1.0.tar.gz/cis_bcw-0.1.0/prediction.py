import numpy as np
import pandas as pd

class CIS_bcw():
    def __init__(self):
        self.alpha = 0.97
        self.sensor_columns = ['Sensor1', 'Sensor2', 'Sensor3', 'Sensor4']

    # Low-pass filter function
    def low_pass_filter(self, x_meas, x_esti):
        """Calculate average using a low-pass filter."""
        return self.alpha * x_esti + (1 - self.alpha) * x_meas


    def predict(self, data):
        df = pd.DataFrame(data, columns=self.sensor_columns)
        # print(df.info())
        S_avg = df.iloc[0]
        # print(S_avg)
        current_values = df.iloc[1:]
        # print(current_values.info())
        for i in range(4):
            current_values = current_values.assign(**{f'Sensor{i+1}_filter':self.low_pass_filter(current_values.iloc[:,i], S_avg.iloc[i])})
            delta = current_values.iloc[:,i] - S_avg.iloc[i]
            threshold = current_values.iloc[:,i].std()
            current_values.loc[:,f'Sensor{i+1}_status'] = 0
            current_values.loc[delta > threshold, f'Sensor{i+1}_status'] = 1
            current_values.loc[delta < threshold, f'Sensor{i+1}_status'] = -1
        current_values.loc[:,'Label'] = 'AIR'
        current_values.loc[(current_values['Sensor3_status']==1)&(current_values['Sensor4_status']==-1),'Label']='MES'
        current_values.loc[(current_values['Sensor3_status']==1)&(current_values['Sensor4_status']==1),'Label']='SF6'
        return current_values.iloc[:,-1].value_counts().idxmax()