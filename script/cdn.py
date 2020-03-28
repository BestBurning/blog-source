# -*- coding: utf-8 -*-

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.cdn.v20180606 import cdn_client, models 
import argparse


def cnd_refresh(s_id,s_key):
    try: 
        cred = credential.Credential(s_id,s_key) 
        httpProfile = HttpProfile()
        httpProfile.endpoint = "cdn.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = cdn_client.CdnClient(cred, "ap-guangzhou", clientProfile) 

        req = models.PurgePathCacheRequest()
        params = '{"Paths":["https://di1shuai.com/"],"FlushType":"delete"}'
        req.from_json_string(params)

        resp = client.PurgePathCache(req) 
        print(resp.to_json_string()) 
        return True
    except TencentCloudSDKException as err: 
        print(err)
        return False 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--s_id', type=str, default = None)
    parser.add_argument('--s_key', type=str, default= None)
    args = parser.parse_args()
    cnd_refresh(args.s_id,args.s_key)