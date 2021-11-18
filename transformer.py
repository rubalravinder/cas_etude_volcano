# TACHE : empilement de pipelines avec l'aide d'une classe transformer qui:
#   - récupérer à partir des 2 1eres colonnes du fichier association_table_corrected_index.xlsx le nom du fichier numpy
#   - créer un chemin pour aller récupérer les données du fichier numpy

import pandas as pd
import numpy as np
import os
from sklearn.base import TransformerMixin
from pathlib import Path
from scipy import stats
import math
from numpy.fft import fft 
from scipy import fftpack


class Transformer(TransformerMixin):

    def __init__(self, directory_path):
        self.directory_path = directory_path
#       directory_path : absolute path of the directory containing all folders of numpy files (until Extracted/)
#                        /!\ DO NOT FORGET TO END THE STRING BY THE CHARACTER '/'
    
    def get_event_and_file_name(self, catalog_file, index:int):
        """
        Input :
            - catalog_file : table associating the files with their information and indexes
            - index : index of the desired file row in the catalog_file
        Output : event associated with file, directory where the file is stored and string with the name of the file
        """
        list_of_file_directories = ['EXP','HIB','LP','PIS','TOR','TR','VT']
        event = catalog_file.loc[index,'Event']

        # on supprime le dernier caractère pour avoir le nom du dossier où est le fichier
        if event not in list_of_file_directories:
            event_without_last_digit = event[:-1]
            name = str(event_without_last_digit + '_' + str(index))
            return event_without_last_digit, name
        else:
            name = str(event + '_' + str(index))
            return event, name

    def put_event_in_df(self,catalog_file):
        """
        Input :
            - catalog_file : table associating the files with their information and indexes
        Output : creates a column in the dataframe for the type of event
        """
        for idx in catalog_file.index:
            try :
                event, name = self.get_event_and_file_name(catalog_file, idx)
                catalog_file.loc[idx, 'event'] = event
            except:
                pass
        return catalog_file
    
    def get_file_path(self, catalog_file, index):
        """
        Input :
            - catalog_file : table associating the files with their information and indexes
            - index : index of the desired file row in the catalog_file
        Output : return the relative path for the desired file
        """
        # on récupère le nom de l'event (dossier dans lequel est rangé le fichier) et du fichier
        event, name = self.get_event_and_file_name(catalog_file, index)
        
        # on crée un string pour avoir le chemin du fichier
        end_folder_path = str(event + '/' + name + '.npy')
        final_path = self.directory_path + end_folder_path
        return final_path
    
    def put_path_in_df(self, catalog_file):
        """
        Input :
            - catalog_file : table associating the files with their information and indexes
        Output : creates a column in the dataframe for the file path of each numpy file
        """
        for idx in catalog_file.index:
            try :
                path = self.get_file_path(catalog_file, idx)
                catalog_file.loc[idx, 'path'] = path
            except:
                pass
        return catalog_file

    def open_file(self, catalog_file, index):
        """
        Input :
            - catalog_file : table associating the files with their information and indexes
            - index : index of the desired file row in the catalog_file        
        Output : loads the file at the desired index
        """
        # on récupère le chemin menant au fichier
        path = self.get_file_path(catalog_file, index)
        
        if os.path.exists(path):
            file = np.load(path) # on ouvre le fichier seulement s'il existe
            return file
        else:
            pass
        
    def TF(self, data:np.ndarray)->np.ndarray:  
        
        tfd = fft(data)
        N=len(data)
        spectre = np.absolute(tfd)*2/N  
        return spectre   
    
    
    def get_info_from_file(self, catalog_file, index):
        """
        Input : 
            - catalog_file : table associating the files with their information and indexes
            - index : index of the desired file row in the catalog_file        
        Output : Returns a tuple with the variance, mean, median, maximum and amplitude of the numpy array
        """        

        # try:
        data = self.open_file(catalog_file, index)
        data_TF = self.TF(data)
        
        variance = np.var(data)
        mean = np.mean(data)
        median = np.median(data)            
        maximum = np.amax(data)
        minimum = np.amin(data)
        amplitude = maximum - minimum
        kurtosis= stats.kurtosis(data)
        skew=stats.skew(data)  
        variance_TF = np.var(data_TF)
        mean_TF = np.mean(data_TF)
        median_TF = np.median(data_TF)            
        maximum_TF = np.amax(data_TF)
        minimum_TF = np.amin(data_TF)
        amplitude_TF = maximum_TF - minimum_TF
        kurtosis_TF= stats.kurtosis(data_TF)
        skew_TF=stats.skew(data_TF) 
        
        return variance, mean, median, maximum, amplitude, kurtosis, skew, variance_TF, mean_TF, median_TF, maximum_TF,                        amplitude_TF, kurtosis_TF, skew_TF
        # except:
        #     pass
       
      
    
    def supp_columns(self, catalog_file, columns_to_supp=["File name","File start" ,"File end" ,"Unnamed: 10" ,"Unnamed: 11" ,"Unnamed: 12"]):
        """
        Input :
            - catalog_file : table associating the files with their information and indexes
            - columns_to_supp : list of columns names to delete from the dataframe catalog_file. If None, following
                                columns are deleted : ["File name","File start" ,"File end" ,"Unnamed: 10" ,"Unnamed: 11" ,"Unnamed: 12"] 
        Output : returns the dataframe catalog_file cleant from unused columns
        """
        catalog_file.drop(columns_to_supp, axis=1, inplace=True)
        return catalog_file
    
    def put_info_in_df(self, catalog_file):
        """
        Input :
            - catalog_file : table associating the files with their information and indexes
        Output : creates a different column for variance, mean, median, maximum and amplitude of each numpy array.
        """
        for idx in catalog_file.index:
            
            # try :
            variance, mean, median, maximum, amplitude, kurtosis, skew , variance_TF , mean_TF, median_TF, maximum_TF,                                              amplitude_TF, kurtosis_TF, skew_TF = self.get_info_from_file(catalog_file, idx)
            
            catalog_file.loc[idx, 'variance'] = variance
            catalog_file.loc[idx, 'mean'] = mean
            catalog_file.loc[idx, 'median'] = median
            catalog_file.loc[idx, 'maximum'] = maximum
            catalog_file.loc[idx, 'amplitude'] = amplitude
            catalog_file.loc[idx, 'kurtosis'] = kurtosis
            catalog_file.loc[idx, 'skew'] = skew
            catalog_file.loc[idx, 'variance_TF']=variance_TF
            catalog_file.loc[idx, 'mean_TF']=mean_TF
            catalog_file.loc[idx, 'median_TF']=median_TF
            catalog_file.loc[idx, 'maximum_TF'] = maximum_TF
            catalog_file.loc[idx, 'amplitude_TF']= amplitude_TF        
            catalog_file.loc[idx, 'kurtosis_TF']=kurtosis_TF
            catalog_file.loc[idx, 'skew_TF'] = skew_TF            
                             
            
            # except:
            #     pass
        return catalog_file

    def fit_transform(self, X):
        """
        Input :
            - X : array-like of shape (n_samples, n_features)
        Output : returns a fit_transformed X array
        """
        X_copy = X.copy()
        X_with_event = self.put_event_in_df(X_copy)
        X_with_path = self.put_path_in_df(X_with_event)
        X_supp_cols = self.supp_columns(X_with_path)
        X_add_cols = self.put_info_in_df(X_supp_cols)
        return X_add_cols

class Event(TransformerMixin):

    def __init__(self):
        self.list_of_file_directories = ['EXP','HIB','LP','PIS','TOR','TR','VT']

    def get_event(self, event:str):
        """
        Input :
            - event : the full name string of the event name
        Output : event associated with file, directory where the file is stored and string with the name of the file
        """

        # on supprime le dernier caractère pour avoir le nom du dossier où est le fichier
        if event not in self.list_of_file_directories:
            return event[:-1]
        else:
            return event

    def put_event_in_df(self,df):
        """
        Input :
            - df : table associating the files with their information and indexes
        Output : creates a column in the dataframe for the type of event
        """
        event_list = []
        for idx, row in df.iterrows():
            event_list.append(self.get_event(row.Event))
        df["event"] = event_list

    def fit_transform(self, X):
        """
        Input :
            - X : array-like of shape (n_samples, n_features)
        Output : returns a fit_transformed X array
        """
        X_copy = X.copy()
        self.put_event_in_df(X_copy)
        return X_copy


if __name__ == '__main__':
    print('class Transformer and Event successfully imported')