import base64

import requests

from common.log import logger
from common import const, utils, memory
from config import conf

# OPENAI提供的图像识别接口
class OpenAIVision(object):
    def do_vision_completion_if_need(self, session_id: str, query: str):
        img_cache = memory.USER_IMAGE_CACHE.get(session_id)
        if img_cache and conf().get("image_recognition"):
            response, err = self.vision_completion(query, img_cache)
            if err:
                return {"completion_tokens": 0, "content": f"识别图片异常, {err}"}
            memory.USER_IMAGE_CACHE[session_id] = None
            return {
                "total_tokens": response["usage"]["total_tokens"],
                "completion_tokens": response["usage"]["completion_tokens"],
                "content": response['choices'][0]["message"]["content"],
            }
        return None

    def vision_completion(self, query: str, img_cache: dict):
        msg = img_cache.get("msg")
        path = img_cache.get("path")
        msg.prepare()
        logger.info(f"[CHATGPT] query with images, path={path}")
        payload = {
            "model": const.GPT4_VISION_PREVIEW,
            "messages": self.build_vision_msg(query, path),
            "temperature": conf().get("temperature"),
            "top_p": conf().get("top_p", 1),
            "frequency_penalty": conf().get("frequency_penalty", 0.0),  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            "presence_penalty": conf().get("presence_penalty", 0.0),  # [-2,2]之间，该值越大则更倾向于产生不同的内容
        }
        headers = {"Authorization": "Bearer " + conf().get("open_ai_api_key", "")}
        # do http request
        base_url = conf().get("open_ai_api_base", "https://api.openai.com/v1")
        res = requests.post(url=base_url + "/chat/completions", json=payload, headers=headers,
                            timeout=conf().get("request_timeout", 180))
        if res.status_code == 200:
            return res.json(), None
        else:
            logger.error(f"[CHATGPT] vision completion, status_code={res.status_code}, response={res.text}")
            return None, res.text

    def build_vision_msg(self, query: str, path: str):
        suffix = utils.get_path_suffix(path)
        with open(path, "rb") as file:
            base64_str = base64.b64encode(file.read()).decode('utf-8')
        messages = [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/{suffix};base64,{base64_str}"
                    }
                }
            ]
        }]
        return messages

    def vision_recognition(self, image_url, prompt="请分析图片"):
        messages = [
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]}
        ]
        args = {
            "model": conf().get("model") or const.GPT4_VISION_PREVIEW,
            "messages": messages,
            "temperature": conf().get("temperature", 0.9),
            "top_p": conf().get("top_p", 1),
            "frequency_penalty": conf().get("frequency_penalty", 0.0),
            "presence_penalty": conf().get("presence_penalty", 0.0),
        }
        api_key = conf().get("open_ai_api_key")
        try:
            import openai
            response = openai.ChatCompletion.create(api_key=api_key, **args)
            content = response.choices[0]["message"]["content"]
            return Reply(ReplyType.TEXT, content)
        except Exception as e:
            logger.error(f"[OPENAI] vision_recognition error: {e}")
            return Reply(ReplyType.ERROR, "图片分析失败")
