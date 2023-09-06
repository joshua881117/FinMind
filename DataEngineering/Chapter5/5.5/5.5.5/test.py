from financialdata.backend.db import *
import financialdata.crawler.taiwan_stock_price as s
import pandas as pd

# data = {'col1':[1,2], 'col2':[3,4]}
# df = pd.DataFrame(data=data)

# # parameter_list = s.gen_task_paramter_list('2021-04-02', '2021-04-06')
# # df = s.crawler(parameter_list[-1])
# # print(df.head())
# # r = get_db_router()


# # print(build_df_update_sql('TaiwanStockPrice', df))
# # sql_list = build_df_update_sql('test', test_df)
# # print(sql_list)
# with r.mysql_financialdata_conn as conn:
#     print(conn)

# with r.mysql_financialdata_conn as conn:
#     print(conn)
data = {"col":[4, 5], 'col2':[7,8]}
df = pd.DataFrame(data=data)

r = get_db_router()
with r.mysql_financialdata_conn as conn:
    db.upload_data(df, 'test', conn)