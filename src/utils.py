import os 
import sys
from src.exception import CustomException
import dill



def save_object(obj,path):
    try:
        dir_path=os.path.dirname(path)
        os.makedirs(dir_path,exist_ok=True)

        with open(path,"wb") as file_obj:
            dill.dump(obj,file_obj)
    


    except Exception as e:
        raise CustomException(e,sys)





def evaluate_model(x_train,y_train,x_test,y_test,models):
    from sklearn.metrics import f1_score,roc_auc_score
    try:
        report={}
        for key,value in models.items():
            model=value
            model.fit(x_train,y_train)
            y_pred=model.predict(x_test)
            y_pred_proba=model.predict_proba(x_test)[:,1]
            repo={"f1 score":f1_score(y_test,y_pred),"roc auc score":roc_auc_score(y_test,y_pred_proba),"roc auc score (prob)":roc_auc_score(y_test,y_pred_proba)}
            report[key]=repo
        return report
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)