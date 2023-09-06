import importlib
import sys

from loguru import logger

from financialdata.backend import db
from financialdata.tasks.task import crawler



def Update(dataset: str, start_date: str, end_date: str):
    # 拿取每個爬蟲任務的參數列表，
    # 包含爬蟲資料的日期 date，例如 2021-04-10 的台股股價，
    # 資料來源 data_source，例如 twse 證交所、tpex 櫃買中心
    parameter_list = getattr(
        importlib.import_module(f"financialdata.crawler.{dataset}"),
        "gen_task_paramter_list",
    )(start_date=start_date, end_date=end_date)
    # 用 for loop 發送任務
    for parameter in parameter_list:
        logger.info(f"{dataset}, {parameter}")
        task = crawler.s(dataset, parameter)
        # 異步執行：在執行多個爬蟲 request 時不需要等到前一個回傳資料後才執行下一個 request
        # apply_async() 方法可以方便地将任务提交到 Celery 任务队列中，以实现后台异步执行，
        # 这对于处理需要长时间运行的任务非常有用，因为它不会阻塞主程序的执行。
        # queue 參數，可以指定要發送到特定 queue 列隊中
        task.apply_async(queue=parameter.get("data_source", "")) 

    # db.close_conn()


if __name__ == "__main__":
    dataset, start_date, end_date = sys.argv[1:]
    Update(dataset, start_date, end_date)
