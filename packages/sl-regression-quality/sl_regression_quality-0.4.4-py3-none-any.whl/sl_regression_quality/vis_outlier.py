import numpy as np 

from .outlier_detection import OutlierDetection



def visualization_residuals(df_x,df_y):

    #------------------------------------------------------------------------------------
    # first organize data: 
    x_extended = df_x.iloc[:,:].values
    x = np.mean(x_extended,axis=1)
    x = x.reshape(x_extended.shape[0],1)

    y_extended = df_y.iloc[:,:].values
    y = np.mean(y_extended, axis=1)
    y = y.reshape(y_extended.shape[0],1)

    #------------------------------------------------------------------------------------
                   
    OutlierDetection(x,y).visualization()
        
     
 