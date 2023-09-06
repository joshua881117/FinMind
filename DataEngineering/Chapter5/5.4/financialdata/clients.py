# 管理所有對資料庫的連線
from sqlalchemy import (
    create_engine,
    engine,
)


def get_mysql_financialdata_conn() -> engine.base.Connection:
    """
    user: root
    password: test
    host: localhost
    port: 3306
    database: financialdata
    如果有實體 IP，以上設定可以自行更改
    """
    # 初始化資料庫連接，使用pymysql模組。(若是要用其他的只要更換pymysql即可)
    # create_engine("mysql+module://username:password@ip:port/dbname")
    address = "mysql+pymysql://root:test@localhost:3306/financial_data"
    engine = create_engine(address)
    # 連線
    connect = engine.connect()
    return connect
