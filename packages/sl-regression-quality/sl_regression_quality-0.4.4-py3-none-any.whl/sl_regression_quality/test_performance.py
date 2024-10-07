"""
Calls all functions and classes to generate the complete analysis:
1) calculation of assumptions
2) quality of the regression

"""


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from art import text2art
import numpy as np
import time 

from .outlier_detection import OutlierDetection
from .metrics import Metrics
from .parameters import Parameters
from .resolution import resolution
from .user_messages import parameters_messages
from .global_constants import BLUE,  RESET, RED, YELLOW
from .ram_consumption import memory_usage_psutil

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def regression_quality_performance(df_x,df_y,alpha,dL,dU,enable_outlier=True,return_time=True):

    elapsed_time_outlier = -10
    elapsed_time_metrics = -10
    elapsed_time_parameters = -10

    #--------------------------------------------------------------------------------------
    space_1 = '            '
    space_2 = '                  '
    art_text1 = text2art("SIMPLE    LINEAR") 
    art_text2 = text2art(space_1+"REGRESION")  
    art_text3 = text2art(space_2+"QUALITY")  
   
    print(art_text1)
    print(art_text2)
    print(art_text3)
    

    #------------------------------------------------------------------------------------
    # first organize data: 
    x_extended = df_x.iloc[:,:].values
    x = np.mean(x_extended,axis=1)
    x = x.reshape(x_extended.shape[0],1)

    y_extended = df_y.iloc[:,:].values
    y = np.mean(y_extended, axis=1)
    y = y.reshape(y_extended.shape[0],1)

    #------------------------------------------------------------------------------------
    # 1) part:
    print(BLUE+'===='*20+RESET)
    print(BLUE+'part 1, Assumption calculation: '+RESET)
    print(BLUE+'===='*20+RESET)
    

    if enable_outlier:
        print('part 1.1, outlier identification: ')
        start_time_outlier = time.time()
        new_x, new_y = OutlierDetection(x,y).run()
        ram_outlier = memory_usage_psutil()
        end_time_outlier = time.time()
        elapsed_time_outlier = end_time_outlier - start_time_outlier

        print(YELLOW+ f"Elapsed time (outlier): {round(elapsed_time_outlier,2)} seconds."+ RESET)
        print(YELLOW+ f"Memory usage (outlier): {round(ram_outlier,2)} MB."+ RESET)
        print('----'*20)
    else: 
        print(YELLOW+'part 1.1, outlier identification: unrealized'+RESET)
        new_x, new_y = (x,y)


    #--------------------------------------------------------------------------------------
    # 2) part:
    print('part 1.2, Verification of: ')

    start_time_metrics = time.time()
    enable_metrics = Metrics(new_x,new_y,alpha,dL,dU).run()
    ram_metrics = memory_usage_psutil()
    end_time_metrics = time.time()
    elapsed_time_metrics = end_time_metrics - start_time_metrics

    print(YELLOW+ f"Elapsed time (assumption): {round(elapsed_time_metrics,2)} seconds."+ RESET)
    print(YELLOW+ f"Memory usage (assumption): {round(ram_metrics ,2)} MB."+ RESET)

    #--------------------------------------------------------------------------------------
    # 3) part:
    print(BLUE+'===='*20+RESET)

    if enable_metrics:
        print(BLUE+'part 2, Regression quality: '+RESET)
        print(BLUE+'===='*20+RESET)

           
        #------------------------------------------
        start_time_parameters = time.time() 
        accuracy,d_range,sensitivity = Parameters(new_x,new_y).run()              
        res_value = resolution(y_extended,alpha)
        ram_parameters = memory_usage_psutil() 
        end_time_parameters = time.time()
        #-----------------------------------------
        parameters_messages(accuracy,res_value,sensitivity,d_range)
        
        
        elapsed_time_parameters = end_time_parameters  - start_time_parameters 

        print(YELLOW+ f"Elapsed time (quality): {round(elapsed_time_parameters ,2)} seconds."+ RESET)
        print(YELLOW+ f"Memory usage (quality): {round(ram_parameters ,2)} MB."+ RESET)

    else:
        print(RED +'Not all assumptions were met'+RESET)

    #-----------------------------------------------------------------------------------------------------
    if return_time: 
        return elapsed_time_outlier, elapsed_time_metrics, elapsed_time_parameters,ram_outlier,ram_metrics,ram_parameters
    
    print(BLUE+'===='*20+RESET)