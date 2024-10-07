import matplotlib.pyplot as plt 
from scipy import stats
import numpy as np 
from .outlier_detection import OutlierDetection


def visualization_norm(df_x,df_y):
    
    # first organize data: 
    x_extended = df_x.iloc[:,:].values
    x = np.mean(x_extended,axis=1)
    x = x.reshape(x_extended.shape[0],1)

    y_extended = df_y.iloc[:,:].values
    y = np.mean(y_extended, axis=1)
    y = y.reshape(y_extended.shape[0],1)
    
    #----------------------------------------------------------------------
    # visualization data raw:

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    ax[0].hist(y, bins=30, edgecolor='black')
    ax[0].set_title('data raw ')
    ax[0].set_xlabel('Values')
    ax[0].set_ylabel('Quantity')
    #--------------------------------------------------------------------
    # visualization data after outlier detection: 
    _, data_y = OutlierDetection(x,y).run()

    ax[1].hist(data_y , bins=30, edgecolor='black')
    ax[1].set_title('without outlier')
    ax[1].set_xlabel('Values')
    ax[1].set_ylabel('Quantity')
    plt.tight_layout()
    plt.show()     