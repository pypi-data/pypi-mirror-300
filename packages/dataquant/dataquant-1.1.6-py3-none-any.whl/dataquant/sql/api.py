# -*- coding: UTF-8 -*-
import warnings

import pandas as pd

from dataquant.apis.base import get_data


__all__ = [
    "get_sql_data"
]


def get_sql_data(qry_db, qry_sql, page_no=-1, page_size=-1):
    """
    获取SQL查询数据

    """

    if qry_db is None or qry_sql is None:
        warnings.warn("函数[get_sql_data]的参数(qry_db, qry_sql)为必填项")
        return None

    try:
        if page_no == -1:
            page_no = 0
        if page_size == -1:
            page_size = 100000

        params = {
            "query_db": qry_db,
            "query_sql": qry_sql,
            "page_no": page_no,
            "page_size": page_size,
            "api_type": "sql",
        }

        _url = "sql/get_sql_data" + "/" + qry_db
        result = get_data(_url, **params)
        if result.empty:
            return result

        total_cnt = result['query_total'][0]
        while total_cnt > result.shape[0]:
            params['page_no'] += 1
            page_result = get_data(_url, **params)
            result = pd.concat([result, page_result], axis=0)

        result.reset_index(drop=True, inplace=True)
        result.drop(['query_total'], axis=1, inplace=True)
        columns = result.columns.tolist()
        new_columns = [x.lower() for x in columns]
        result.columns = new_columns

        return result
    except Exception as ex:
        import traceback
        print(traceback.print_exc())
        return None


