# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:23:46 2023

@author: Franco, Bruno Agustín 
         
DP4+ parameterization module
It uses the DP4+ nmr correlation and calculation modules, as well as having 
its own functions to complete the proccess. 
"""

from PyQt5.QtCore import QThread, pyqtSignal


import pandas as pd
import numpy as np
import scipy.stats as st
import os

##### AGREGAR RELATIVE IMPORTS 
from . import correlation_module as nmr_correl
from . import dp4_module as dp4
from . import bugs_a_warning_module as warn
from . import output_module as output

def add_errors(e_vectors, df_selections, uns_e, sca_e):
    '''Attaches the errors of a molecule to the global parameterization sets
    '''
    e_vectors['Csca'] = np.append(e_vectors['Csca'], sca_e[df_selections['C']])
    e_vectors['Hsca'] = np.append(e_vectors['Hsca'], sca_e[df_selections['H']])
    
    e_vectors['Csp2'] = np.append(e_vectors['Csp2'], uns_e[df_selections['C_sp2']])
    e_vectors['Csp3'] = np.append(e_vectors['Csp3'], uns_e[df_selections['C_sp3']])
    
    e_vectors['Hsp2'] = np.append(e_vectors['Hsp2'], uns_e[df_selections['H_sp2']])
    e_vectors['Hsp3'] = np.append(e_vectors['Hsp3'], uns_e[df_selections['H_sp3']])
    
    return e_vectors

def get_parameters(e_vectors):
    '''Estimates the parameters of the t studen probability distribution
    '''
    # out_file = os.path.normpath(os.path.expanduser("~/Desktop"))
    # out_file = os.path.join(out_file,'Qt_temp_Train.xlsx')
    # with pd.ExcelWriter(out_file) as writer:     
    #     for label,data in e_vectors.items(): 
    #         temp = pd.DataFrame(data)
    #         temp.to_excel(writer, sheet_name=label)
    
    param = pd.DataFrame(columns=['n', 'm', 's'],
                         index = ['Csp3','Csp2','Csca',
                                  'Hsp3','Hsp2','Hsca'])
    
    param.loc['Csca'] = st.t.fit(e_vectors['Csca'])
    param.loc['Hsca'] = st.t.fit(e_vectors['Hsca'])
    
    param.loc['Csp2'] = st.t.fit(e_vectors['Csp2'])
    # print (len (e_vectors['Csp3']))
    # print (st.t.fit(e_vectors['Csp3']))
    param.loc['Csp3'] = st.t.fit(e_vectors['Csp3'])
    
    param.loc['Hsp2'] = st.t.fit(e_vectors['Hsp2'])
    param.loc['Hsp3'] = st.t.fit(e_vectors['Hsp3']) 
    
    param.loc['Csca','m'] = 0.0
    param.loc['Hsca','m'] = 0.0
    
    return param

class train_Thread(QThread):
    '''DOC STRING
    DOC STRING
    DOC STRING
    '''  
    results = pyqtSignal(pd.DataFrame, dict, bool)
    finished = pyqtSignal(dict)
    message = pyqtSignal(str)  
    correlation_warn = pyqtSignal(str)
    
    def __init__(self, thelev_name, dirname, xlsname, molecules:list):
        super().__init__()
        
        self.thelev_name = thelev_name
        self.dirname = dirname
        self.xlsname = xlsname
        self.molecules = molecules
        
    
    def run(self):
        warn_flag = False
        small_sample = False
            
        # Start calculation -------------------------------------------------
        os.chdir(self.dirname)
        self.message.emit("Starting training ")
        
        tms_tens = nmr_correl.collect_G09_data(['tms'], self.dirname ) 
        tms_tens = tms_tens['tms'].iloc[:,0]        
        tms_tens = pd.Series(tms_tens)
        tms_tens = tms_tens.groupby(tms_tens).mean()
        
        tms_tens = {'H': tms_tens.iloc[(tms_tens - 30).abs().argmin()],
                    'C': tms_tens.iloc[(tms_tens - 190).abs().argmin()] }
        
        
        e_vectors = {'Csca':np.empty(0), 'Csp2':np.empty(0), 'Csp3':np.empty(0),
                    'Hsca':np.empty(0), 'Hsp2':np.empty(0), 'Hsp3':np.empty(0)}
        
        for molec in self.molecules:
            if 'tms' in molec : continue
            exp_data, wtl = nmr_correl.get_exp_data(self.xlsname, molec)
            df_selections = nmr_correl.selections(exp_data)
            
            tens_by_conf_a_molec = nmr_correl.collect_G09_data([molec], self.dirname)
            tens_by_molec = nmr_correl.Boltzman_pond (tens_by_conf_a_molec[molec])
            tens_by_molec = tens_by_molec[:,np.newaxis]
            tens_by_molec_sorted = nmr_correl.sort_tens_matrix(tens_by_molec, [molec], exp_data, wtl) 
            if type(tens_by_molec_sorted) == str : 
                self.finished.emit({'statusBar': u"Calculation aborted \u2717",
                                    'popupTitle': u'Calculation aborted \u2717', 
                                    'popupText': f'''Attention:
    The calculation was aborted because in molecule: {molec} labels: {tens_by_molec_sorted} could not be matched with its corresponding nucleus. 
    Please correct the correlation file and try again.'''})
                return 
            
            uns = dp4.get_uns_shifts(tens_by_molec_sorted,df_selections, tms_tens )
            sca = dp4.get_sca_shifts(uns, df_selections, exp_data)
            
            uns_e = dp4.calc_errors(uns,exp_data)
            sca_e = dp4.calc_errors(sca,exp_data)
            
            e_hl = warn.sca_e_control(exp_data, sca_e)
            exp_hl = warn.exp_data_control(exp_data)
            if e_hl + exp_hl: 
                  output.add_highlights_warn(self.xlsname, molec, 
                                            e_hl, exp_hl)
                  warn_flag = True
            
            e_vectors = add_errors(e_vectors, df_selections, uns_e, sca_e)
            
        self.param  = get_parameters(e_vectors)
        if any (len(vector)<150 for e_type,vector in e_vectors.items()): 
            small_sample = True 
        
        self.message.emit("Finishing training ")
        
        if warn_flag :
            self.correlation_warn.emit('''Attention:
Some possiible errors were found in the correlation spread sheet
Check the highlights in {e_hl + exp_hl}
It is recommended to correct the inconsistency''')

        self.finished.emit({})

        self.results.emit (self.param , tms_tens, small_sample )
        # DEVOLVER LOS PARAMETROS, EL STANDARD Y SI HAY Q CAMBIAR LOS NHU

            
    
    
