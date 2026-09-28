import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import evaluate_model,save_object
import sys
import os
from src.components.data_ingestion import DataIngestionConfig,DataIngestion
from src.components.data_transformation import DataTransformationConfig,DataTransformation


@dataclass
class ModelTrainerConfig:
    trained_model_file_path=os.path.join("artifacts","model.pkl")
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("spliting the features and target")
            x_train,y_train,x_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]

            )
            models={
                "Random Forest": RandomForestClassifier(**{'class_weight': 'balanced_subsample',
                                                            'criterion': 'entropy',
                                                            'max_depth': 5,
                                                            'max_features': 'log2',
                                                            'n_estimators': 100})
                                                                }

            model_report:dict=evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models)


            max=0
            best_model_name=""
            for key,value in model_report.items():
                average=(value["f1 score"] +value["roc auc score"])
                if average>max:
                    max=average
                    best_model_name=key

                else:
                    pass


            best_model=[best_model_name]

            
            logging.info(f"best model was found to be {best_model_name}")
            save_object(
                path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )
            return model_report

        except Exception as e:
            raise CustomException(e,sys)


if __name__=="__main__":

    obj=DataIngestion()
    train_data_path,test_data_path,raw_data_path=obj.initiate_data_ingestion()

    obj2=DataTransformation()
    train_array,test_array,_=obj2.initiate_data_transformation(train_path=train_data_path,test_path=test_data_path)

    trainer=ModelTrainer()
    print(trainer.initiate_model_trainer(train_array=train_array,test_array=test_array))

