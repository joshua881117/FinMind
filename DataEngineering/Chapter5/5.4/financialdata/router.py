# 管理資料庫的 connect, upload, alive
import time
import typing

from loguru import logger # 日誌顯示套件
from sqlalchemy import engine, text

from financialdata import clients


def check_alive(
    connect: engine.base.Connection,
):
    """在每次使用之前，先確認 connect 是否活者"""
    connect.execute(text("SELECT 1 + 1"))


def reconnect(
    connect_func: typing.Callable, # 連線的函式
) -> engine.base.Connection:
    """如果連線斷掉，重新連線"""
    try:
        connect = connect_func()
    except Exception as e:
        logger.info(
            f"{connect_func.__name__} reconnect error {e}"
        )
    return connect

def check_connect_alive(
    connect: engine.base.Connection,
    connect_func: typing.Callable,
):
    """確認連線是否存在(連線失敗後會持續嘗試)"""
    if connect:
        try:
            check_alive(connect)
            return connect
        except Exception as e:
            logger.info(
                f"{connect_func.__name__} connect, error: {e}"
            )
            time.sleep(1)
            connect = reconnect(
                connect_func
            )
            return check_connect_alive(
                connect, connect_func
            ) # 再次確認是否連線成功
    else:
        connect = reconnect(
            connect_func
        )
        return check_connect_alive(
            connect, connect_func
        )


class Router:
    def __init__(self):
        self._mysql_financialdata_conn = (
            clients.get_mysql_financialdata_conn()
        )

    def check_mysql_financialdata_conn_alive(
        self,
    ):
        self._mysql_financialdata_conn = check_connect_alive(
            self._mysql_financialdata_conn,
            clients.get_mysql_financialdata_conn,
        )
        return (
            self._mysql_financialdata_conn
        )

    @property
    def mysql_financialdata_conn(self):
        """
        使用 property，在每次拿取 connect 時，
        都先經過 check alive 檢查 connect 是否活著
        """
        return (
            self.check_mysql_financialdata_conn_alive()
        )
