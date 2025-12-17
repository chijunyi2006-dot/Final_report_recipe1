from fastapi import FastAPI, Query
from typing import List, Optional
import random
from database import load_recipes

app = FastAPI(
    title="食譜查詢 API",
    version="2.1.0",
    description="支援分類、複選食材、模糊搜尋的食譜 API"
)

# 載入食譜資料
recipes = load_recipes()


@app.get("/")
def root():
    return {"message": "歡迎使用強化版食譜查詢 API！"}


# =========================
# 搜尋功能（重點）
# =========================
@app.get(
    "/search",
    summary="依分類＋多食材（支援模糊）搜尋食譜",
    description=(
        "📌 **使用說明：**\n"
        "- 可同時選擇「分類」＋「多個食材」\n"
        "- 食材支援 **模糊搜尋**（例：輸入「飯」可找到「白飯」）\n\n"
        "📌 **甜點食材可選：**\n"
        "🍓 水果：草莓、香蕉、蘋果、芒果、酪梨、藍莓、地瓜、南瓜\n"
        "🥛 乳製品：鮮奶、豆漿、優格、乳酪\n"
        "🥚 蛋類：雞蛋、蛋黃\n"
        "🍯 甜味：蜂蜜、砂糖、黑糖、冰糖、楓糖漿\n"
        "🍫 烘焙：可可粉、巧克力豆、肉桂粉、泡打粉、吉利丁\n"
        "🥣 穀類：燕麥、紫米、糯米粉、低筋、中筋、餅乾\n"
        "🥑 豆類：豆腐、豆渣、紅豆\n\n"
        "📌 **家常菜食材可選：**\n"
        "🥬 蔬菜：蔥、蒜、洋蔥、青江菜、番茄\n"
        "🥩 肉類：雞肉、豬肉、牛肉、絞肉\n"
        "🐟 海鮮：蝦、魚肉、鮪魚罐頭\n"
        "🍳 基礎：雞蛋、醬油、鹽、糖、油\n"
        "🍚 主食：白飯、麵條、米粉\n"
    )
)
def search_recipes(
    category: Optional[str] = Query(
        None,
        description="分類：dessert（甜點） 或 home（家常菜）"
    ),
    ingredient: Optional[List[str]] = Query(
        None,
        description="可輸入多個食材，如：?ingredient=飯&ingredient=蛋"
    )
):
    result = recipes
    fuzzy_hit_count = 0  # 模糊搜尋命中次數

    # 1️⃣ 分類篩選
    if category:
        result = [r for r in result if r["category"] == category]

    # 2️⃣ 多食材 + 模糊搜尋
    if ingredient:
        filtered = []

        for recipe in result:
            matched_all = True
            local_hit = 0

            for q in ingredient:
                # 只要關鍵字出現在任一食材中就算命中
                if any(q in ing for ing in recipe["ingredients"]):
                    local_hit += 1
                else:
                    matched_all = False
                    break

            if matched_all:
                filtered.append(recipe)
                fuzzy_hit_count += local_hit

        result = filtered

    return {
        "category": category,
        "ingredients_query": ingredient,
        "fuzzy_match_count": fuzzy_hit_count,
        "count": len(result),
        "results": result
    }


# =========================
# 其他 API
# =========================
@app.get("/list", summary="列出全部食譜")
def list_recipes():
    return {"count": len(recipes), "recipes": recipes}


@app.get("/random", summary="隨機推薦一道食譜")
def random_recipe():
    return random.choice(recipes)


@app.get("/detail", summary="依完整名稱查詢食譜")
def recipe_detail(
    name: str = Query(..., description="請輸入完整食譜名稱")
):
    for r in recipes:
        if r["name"] == name:
            return r
    return {"error": f"找不到名為 {name} 的食譜"}