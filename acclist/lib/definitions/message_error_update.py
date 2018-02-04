# -*- coding: utf-8 -*-

UPDATE_RESPONSE = {
    # parameter errors
    'param_servicename':
        {'code': 10, 'message': "新規サービス名が未入力です。"},
    'param_servicename_validate':
        {'code': 11, 'message': "登録できない新規サービス名です。"},
    # database errors
    'db_service_save':
        {'code': 101, 'message': "failed to save Service record."},
}

