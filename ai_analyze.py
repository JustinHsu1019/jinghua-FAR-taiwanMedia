import os
import json
import csv
import openai
import textwrap


def gpt_template(prompt):
    openai.api_key = "YOUR_API_KEY"

    userprompt = textwrap.dedent(
        f"""
        {prompt}
    """
    )

    response = openai.ChatCompletion.create(
        model='gpt-4o',
        messages=[
            {'role': 'system', 'content': '使用繁體中文回答'},
            {'role': 'user', 'content': userprompt},
        ],
    )

    return response.choices[0].message['content']


def call_llm(user_input):
    prompt = f"""
你是一個新聞分析助手，請根據以下的報導內容分析其政治傾向、證據公正性，以及情緒性。請使用以下 JSON 格式返回分析結果：

如果報導內容不偏向柯文哲、京華城案的，在 "政治偏向白與否" 的欄位就是 “不偏向”，
如果報導內容站在柯文哲、京華城案這邊的，在 "政治偏向白與否" 的欄位就是 “偏向”

JSON 格式範例：
{{
  "政治偏向白與否": "偏向 / 不偏向 / 中立",
  "證據公正性": "客觀 / 主觀",
  "情緒性": "低 / 中 / 高"
}}

請記得依照以上格式進行分析，並不要返回額外內容。

以下是報導內容：
{user_input}

輸出請直接以 {{ 為開頭，並以 }} 為結尾。不要輸出 ```json 或是 ```。
也不要返回任何額外的內容。
"""

    try:
        response = gpt_template(prompt)
        # 嘗試將回應轉為 JSON，確保格式正確
        json_data = json.loads(response)
        return json_data
    except json.JSONDecodeError:
        raise ValueError("GPT 返回的 JSON 格式有誤，程式終止！")
    except Exception as e:
        raise ValueError(f"發生錯誤：{e}")


def main():
    """分析資料夾內的新聞內容，輸出為 JSON 並存入 CSV"""
    input_dir = "data/20241226"
    output_csv = "output.csv"

    results = []

    # 遍歷資料夾內所有 .txt 檔案
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".txt"):
            file_path = os.path.join(input_dir, file_name)
            
            # 讀取檔案內容
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
            
            # 提取媒體名稱 (檔案名稱 "_" 前的部分)
            media_name = file_name.split("_")[0]

            try:
                # 呼叫 LLM 分析並取得 JSON 結果
                analysis_result = call_llm(file_content)
                print(analysis_result)
                print("==================================")

                # 如果結果符合 JSON 格式，加入結果
                results.append({
                    "ID": file_name,
                    "date": "2024/12/26",
                    "媒體": media_name,
                    "政治偏向白與否": analysis_result["政治偏向白與否"],
                    "證據公正性": analysis_result["證據公正性"],
                    "情緒性": analysis_result["情緒性"]
                })
            except ValueError as e:
                # 捕捉 JSON 格式錯誤並終止程式
                print(e)
                return

    # 將結果寫入 CSV
    with open(output_csv, 'w', encoding='utf-8', newline='') as csvfile:
        fieldnames = ["ID", "date", "媒體", "政治偏向白與否", "證據公正性", "情緒性"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(results)

    print(f"結果已成功輸出至 {output_csv}")


if __name__ == '__main__':
    main()
