#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
from google.cloud import storage
import os

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name, credentials_path):
    # 認証情報の指定
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    # GCS クライアントの作成
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # ファイルのアップロード
    blob.upload_from_filename(source_file_name)

    return True

def run_module():
    # モジュールの引数を定義
    module_args = dict(
        bucket_name=dict(type='str', required=True),
        source_file_name=dict(type='str', required=True),
        destination_blob_name=dict(type='str', required=True),
        credentials_path=dict(type='str', required=False, default=None)
    )

    # モジュールオブジェクトの作成
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # パラメータの取得
    bucket_name = module.params['bucket_name']
    source_file_name = module.params['source_file_name']
    destination_blob_name = module.params['destination_blob_name']
    credentials_path = module.params['credentials_path']

    # チェックモードの確認
    if module.check_mode:
        module.exit_json(changed=False)

    try:
        # GCS へのファイルアップロード
        result = upload_to_gcs(bucket_name, source_file_name, destination_blob_name, credentials_path)
        module.exit_json(changed=True, result=result)
    except Exception as e:
        module.fail_json(msg='Error uploading file to GCS: {}'.format(str(e)))

def main():
    run_module()

if __name__ == '__main__':
    main()
