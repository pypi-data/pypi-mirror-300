import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)
from functools import lru_cache
from mns_common.db.MongodbUtil import MongodbUtil
import pandas as pd
import mns_common.utils.data_frame_util as data_frame_util
import mns_common.component.common_service_fun_api as common_service_fun_api
import mns_common.constant.db_name_constant as db_name_constant

mongodb_util = MongodbUtil('27017')


@lru_cache(maxsize=None)
def get_hk_company_info():
    query_field = {'symbol': 1,
                   'name': 1,
                   'industry': 1,
                   'hk_ggt': 1}
    return mongodb_util.find_query_data_choose_field(db_name_constant.COMPANY_INFO_HK,
                                                     {}, query_field)
