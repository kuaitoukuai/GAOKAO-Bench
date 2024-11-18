“二八理论”

只保留高考题中的单选题，强制只输出json格式，快速测评AI性能。

测评成绩汇总
![1731895079254](https://github.com/user-attachments/assets/7c2cd57e-59bd-4ffe-8abb-12d6e93aecf7)

测试与统计过程：
1、注册智谱清言，可以获得大量免费tokens，https://bigmodel.cn/finance/resourcepack
![image](https://github.com/user-attachments/assets/38744eeb-f238-4f06-a73b-73188d44e39d)

2、https://bigmodel.cn/usercenter/apikeys获取到APIKey，填到24行代码这里：self.client = ZhipuAI(api_key="xxxx.xxx") 
![image](https://github.com/user-attachments/assets/945cc757-f23c-43a6-b427-0be1cc2e191e)

3、提示词为：
"每小题给出的四个选项中，只有一个选项是最符合题目要求的。请你先认真仔细的读题和一步一步做题，心里面默默做题。告诉我你认为最符合题目要求的答案选项。不要写中间思考和计算过程，直接告诉我结果，告诉我答案就行，严格返回json格式告诉我。回答的答案用""""括号显示为文本格式{
  ""correct_answer"": ""A/B/C/D""
}"

可以自己修改
![image](https://github.com/user-attachments/assets/c332c05f-8977-40d9-9953-7f5404b4e844)

4、程序运行提取json中的答案，填到excel，使用excel函数=IF(E2=J2,1,0)快速比较是否与正确答案相同，1为正确，0为错误。

![image](https://github.com/user-attachments/assets/98a49b9a-f9e0-4096-a746-b87eefad1028)

5、数据透视表，统计每个科目的正确率。
![image](https://github.com/user-attachments/assets/01268c86-f8eb-4983-8dfe-2a6e9cc863db)
