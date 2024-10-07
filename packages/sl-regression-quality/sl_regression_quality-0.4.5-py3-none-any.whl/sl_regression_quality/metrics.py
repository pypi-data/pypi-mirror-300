"""
Assumption calculation:
1) linearity
2) normality
3) homocedasticity
4) independence

"""


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import statsmodels.api as sm
from numpy.linalg import inv
from scipy import stats
import numpy as np

from statsmodels.compat import lzip
import statsmodels.stats.api as sms
from statsmodels.stats.stattools import durbin_watson
from .global_constants import GREEN, RED,  RESET

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


class Metrics:
    def __init__(self,data_x,data_y,significance_level,value_dl,value_du) -> None:
        self.data_x = data_x
        self.data_y = data_y
        self.alpha = significance_level
        self.value_dl = value_dl
        self.value_du = value_du

        self.model_RLS = None
        self.standardized_residuals = None
        self.studentized_residuals = None
        self.enable_outlier = False
        self.x_one = None


        #run linear regression:
        self.linear_regression()
#-------------------------------------------------------------------------------
    def linear_regression(self):

        self.x_one = sm.add_constant(self.data_x)
        self.model_RLS=sm.OLS(self.data_y, self.x_one).fit()
        self.model_RLS.summary()
#--------------------------------------------------------------------------
    def linearity(self):
        value_linearity =  self.model_RLS.f_pvalue


        #1) validation:
        if value_linearity < self.alpha:
            print('1.2.1)'+GREEN+f'Satisfies linearity ({round(value_linearity,4) } < {self.alpha})'+RESET)
            enable_linearity = True
        else:
            print('1.2.1)'+RED+f'Does not satisfies linearity ({round(value_linearity,4) } < {self.alpha})'+RESET)
            enable_linearity = False


        return  enable_linearity
#-------------------------------------------------------------------------------
    def normality(self):


        #main:
        XTr=self.x_one.transpose()
        XM=np.dot(XTr,self.x_one )
        iXM=inv(XM)
        Mxi=np.dot(self.x_one , iXM)
        H=np.dot(Mxi,XTr)
        yPred=np.dot(H,self.data_y)
        Res=self.data_y-yPred
        #perform Shapiro-Wilk Test
        value_normality = stats.shapiro(Res).pvalue

        #1) validation:
        if value_normality > self.alpha:
            print('1.2.2)'+GREEN+ f'Satisfies normality ({round(value_normality,4)} > {self.alpha})'+RESET)
            enable_normality = True
        else:
            print('1.2.2)'+RED+ f'Does not satisfies normality ({round(value_normality,4)} > {self.alpha})'+RESET)
            enable_normality = False
        
        return enable_normality
#----------------------------------------------------------------------------------
    def homocedasticity(self):

        names=['Lagrange multiplier statistic', 'p-value','f-value', 'f p-value']
        test=sms.het_breuschpagan(self.model_RLS.resid, self.model_RLS.model.exog)
        values = lzip(names, test)

        value_homocedasticity = values[1][1]

        #1) validation:
        if value_homocedasticity > self.alpha:
            print('1.2.3)'+GREEN+f'Satisfies homoscedasticity ({round(value_homocedasticity,4)} > {self.alpha})'+RESET)
            enable_homocedasticity = True
        else:
            print('1.2.3)'+RED+ f'Does not satisfies homoscedasticity ({round(value_homocedasticity,4)} > {self.alpha})' +RESET)
            enable_homocedasticity = False

        return enable_homocedasticity

#-----------------------------------------------------------------------------------------

    def independence(self):
        value_dL = self.value_dl
        value_dU = self.value_du

        #main:
        value_independence = durbin_watson(self.model_RLS.resid)

        #1) validation:
        if value_independence <2:
            if value_independence >value_dU:
                print('1.2.4)'+GREEN+ f'Satisfies independence ({round(value_independence,4)} > dU)'+RESET)
                enable_independence  = True
            elif value_independence < value_dL:
                print('1.2.4)'+RED+ f'Does not satisfies independence ({round(value_independence,4)} < dL)'+RESET)
                enable_independence  = False
            else:
                print('1.2.4)'+RED+ f'Test is inconclusive ({round(value_independence,4)} > dU)' +RESET)
                enable_independence  = False

        elif value_independence >2:
            if (4-value_independence)>value_dU:
                print('1.2.4)'+GREEN+ f'Satisfies independence ({round(4-value_independence,4)} > dU)'+RESET)
                enable_independence  = True
            elif (4-value_independence)<value_dL:
                print('1.2.4)'+RED+f'Does not satisfies independence ({round(4-value_independence,4)} < value_dL)'+RESET)
                enable_independence  = False
            else:
                print('1.2.4)'+RED+f"Test is inconclusive ({round(4-value_independence,4)} > dU)"+RESET)
                enable_independence  = False

        return enable_independence

#-----------------------------------------------------------------------------------------
    def run(self):
        print('----'*20)

        # 1) normality
        # 2) homoscedasticity
        # 3) independence 
        # 4) linearlity

        enable_norm = self.normality()

        if enable_norm:
            enable_homo = self.homocedasticity()
            if enable_homo:
                enable_inde = self.independence()
                if enable_inde:
                    enable_line = self.linearity()
                    return enable_line 
                else:
                    return False
                
            else: 
                return False
        else: 
            return False
             




        # #1) linearity:
        # enable_line = self.linearity()
        # #2) normality:
        # if enable_line:
        #     enable_norm = self.normality()

        #     if enable_norm:
        #         enable_homo = self.homocedasticity()

        #         if enable_homo:
        #             enable_inde = self.independence()
        #             return enable_inde
        #         else:
        #             return False

        #     else:
        #          return False
        # else:
        #     return False
        
