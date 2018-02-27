# -*- coding: utf-8 -*-

UPDATE_RESPONSE = {
    # ok message
    'ok':
        {'code': 0, 'message': "アカウント情報を更新しました。"},

    # general errors
    'unexpected_error':
        {'code': 1, 'message': "予期しないエラーが発生しました。"},
    'transaction_error':
        {'code': 2, 'message': "アカウント情報を正常に更新できませんでした。"},
    'update_parameter_error':
        {'code': 3, 'message': "アカウント情報を更新できませんでした。不正な更新情報が含まれています。"},

    # parameter errors
    'param_servicename':
        {'code': 10, 'message': "新規サービス名が未入力です。"},
    'param_servicename_validate':
        {'code': 11, 'message': "登録できない新規サービス名です。"},
    'param_password_not_equal':
        {'code': 12, 'message': "パスワードが一致しません。"},
    'param_mailaddr1':
        {'code': 13, 'message': "新規メールアドレス1が未入力です。"},
    'param_mailaddr1_validate':
        {'code': 14, 'message': "メールアドレス1に登録できない新規メールアドレスが指定されています。"},
    'param_mailaddr2':
        {'code': 15, 'message': "新規メールアドレス2が未入力です。"},
    'param_mailaddr2_validate':
        {'code': 16, 'message': "メールアドレス2に登録できない新規メールアドレスが指定されています。"},
    'param_mailaddr3':
        {'code': 17, 'message': "新規メールアドレス3が未入力です。"},
    'param_mailaddr3_validate':
        {'code': 18, 'message': "メールアドレス3に登録できない新規メールアドレスが指定されています。"},
    'param_mailaddr_duplicate':
        {'code': 19, 'message': "同じメールアドレスは登録できません。"},
    'param_address':
        {'code': 20, 'message': "新規住所が未入力です。"},
    'param_address_validate':
        {'code': 21, 'message': "登録できない住所です。"},
    'param_phonenum':
        {'code': 22, 'message': "新規電話番号が未入力です。"},
    'param_phonenum_validate':
        {'code': 23, 'message': "登録できない電話番号です。"},
    'param_account_validate':
        {'code': 50, 'message': "登録できないパラメタが含まれています。"},

    # database errors
    'db_service_save':
        {'code': 101, 'message': "新規サービス情報を登録できませんでした。"},
    'db_mail1_save':
        {'code': 102, 'message': "新規メールアドレス1を保存できませんでした。"},
    'db_mail2_save':
        {'code': 103, 'message': "新規メールアドレス2を保存できませんでした。"},
    'db_mail3_save':
        {'code': 104, 'message': "新規メールアドレス3を保存できませんでした。"},
    'db_address_save':
        {'code': 105, 'message': "新規住所情報を登録できませんでした。"},
    'db_phonenum_save':
        {'code': 106, 'message': "新規電話番号を登録できませんでした。"},
    'db_account_save':
        {'code': 120, 'message': "アカウントを登録できませんでした。"},

    # user mismatch
    'user_account_mismatch':
        {'code': 201, 'message': "指定されたアカウントは存在しません。"},
    'user_service_mismatch':
        {'code': 202, 'message': "指定されたサービス情報は存在しません。"},
    'user_mail1_mismatch':
        {'code': 203, 'message': "メールアドレス1で指定されたメールアドレスは存在しません。"},
    'user_mail2_mismatch':
        {'code': 204, 'message': "メールアドレス2で指定されたメールアドレスは存在しません。"},
    'user_mail3_mismatch':
        {'code': 205, 'message': "メールアドレス3で指定されたメールアドレスは存在しません。"},
    'user_address_mismatch':
        {'code': 206, 'message': "指定された住所情報は存在しません。"},
    'user_phonenum_mismatch':
        {'code': 207, 'message': "指定された電話番号情報は存在しません。"},
    'user_link1_mismatch':
        {'code': 208, 'message': "アカウント関連付け1で指定されたアカウント情報は存在しません。"},
    'user_link2_mismatch':
        {'code': 209, 'message': "アカウント関連付け2で指定されたアカウント情報は存在しません。"},
    'user_link3_mismatch':
        {'code': 210, 'message': "アカウント関連付け3で指定されたアカウント情報は存在しません。"},

}

