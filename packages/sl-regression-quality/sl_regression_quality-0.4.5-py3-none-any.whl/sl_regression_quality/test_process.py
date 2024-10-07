from .main_routine import regression_quality
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

from .vis_outlier import visualization_residuals
from .vis_norma import visualization_norm
from .test_performance import regression_quality_performance


### CREATION OF DATABASE
x=np.arange(0,4400).reshape((-1, 1))
np.random.seed(42)
deltaN1=np.random.normal(0,1,size=4400).reshape((-1, 1))
#plt.hist(deltaN1, bins=50) # Sólo para ver la distribución de delta
# deltaN2=np.random.normal(20,2,size=25).reshape((-1, 1))
# deltaNN=np.hstack((deltaN1,deltaN2)).reshape((-1, 1))
y=0.39998034*x+70.05474142+deltaN1

# "Dispersión de x y y"
# plt.scatter(x,y)
# plt.xlabel('x', fontsize=18)
# plt.ylabel('y', fontsize=18)
# plt.xticks(fontsize=20)
# plt.yticks(fontsize=20)
# plt.show()


#----------------------------------------------------------------------------------------------------

df_x = pd.DataFrame({
    'Columna1': x.reshape(-1),
    'Columna2': x.reshape(-1),
    'Columna3': x.reshape(-1)
})



df_y = pd.DataFrame({
    'Columna1': y.reshape(-1),
    'Columna2': y.reshape(-1),
    'Columna3': y.reshape(-1)
})

df_x.to_csv("X_test1.csv", index=False)
df_y.to_csv("Y_test1.csv", index=False)



dataset_x = pd.read_csv('X_test1.csv') # example data (uncomment line)
dataset_y = pd.read_csv('Y_test1.csv') # example data (uncomment line)


alpha = 0.05 # significance level
dL = 1.758 # dL
dU = 1.778 # dU


# process validation: 
regression_quality(dataset_x  ,dataset_y  ,alpha,dL,dU)
visualization_residuals(dataset_x  ,dataset_y )
visualization_norm(dataset_x  ,dataset_y )
regression_quality(dataset_x  ,dataset_y ,alpha,dL,dU,enable_outlier=False)


time_outlier, time_assumption, time_quality = regression_quality_performance (dataset_x  ,dataset_y, alpha,dL,dU)

print(f'out: {time_outlier}')
print(f'out: {time_assumption}')
print(f'out: {time_quality}')


time_outlier, time_assumption, time_quality = regression_quality_performance (dataset_x  ,dataset_y, alpha,dL,dU,enable_outlier=False)

print(f'out: {time_outlier}')
print(f'out: {time_assumption}')
print(f'out: {time_quality}')

