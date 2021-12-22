import pandas as pd

class inputtext():
    def __init__(self):
        pass

    def handletxt(self,filepath):
        df=pd.DataFrame()
        try:
            df=pd.read_csv(filepath,header=None,error_bad_lines=False)
        except Exception:
            raise Exception("not find file!")
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        df.columns=["id","time","likes","comment","share","text"]
        df.reset_index(inplace=True,drop=True)
        print(df)
        return df
    
    def gettext_day(self,filename,date):
        filepath="/home/zhou/Desktop/code/mygit/SentimentStockPredict/{}".format(filename)
        df=self.handletxt(filepath)
        df["date"]=df["time"].apply(lambda x:x[:10])
        return df[df["date"]==date]["text"].tolist()
    
    def gettext_days(self,filename,startdate,enddate):
        filepath="/home/zhou/Desktop/code/mygit/SentimentStockPredict/{}".format(filename)
        df=self.handletxt(filepath)
        df["date"]=df["time"].apply(lambda x:x[:10])
        return df[df["date"]>=startdate][df["date"]<=enddate]["text"].tolist()


    def remove_stopword(self,text):
        stopwords=[line.strip() for line in open('data/cn_stopwords.txt', encoding='UTF-8').readlines()]
        newtext=[]
        for sentence in text:
            newsentence=[]
            for t in sentence:
                if t not in stopwords and t not in ['\\u3000']:
                    newsentence.append(t)
            newtext.append(newsentence)
        return newtext
            