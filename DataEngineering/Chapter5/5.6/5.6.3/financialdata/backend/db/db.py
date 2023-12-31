import typing

import pandas as pd
import pymysql
from loguru import logger
from sqlalchemy import engine, text


def update2mysql_by_pandas(
    df: pd.DataFrame,
    table: str,
    mysql_conn: engine.base.Connection,
):
    if len(df) > 0:
        try:
            df.to_sql(
                name=table,
                con=mysql_conn,
                if_exists="append",
                index=False,
                chunksize=1000,
            )
            mysql_conn.commit()
        except Exception as e:
            logger.info(e)
            return False
    return True


def build_update_sql(
    colname: typing.List[str],
    value: typing.List[str],
):
    update_sql = ",".join(
        [
            ' `{}` = "{}" '.format(
                colname[i],
                str(value[i]),
            )
            for i in range(len(colname))
            if str(value[i])
        ]
    )
    return update_sql


def build_df_update_sql(
    table: str, df: pd.DataFrame
) -> typing.List[str]:
    logger.info("build_df_update_sql")
    df_columns = list(df.columns)
    sql_list = []
    for i in range(len(df)):
        temp = list(df.iloc[i])
        value = [
            pymysql.converters.escape_string(
                str(v)
            )
            for v in temp
        ]
        sub_df_columns = [
            df_columns[j]
            for j in range(len(temp))
        ]
        update_sql = build_update_sql(
            sub_df_columns, value
        )
        # SQL 上傳資料方式
        # DUPLICATE KEY UPDATE 意思是
        # 如果有重複，就改用 update 的方式
        # 避免重複上傳
        sql = """INSERT INTO `{}`({})VALUES ({}) ON DUPLICATE KEY UPDATE {}
            """.format(
            table,
            "`{}`".format(
                "`,`".join(
                    sub_df_columns
                )
            ),
            '"{}"'.format(
                '","'.join(value)
            ),
            update_sql,
        )
        sql_list.append(sql)
    return sql_list


def update2mysql_by_sql(
    df: pd.DataFrame,
    table: str,
    mysql_conn: engine.base.Connection,
):
    sql = build_df_update_sql(table, df)
    commit(
        sql=sql, mysql_conn=mysql_conn
    )


def commit(
    sql: typing.Union[
        str, typing.List[str]
    ],
    mysql_conn: engine.base.Connection = None,
):
    logger.info("commit")
    try:
        if isinstance(sql, list):
            for s in sql:
                try:
                    sql_query = text(s)
                    mysql_conn.execution_options(
                        autocommit=False
                    ).execute(sql_query)
                    mysql_conn.commit()
                except Exception as e:
                    logger.info(e)
                    logger.info(s)
                    break

        elif isinstance(sql, str):
            sql_query = text(sql)
            mysql_conn.execution_options(
                autocommit=False
            ).execute(sql_query)
            mysql_conn.commit()
    except Exception as e:
        mysql_conn.rollback()
        logger.info(e)


def upload_data(
    df: pd.DataFrame,
    table: str,
    mysql_conn: engine.base.Connection,
):
    if len(df) > 0:
        # 直接上傳
        if update2mysql_by_pandas(
            df=df,
            table=table,
            mysql_conn=mysql_conn,
        ):
            logger.info("Success upload {} data by pandas".format(len(df)))
            pass
        else:
            # 如果有重複的資料
            # 使用 SQL 語法上傳資料
            update2mysql_by_sql(
                df=df,
                table=table,
                mysql_conn=mysql_conn,
            )
            logger.info("Success upload {} data by SQL".format(len(df)))
