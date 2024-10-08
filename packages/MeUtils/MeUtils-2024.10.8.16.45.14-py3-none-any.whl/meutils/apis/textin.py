#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : textin
# @Time         : 2024/6/26 08:22
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : todo: 重构 https://tools.textin.com/
# https://www.textin.com/console/recognition/robot_enhance?service=watermark-remove

from meutils.pipe import *
from meutils.io.files_utils import to_url

from meutils.apis.proxy import ips

BASE_URL = "https://api.textin.com/home"


@alru_cache(ttl=3600 * 24)
async def document_process(data: bytes, service: str = "pdf_to_markdown", response_format: str = "url", **kwargs):
    """

    :param data:
    :param service: pdf_to_markdown watermark-remove dewarp
    :param response_format:
    :param kwargs:
    :return:
    """
    params = {
        "service": service,
        **kwargs

        # "page_count": page_count,
        # "get_image": "objects"
        # "apply_document_tree": 0,
    }
    try:
        async with httpx.AsyncClient(base_url=BASE_URL, timeout=120, follow_redirects=True) as client:
            response = await client.post('/user_trial_ocr', content=data, params=params)
            response.raise_for_status()

            logger.debug(response.status_code)
            logger.info(response.json())  # {'msg': '今日请求超过限制次数', 'code': 431}

            if response.is_success:
                _ = response.json()
                if '今日请求超过限制次数' in str(_):
                    raise Exception("加代理")

    except Exception as e:  # 加代理
        logger.error(e)

        proxies = await ips.get_proxies()
        response = requests.post(f"{BASE_URL}/user_trial_ocr", data=data, params=params, proxies=proxies)

        _ = response.json()

    if response_format == "url" and service in {"watermark-remove", "dewarp"}:
        _['data']['result']['image'] = await to_url(_['data']['result']['image'])

    return _


if __name__ == '__main__':
    # data = open("/Users/betterme/PycharmProjects/AI/11.jpg", 'rb').read()
    # # data = open("/Users/betterme/PycharmProjects/AI/蚂蚁集团招股书.pdf", 'rb').read()
    # with timer("解析"):
    #     # arun(textin_fileparser(data))
    #     print(arun(textin_fileparser(data, service="pdf_to_markdown")))

    # response = requests.request("POST", url, data=data)
    data = open("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/io/x.png", 'rb').read()

    from meutils.schemas.task_types import Purpose

    service = Purpose.watermark_remove.value
    # service = "pdf_to_markdown"

    with timer("解析"):
        # arun(textin_fileparser(data))
        data = arun(document_process(data, service=service))

        b64 = data['data']['result']['image']

        # base64_to_file(b64, "demo.png")

        # data['data']['result']['image'] = arun(to_url(b64))

        logger.debug(data)

        # {'msg': 'success',
        #  'data': {
        #      'result': {
        #          'image': 'https://sfile.chatglm.cn/chatglm-videoserver/image/e5/e5d4011c.png'
        #      },
        #      'file_type': '', 'file_data': ''
        #  }, 'code': 200
        #  }
