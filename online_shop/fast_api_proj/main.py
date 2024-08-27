from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Base, Product, User, Cart, CartItem
from database import SessionLocal, engine

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request and response
class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int

class ProductResponse(ProductCreate):
    id: int

class UserCreate(BaseModel):
    username: str
    password: str  # In a real app, hash this password

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

# API Endpoints
@app.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/", response_model=list[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, password=user.password)  # Hash password in a real app
    db.add(db_user)
    db.commit()
    return {"username": db_user.username}

@app.post("/cart/")
def create_cart(user_id: int, db: Session = Depends(get_db)):
    db_cart = Cart(user_id=user_id)
    db.add(db_cart)
    db.commit()
    return {"cart_id": db_cart.id}

@app.post("/cart/{cart_id}/items/")
def add_cart_item(cart_id: int, item: CartItemCreate, db: Session = Depends(get_db)):
    db_cart_item = CartItem(cart_id=cart_id, **item.dict())
    db.add(db_cart_item)
    db.commit()
    return {"item_id": db_cart_item.id}

@app.get("/cart/{cart_id}/items/")
def get_cart_items(cart_id: int, db: Session = Depends(get_db)):
    items = db.query(CartItem).filter(CartItem.cart_id == cart_id).all()
    return items



# API Endpoints
# Create a product
# :
# POST /products/
# List all products
# :
# GET /products/
# Create a user
# :
# POST /users/
# Create a cart
# :
# POST /cart/
# Add an item to the cart
# :
# POST /cart/{cart_id}/items/
# Get items in the cart
# :
# GET /cart/{cart_id}/items/