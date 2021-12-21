# SentimentStockPredict
This project collects the sentiment information from social media and news website and uses these information to predict the stock price trend. It mainly contains following parts——data collector, data management, predicting models.

### 运行方法
安装相关依赖后在根目录下运行
~~~bash
python ui/main.py
~~~

### 各模块说明
#### Data collector
Getting the stock data and the sentiment data<br/>
[twitter 官方API](https://developer.twitter.com/en/docs/tutorials)<br/>
1.从微博等社交平台下载相关内容，并保存为字典格式。（内容发布的时间、内容文本、用户等信息）(√)<br/>
2.下载指数或各股票历史数据，保存至csv文件。(√)<br/>


#### Data management
Data saving process and database query<br/>
1.将下载到的数据存储至本地数据库，方便查询。数据库可以采用sqlite3/mysql/mongodb等。(√)<br/>
2.实现从数据库中读取特定时间段的数据，统计特定单词出现的频率，能够实现查询功能。（sql相关语句）()<br/>



#### Predicting models
Models to predict how the price of stock will change<br/>
1.分析股票走势及收益与舆情之间的关系。<br/>
2.构建相关分类或预测模型，预测股票未来价格走势，评价模型表现。<br/>

#### Engine
Update data, backtest and realtime test<br/>
1.定期更新数据库数据。( )<br/>
2.回测检验模型的效果。( )<br/>
3.实际效果测试。( )<br/>

#### UI
Interface for convenient use<br/>
设计软件界面整合功能。 <br/>
UI使用Qt和PyDracular框架开发，目前只完成了爬取下载部分功能。(√)<br/>
尚未完成：本地数据保存、数据可视化。()<br/>
