
#修改记录

1. config.json
2. config.py
3. channel目录下
    3.1 chat_channel.py 
    3.2 gewe目录下
    - gewechat_channel.py
    - gewechat_message.py先不动

4.chat_gpt_bot.py - bot/chat_gpt_bot.py

5.lib/gewechat/api/login_api.py （*适配regional_id在config.json中指定）
  client.py - lib/gewechat/client.py
6.bridge/reply.py修改，增加了APP = "app" #APP配合SearchMusic



-----
1. 微信机器人主流程相关
gewechat_channel.py - channel/gewechat/gewechat_channel.py
chat_channel.py - channel/chat_channel.py
gewechat_message.py - channel/gewechat/gewechat_message.py

2. FastGPT/OpenAI API对接
chat_gpt_bot.py - bot/chat_gpt_bot.py

3. S3上传与图片缓存
config.json - config.json
config.py - config.py
（如有 S3 工具类）s3_utils.py 或相关实现文件

4. gewechat二维码登录 regionId 支持
gewechat_channel.py - channel/gewechat/gewechat_channel.py
client.py - lib/gewechat/client.py
login_api.py - lib/gewechat/api/login_api.py

5. 其它配置与通用
config.json - config.json
config.py - config.py