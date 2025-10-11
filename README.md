# 🧵 ThreadOra – E-commerce Platform

### __ThreadOra is an full-featured E-commerce Web Application, Where user can easily browse product, add in cart, place order, And can review products।__
---
### ✨ Features

- ##### 👤 _User Management (signup, login, profile, multiple addresses)_

- ##### 🛍️ _Product Catalog (categories, stock, sizes, discount, product images)_

- ##### 🛒 _Cart System (add/remove products, update quantity)_

- ##### 📦 _Order Management (place orders, order items, track status, payment status)_

- ##### ⭐ _Reviews & Ratings (1–5 star ratings, user comments)_

- ##### 🎟️ _Coupons & Discounts (optional feature)_

- ##### 🔒 _Authentication & Authorization (only logged-in users can order/review)_

- ##### 📝 _REST API (Django REST Framework with Swagger API Docs)_
---
### 🗂️ Database Models
1. #### **User**

- ##### id, name, email, password, phone, created_at

2. #### **Address**

- ##### Linked to User (One-to-Many)

- ##### Fields: full_name, phone, street_address, city, state, country, postal_code

3. #### **Category**

- ##### Product classification (e.g., T-shirt, Jeans, Saree)

4. #### **Product**

- ##### Fields: name, slug, description, price, discount_price, stock_quantity, brand, size, created_at, updated_at

- ##### Linked to Category

5. #### **Cart**

- ##### Linked to User & Product

6. #### **Order**

- ##### Linked to User & Address

- ##### Fields: total_price, status (pending/processing/shipped/delivered/cancelled), payment_status (unpaid/paid/refunded)

7. ### **OrderItem**

- ##### Linked to Order & Product

8. #### **Review**

- ##### Linked to User & Product

- ##### Fields: rating, comment, created_at

9. #### **Coupon** (optional)
- ##### Fields: code, discount_type, discount_value, min_purchase_amount, expiry_date, is_active

10. #### ProductImage

- ##### Multiple images per product

---

### __🔗 Relationships__

- ##### User → Address = One-to-Many

- ##### Category → Product = One-to-Many

- ##### User → Cart = One-to-Many

- ##### Order → OrderItems → Product = One-to-Many

- ##### User ↔ Review ↔ Product = Many-to-Many (via Review)

---
### __⚙️ Tech Stack__

- ##### Backend: Django REST Framework

- ##### Database: SQLite / PostgreSQL (configurable)

- ##### API Docs: drf-yasg (Swagger & ReDoc)

- ##### Authentication: Django Auth System (JWT/Session)

---
### __🚀 Installation & Setup__

1. _Clone the repo_

```
git clone https://github.com/asifraihan821/ThreadOra-Fashion-Web-Store
```

2. _activate virtual environment_

```
python -m venv .thread_env 
.thread_env\Scripts\activate
```

3. _Install dependencies_

```
pip install -r requirements.txt
```

4. _Run migrations :_

```
python manage.py migrate
```

5. _Create Superuser(admin) :_

```
python manage.py createsuperuser
```

6. _run server :_

```
python manage.py runserver
```
---

### __📖 API Documentation__
- Swagger UI : http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/
---
### __👨‍💻 Author__

- ####  ___Asibur Rahaman Asif___
- Email: asifraihan821@gmail.com
- Github : asifraihan821