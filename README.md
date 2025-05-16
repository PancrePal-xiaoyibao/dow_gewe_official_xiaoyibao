这是基于Dify-on-wechat的一个优化版本，由小x宝社区开源提供

感谢DOW作者，以及GEWE官方社区对于小X宝公益社区的支持和捐助。如需了解和购买GEWE服务，可以访问[gewe官网](https://geweapi.com/#/newHome),专业服务值得拥有。

## 主要功能更新：
1. 适配了gewechat官方token和相应的api规范。
2. 适配了fastgpt智能体，接入后实现对话/图像分析/插件功能
3. 场景主要满足小x宝社区服务肿瘤患者/罕见病患则的需求

## 主要修改文件：
/channel/chat_channel.py
/channel/gewechat
/lib/gewechat/api/login.py #适配gewe官方api接口，原来的不对。

```bash
    tools/setCallback改为

    return post_json(self.base_url, "/login/setCallback", self.token, param)

```

/bot/chatgpt/chat_gpt_bot.py #修改增加s3图片处理逻辑，位置 “        
```bash
elif context.type == ContextType.IMAGE:
```

## 配置说明：
1. config.json按照要求配置，尤其是s3的部分，可以参考sealos存储桶参数填写。其它的自己需要测试适配。
2. docker-compose.yml文件参考如下配置

```yaml
version: '3.8'

services:
  xiaofenbao:
    container_name: xiaofenbao
    image: dow-gewe-official-xyb:v2
    restart: unless-stopped
    ports:
      - "19923:9919"
    security_opt:
      - seccomp:unconfined
    environment:
      TZ: 'Asia/Shanghai'
    volumes:
      - ./config.json:/app/config.json
      - ./tmp:/app/tmp
      # - /srv/plugins:/app/plugins
      # - /srv/gewechat_message.py:/app/channel/gewechat/gewechat_message.py
      # - /srv/lib/gewechat:/app/lib/gewechat

```

4. docker-compose up -d 启动就可以

# docker私有化镜像
```bash

docker login ccr.ccs.tencentyun.com --username=100015489703

密码咨询小x宝社区，授权使用。

docker pull ccr.ccs.tencentyun.com/xiaoyibao/dow-gewe-official-xyb:v3


```

# 数据隐私
技术目的存储的图片等数据含有隐私信息，需要定期处理删除。后续需要增强自动化清理。

#后续开发
[]临床试验插件
[]药物查询插件: 输入药物关键词，通过用药助手卡片打开
[]---