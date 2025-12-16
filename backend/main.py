from fastapi import FastAPI, Query
from typing import List, Optional
import random
from database import load_recipes

app = FastAPI(title="食譜查詢 API", version="2.0.0")

recipes = load_recipes()

@app.get("/")
def root():
    return {"message": "歡迎使用強化版食譜查詢 API！"}

# 多條件搜尋：分類 + 多食材
@app.get("/search")
def search_recipes(
    category: Optional[str] = Query(None, description="分類：dessert（甜點）或 home（家常菜）"),
    ingredient: Optional[List[str]] = Query(
        None,
        description="輸入多個食材，例如：?ingredient=香蕉&ingredient=牛奶"
    )
):
    result = recipes

    # 篩選分類
    if category:
        result = [r for r in result if r["category"] == category]

    # 多食材搜尋（需要全部符合）
    if ingredient:
        result = [r for r in result if all(i in r["ingredients"] for i in ingredient)]

    return {
        "category": category,
        "ingredients_query": ingredient,
        "count": len(result),
        "results": result
    }

@app.get("/list")
def list_recipes():
    return {"count": len(recipes), "recipes": recipes}

@app.get("/random")
def random_recipe():
    return random.choice(recipes)

@app.get("/detail")
def recipe_detail(name: str = Query(..., description="食譜名稱")):
    for r in recipes:
        if r["name"] == name:
            return r
    return {"error": f"找不到名為 {name} 的食譜"}

