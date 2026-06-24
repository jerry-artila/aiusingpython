# ============================================
# DeepSeek API 連線測試工具
# ============================================

import os
from dotenv import load_dotenv
from openai import OpenAI

# ----- 環境初始化 -----

# 載入 .env 檔案中的環境變數（如 DEEPSEEK_API_KEY）
load_dotenv()

# 從環境變數取得 DeepSeek API Key
api_key = os.environ.get("DEEPSEEK_API_KEY")

# 若未取得 API Key，則提示使用者並結束程式
if not api_key:
    print("❌ 錯誤：找不到 DEEPSEEK_API_KEY")
    print("")
    print("請確認 .env 檔案中存在 DEEPSEEK_API_KEY 設定，例如：")
    print("  DEEPSEEK_API_KEY=sk-your-api-key")
    print("")
    print("💡 可在 https://platform.deepseek.com/api_keys 取得 API Key")
    exit(1)

# 遮罩顯示 API Key 以便除錯時確認（僅顯示前8碼與末4碼）
print("🔑 API Key 已找到 (前綴: {}...{})".format(api_key[:8], api_key[-4:]))

# ----- 建立 OpenAI 相容客戶端 -----

# 使用 OpenAI SDK 連接 DeepSeek API（兩者 API 格式相容）
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"  # DeepSeek API 端點
)

# ============================================
# 測試 1：列出可用模型
# ============================================
print("\n📡 測試 1：列出可用模型...")
try:
    # 呼叫 DeepSeek 的模型列表 API
    models = client.models.list()
    print(f"✅ 成功！共 {len(models.data)} 個模型可用：")
    # 逐一印出每個模型的名稱
    for m in models.data:
        print(f"   - {m.id}")
except Exception as e:
    # 若 API 呼叫失敗，印出錯誤訊息
    print(f"❌ 列出模型失敗：{e}")

# ============================================
# 測試 2：發送聊天請求
# ============================================
print("\n📡 測試 2：發送聊天請求...")
try:
    # 向 DeepSeek 發送一則對話請求
    response = client.chat.completions.create(
        model="deepseek-chat",          # 使用的模型名稱
        messages=[
            # 系統角色：設定 AI 助手的基本人格
            {"role": "system", "content": "You are a helpful assistant."},
            # 使用者角色：輸入實際的提問
            {"role": "user", "content": "請用一句話介紹 DeepSeek"}
        ],
        temperature=0.7,    # 生成隨機性（0~2，越高越有創意）
        max_tokens=100       # 回覆最大 token 數
    )
    print("✅ 連線成功！")
    # 從回覆中取出 AI 生成的文字內容
    print(f"💬 回覆內容：{response.choices[0].message.content}")
    # 顯示本次請求消耗的 token 總數
    print(f"📊 Token 用量：{response.usage.total_tokens}")
except Exception as e:
    # 若 API 呼叫失敗，印出錯誤訊息
    print(f"❌ 聊天請求失敗：{e}")
