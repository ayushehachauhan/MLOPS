import sys
import os
from dataclasses import dataclass


import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.compose import ColumnTransformer

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
from src.components.data_ingestion import DataIngestionConfig,DataIngestion


@dataclass
class DataTransformationConfig:
    preprocessor_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()


        
    def get_data_transformer_object(self):
        try:
            numerical_features=['sl_no', 'ssc_p', 'hsc_p', 'degree_p', 'etest_p', 'mba_p']
            categorical_features=['gender', 'ssc_b', 'hsc_b', 'hsc_s', 'degree_t', 'workex',
       'specialisation']
            num_pipeline=Pipeline(
            steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                     ("Scaler",StandardScaler())
                 ]
                )
                                  
            logging.info("numerical columns were standar scaled")
            cat_pipeline=Pipeline(
            steps=[
            ('imputer',SimpleImputer(strategy="most_frequent")),
            ("one_hot_encoder",OneHotEncoder())
                                                      ]
            )
            logging.info("categorical columns encoded")

            preprocessor=ColumnTransformer(
                   [
                    ("num pipeline",num_pipeline,numerical_features),
                    ("cat features",cat_pipeline,categorical_features)
                      ] )
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("reading train and test data completed")

            preprocssesing_object= self.get_data_transformer_object()
            logging.info("obtained preprocessor object")


            target_column_name="status"
            x_train=train_df.drop(columns=[target_column_name],axis=1)
            x_test=test_df.drop(columns=[target_column_name],axis=1)


            x_train = preprocssesing_object.fit_transform(x_train)
            x_test = preprocssesing_object.transform(x_test)



            y_train=train_df["status"].map({'Placed':1,'Not Placed':0})
            y_test=test_df["status"].map({'Placed':1,'Not Placed':0})
            

            # creating train and test array

            training_array=np.c_[x_train,y_train]
            test_array=np.c_[x_test,y_test]
            logging.info("training and test data were completed")

            path=self.data_transformation_config.preprocessor_file_path

            save_object(
                obj=preprocssesing_object,
                path=path)
            return (
                training_array,
                test_array,
                self.data_transformation_config.preprocessor_file_path
            )
             
            

        except Exception as e:
            raise CustomException(e,sys)
                                      
if __name__=="__main__":
    obj=DataIngestion()
    train_data_path,test_data_path,raw_data_path=obj.initiate_data_ingestion()

    obj2=DataTransformation()
    obj2.initiate_data_transformation(train_path=train_data_path,test_path=test_data_path)
    
             

