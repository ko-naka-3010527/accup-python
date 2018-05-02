# -*- coding: utf-8 -*-

UPDATE_RESPONSE = {
    # ok message
    'ok':
        {'code': 0, 'message': "Acc-Up アカウント情報を更新しました。"},

    # general errors
    'unexpected_error':
        {'code': 1, 'message': "予期しないエラーが発生しました。"},
    'transaction_error':
        {'code': 2, 'message': "Acc-Up アカウント情報を正常に更新できませんでした。"},
    'update_parameter_error':
        {'code': 3, 'message': "Acc-Up アカウント情報を更新できませんでした。不正な更新情報が含まれています。"},
    'create_parameter_error':
        {'code': 4, 'message': "Acc-Up アカウントを作成できませんでした。不正な更新情報が含まれています。"},

    # update failure
    'param_password':
        {'code': 10, 'message': "新しいパスワードが未入力です。"},
    'param_password_conf':
        {'code': 11, 'message': "新しいパスワードをもう一度入力してください。"},
    'param_password_not_equal':
        {'code': 12, 'message': "パスワードが一致しません。"},
    'param_username_invalid':
        {'code': 13, 'message': "ユーザ名に使用できない文字が含まれています。"},
    'param_username_already_exists':
        {'code': 14, 'message': "指定されたユーザ名は既に使用されています。"},
    'param_current_password_is_none':
        {'code': 15, 'message': "現在のパスワードが入力されていません。"},
    'param_current_password_failure':
        {'code': 16, 'message': "パスワードが違います。"},

    # database errors
    'db_djgaccount_save':
        {'code': 101, 'message': "アカウントを登録できませんでした。"},
    'db_accaccount_save':
        {'code': 102, 'message': "アカウントを登録できませんでした。"},
}
