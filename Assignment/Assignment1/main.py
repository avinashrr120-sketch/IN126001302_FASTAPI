from fastapi import FastAPI,Query
app = FastAPI()

# ── Temporary data — acting as our database for now ──────────

products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook','price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub','price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set','price':  49, 'category': 'Stationery',  'in_stock': True },
    {"id": 5, "name": "Laptop Stand", "price": 1200, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 3500, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 2500, "category": "Electronics", "in_stock": False}
]

# ── Endpoint 0 — Home ────────────────────────────────────────

@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}

# ── Endpoint 1 — Return all products ──────────────────────────

@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}
@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    
    filtered_products = [
        product for product in products
        if product["category"].lower() == category_name.lower()
    ]
    
    if not filtered_products:
        return {"error": "No products found in this category"}
    
    return {
        "category": category_name,
        "products": filtered_products,
        "total": len(filtered_products)
    }
@app.get("/products/instock")
def get_instock_products():
    
    available = [p for p in products if p["in_stock"] == True]
    
    return {
        "in_stock_products": available,
        "count": len(available)
    }

@app.get("/store/summary")
def store_summary():
    
    total_products = len(products)
    in_stock_count = len([p for p in products if p["in_stock"]])
    out_of_stock_count = total_products - in_stock_count
    
    categories = list(set([p["category"] for p in products]))
    
    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock_count,
        "out_of_stock": out_of_stock_count,
        "categories": categories
    }

@app.get("/products/search/{keyword}")
def search_products_by_name(keyword: str):
    search_term = keyword.lower()
    matched_products = [
        product for product in products 
        if search_term in product["name"].lower()
    ]
    if not matched_products:
        return {"message": "No products matched your search"}
    return {
        "matched_products": matched_products,
        "total_count": len(matched_products)
    }


@app.get("/products/deals")
def get_deals():
    cheapest = min(products, key=lambda p: p["price"])
    most_expensive = max(products, key=lambda p: p["price"])
    return {
        "best_deal": cheapest,
        "premium_pick": most_expensive
    }

# ── Endpoint 2 — Return one product by its ID ──────────────────

@app.get('/products/{product_id}')
def get_product(product_id: int):
    for product in products:
        if product['id'] == product_id:
            return {'product': product}
    return {'error': 'Product not found'}