# -*- coding: utf-8 -*-
"""
集成程序1和程序2的自动化机器人

功能：
1. 读取Excel文件中的题目和提示词。
2. 将内容上传到指定网页的输入框。
3. 提交并获取AI生成的答案。
4. 将答案保存回Excel文件中。

作者: 您的名字
日期: 2024-09-25
"""

import pandas as pd
import json
from zhipuai import ZhipuAI
from concurrent.futures import ThreadPoolExecutor, as_completed

class 自动化机器人:
    def __init__(self, 文件路径='输入输出.xlsx'):
        self.文件路径 = 文件路径
        self.数据 = self.读取数据()
        self.client = ZhipuAI(api_key="xxxx.xxx")  # 使用您的真实APIKey,网址https://bigmodel.cn/usercenter/apikeys

    def 读取数据(self):
        try:
            数据 = pd.read_excel(self.文件路径)
            return 数据
        except FileNotFoundError:
            print(f"未找到文件: {self.文件路径}")
            return pd.DataFrame()
    
    def 保存数据(self):
        self.数据.to_excel(self.文件路径, index=False)
        print(f"数据已保存到 {self.文件路径}")
    
    def 提问AI并获取答案(self, 题目, 提示词):
        try:
            提问内容 = f"{题目}\n{提示词}"
            response = self.client.chat.completions.create(
                # model="glm-4-plus",
                model="glm-4-0520",
                
                messages=[{"role": "user", "content": 提问内容}],
                stream=False
            )

            最新回复 = response.choices[0].message.content
            print(f"获取到AI回复: {最新回复}")

            return self.解析JSON(最新回复)

        except Exception as e:
            print(f"发生错误: {e}")
            return "处理失败"

    def 解析JSON(self, AI回复):
        AI回复 = AI回复.strip()
        if AI回复.startswith('{') and AI回复.endswith('}'):
            try:
                json数据 = json.loads(AI回复)
                答案 = json数据.get("correct_answer", "")
                return 答案 if 答案 else "未找到答案字段"
            except json.JSONDecodeError:
                return "JSON解析失败"
        else:
            return AI回复
    
    def 处理单行(self, index, 行, 运行次数):
        题目 = str(行['题目'])
        提示词 = str(行['提示词'])
        print(f"处理第 {index + 1} 行...")

        AI答案 = self.提问AI并获取答案(题目, 提示词)
        print(f"第 {index + 1} 行的AI答案: {AI答案}")

        列名 = f"AI回答的答案-glm-4-0520-第{运行次数}遍"
        self.数据.at[index, 列名] = AI答案
    
    def 运行一次(self, 运行次数, 并发数量=18):
        if self.数据.empty:
            print("没有数据可处理。")
            return

        列名 = f"AI回答的答案-glm-4-0520-第{运行次数}遍"
        if 列名 not in self.数据.columns:
            self.数据[列名] = None

        with ThreadPoolExecutor(max_workers=并发数量) as executor:
            futures = {executor.submit(self.处理单行, index, 行, 运行次数): index for index, 行 in self.数据.iterrows() if pd.isna(行.get(列名))}
            for future in as_completed(futures):
                index = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"处理第 {index + 1} 行时发生错误: {e}")
        
        self.保存数据()
    
    def 运行(self, 总运行次数=1, 并发数量=18):
        for i in range(1, 总运行次数 + 1):
            print(f"开始第 {i} 次运行...")
            self.运行一次(运行次数=i, 并发数量=并发数量)
            print(f"第 {i} 次运行已完成。")
            print("-----------")

if __name__ == "__main__":
    机器人 = 自动化机器人(文件路径='汇总 - 高考单选题2024.11.13 - github.xlsx')
    机器人.运行(总运行次数=4, 并发数量=18)  # 可以调整总运行次数
