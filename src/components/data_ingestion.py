import os
import sys  # as we are using custom exception
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

@dataclass  # can be used to directly define class varibale
class DataIngestionConfig:   #any input of data is performed using this class
      train_data_path: str=os.path.join("artifacts","train.csv")
      test_data_path: str= os.path.join("artifacts","test.csv")
      raw_data_path: str =os.path.join("artifacts","raw.csv")
       # can use train_data_path:=os.path.join("artifacts","train.csv")
       #which gives the  train.csv path
       # train_data_path=os.path.join("artifacts","train.csv")
class DataIngestion:
        def __init__(self):
            self.ingestion_config=DataIngestionConfig()
            #so the path given by the data ingestion config will be stored here
        def initiate_data_ingestion(self):
             logging.info("The data ingestion component for training data was added")
             try:
                  df=pd.read_csv(os.path.join("notebook","data","Placement_Data_Full_Class.csv"))
                  os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path),exist_ok=True)
                  df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True )
                  target='status'
                  df=df.drop(['salary'],axis=1)
                  train_set,test_set=train_test_split(df,stratify=df[target],test_size=0.25,random_state=42)
                  logging.info("the train dataset was stored in artifacts")

                  os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
                  train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True )

                  os.makedirs(os.path.dirname(self.ingestion_config.test_data_path),exist_ok=True)
                  test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True )
                  logging.info("the test dataset was stored in artifacts")
                  return(
                         self.ingestion_config.train_data_path,
                         self.ingestion_config.test_data_path,
                         self.ingestion_config.raw_data_path
                   )
             except Exception as e:
                   raise CustomException(e,sys) 
if __name__=="__main__":
      obj=DataIngestion()
      obj.initiate_data_ingestion()