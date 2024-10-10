# openapi-sdk-python

#### 介绍
大淘客开放平台SDK PYTHON版

#### 安装教程

1.  依赖包安装
    pip install  requests
2.  安装
    
    1)下载安装包
    
    git clone https://gitee.com/dtk-developer/openapi-sdk-python.git
    或者下载压缩包
    
    2)安装
	python setup.py install


#### 使用说明
**** 
`热搜记录`

from dtkApi.search import Top100Req

appKey = 'xxx'

appSecret = 'xxx'

version = 'v1.0.1'  # 当前版本号

gr=Top100Req(appKey,appSecret,version)

gr.setParams("type",1)

gr.setParams("keyWords","男装")

data=gr.getResponse()

print(data)

****
`商品列表`

from dtkApi.save import GoodsListReq

appKey = 'xxx'

appSecret = 'xxx'

version = 'v1.2.4'  # 当前版本号

gr=GoodsListReq(appKey,appSecret,version)

gr.setParams("pageId",1)

data=gr.getResponse()

print(data)

****
`各大榜单`

from dtkApi.original import RankingListReq

appKey = 'xxx'

appSecret = 'xxx'

version = 'v1.3.0'  # 当前版本号

gr=RankingListReq(appKey,appSecret,version)

gr.setParams("rankType",1)

data=gr.getResponse()

print(data)

****
`高效转链`

from dtkApi.basic import PrivilegeLinkReq

appKey = 'xxx'

appSecret = 'xxx'

version = 'v1.3.1'  # 当前版本号

gr=PrivilegeLinkReq(appKey,appSecret,version)

gr.setParams("goodsId","2222112")

data=gr.getResponse()

print(data)
