import time
import typing

from loguru import logger
from sqlalchemy import engine, text
from financialdata.backend.db import clients


def check_alive(connect: engine.base.Connection):
    sql_query = text('SELECT 1+1')
    connect.execute(sql_query)


def check_connect_alive(
    connect: engine.base.Connection,
    connect_func: typing.Callable,
    connect_count: int
):
    if connect:
        try:
            check_alive(connect)
            if connect_count > 0:
                logger.info("success reconnect")
            return connect
        except Exception as e:
            logger.info(
                f"""
                {connect_func.__name__} reconnect, error: {e}
                """
            )
            time.sleep(1)
            try:
                connect = connect_func()
            except Exception as e:
                logger.info(
                    f"""
                    {connect_func.__name__} connect error, error: {e}
                    """
                )
            connect_count += 1
        
            if connect_count < 5:
                return check_connect_alive(connect, connect_func, connect_count)
            else:
                logger.info("reconnect too many times")


class Router:
    def __init__(self):
        self._mysql_financialdata_conn = clients.get_mysql_financialdata_conn()

    def check_mysql_financialdata_conn_alive(self):
        self._mysql_financialdata_conn = check_connect_alive(
            self._mysql_financialdata_conn,
            clients.get_mysql_financialdata_conn,
            0,
        )
        return self._mysql_financialdata_conn

    # 定義物件的屬性，可以透過 .mysql_financialdata_conn 來取得值
    @property
    def mysql_financialdata_conn(self):
        return self.check_mysql_financialdata_conn_alive()

    def close_connection(self):
        self._mysql_financialdata_conn.close()
