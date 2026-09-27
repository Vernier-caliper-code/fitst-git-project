""""
学会封装成类：需要管理状态的，然后需要不断的复用

"""

import os
from typing import Dict, List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class HelloAgentsLLM:
    """"
    
    为本书“hello,Agents"定制LLM客户端。
    它用于调用任何兼容OpenAI接口的服务，并默认使用流式响应

    """

    def __init__(self,model:str,apiKey,baseUrl,timeout:int):
        """"
        初始化客户端，优先使用传入参数，如果未提供，则从环境变量加载

        """
        self.model=model or os.getenv("OPENAI_MODEL")
        apiKey=apiKey or os.getenv("OPENAI_API_KEY")
        baseUrl=baseUrl or os.getenv("OPENAI_BASE_URL")

        if not all([self.model,apiKey,baseUrl]):
            raise ValueError("请检查环境变量是否正确设置")

        self.client=OpenAI(api_key=apiKey,base_url=baseUrl,timeout=timeout)

    def think(self,message,temperature):
        """
        调用OpenAI API，并返回结果

        """

        print(f"正在使用模型{self.model}进行思考...")
        try:
            response=self.client.chat.completions.create(
                model=self.model,
                messages=message,
                temperature=temperature,
            
            )
            print("大语言模型响应成功：")
            collected_content=[]
            for chunk in response:
                if not chunk.choices:
                    continue
                content=chunk.choices[0].delta.content or ""
                print(content,end="",flush=True)
                collected_content.append(content)

            print()
            return "".join(collected_content)

        except Exception as e:
            print(f"大语言模型响应失败：{e}")
            return None

if __name__=="__main__":
    try:
        llmclient=HelloAgentsLLM()

        exampleMessage=[
            {"role":"system","content":"你是一个助手"},
            {"role":"user","content":"请写一个关于机器学习的例子"},

        ]

        print("___调用LLM____")
        responseText=llmclient.think(exampleMessage)
        if resopnseText:
            print(f"LLM响应：{responseText}")
            print(responseText)
    except ValueError as e:
        print(e)


