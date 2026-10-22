# BAZAR

BAZAR is a hyperlocal marketplace platform where customers can discover nearby shops and browse their product catalogs.

Shopkeepers can create a digital storefront and list their products, allowing local customers to explore items available in their city or pincode.

---

## Features

- **Shop Discovery** — Find shops by city, pincode, or category
- **Seller Dashboard** — Manage products, view orders, update order status, bulk CSV import
- **Product Catalog** — Categories, search, stock tracking, image galleries
- **Cart & Checkout** — Session-based cart, multi-shop order splitting, shop pickup and WhatsApp confirmation
- **Reviews & Ratings** — Customers rate shops and products
- **Platform Admin** — Custom admin panel at `/platform-admin/` for moderation, analytics, featured shops
- **PDF Catalog** — Sellers generate downloadable product catalogs
- **WhatsApp Integration** — Share shop links on WhatsApp
- **HTMX Live Search** — Instant search results without full page reload

---

## Tech Stack

| Layer       | Technology                            |
|-------------|---------------------------------------|
| Backend     | Django 5, Python 3.11+                |
| Database    | SQLite                                |
| Frontend    | TailwindCSS (CDN), HTMX, Crispy Forms|
| Static      | WhiteNoise                            |
| Server      | Gunicorn                              |
| PDF         | WeasyPrint                            |
| Images      | Cloudinary, Pillow, django-imagekit   |

---

## Project Structure

```
localbazaarhub/
├── apps/
│   ├── accounts/        # Custom user model, auth, registration
│   ├── analytics/       # Shop analytics tracking
│   ├── cart/            # Cart, checkout, orders
│   ├── core/            # Homepage, city select, search
│   ├── platform_admin/  # Custom admin dashboard
│   ├── products/        # Product catalog, categories
│   ├── reviews/         # Shop & product reviews
│   └── shops/           # Shop CRUD, seller dashboard
├── localbazaarhub/
│   ├── settings/
│   │   ├── base.py          # Shared settings
│   │   ├── development.py   # DEBUG=True, SQLite
│   │   └── production.py    # DEBUG=False, SQLite, security
│   ├── urls.py
│   └── wsgi.py
├── templates/           # All HTML templates
├── static/              # CSS, JS, images
├── manage.py
├── requirements.txt
├── build.sh             # Deployment build script
├── start.sh             # Gunicorn start script
├── render.yaml          # Render deployment config
├── .env.example         # Environment variable template
└── .gitignore
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd localbazaarhub
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---

## Note

> Shop and product images are stored in Cloudinary when its credentials are configured. Orders are placed for shop pickup and paid at the shop; buyers contact the seller through WhatsApp after checkout.

---

## Deployment

### Render

1. Push your code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` and configures the web service
5. Add the `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET` environment variables on the Render dashboard.

The free Render service uses SQLite on ephemeral storage. Its database can reset when the service restarts, so seed categories are restored at startup. Do not rely on this setup for permanent customer or order data.

---

## Deployment Checklist

- [x] `.gitignore` created
- [x] `requirements.txt` created
- [x] `DEBUG` disabled in production
- [x] Static files configured
- [x] Gunicorn installed
- [x] Migrations ready
- [x] README documentation included

---

## License

This project is for educational and portfolio purposes.
# BAZAR

BAZAR is a hyperlocal marketplace platform where customers can discover nearby shops and browse their product catalogs.

Shopkeepers can create a digital storefront and list their products, allowing local customers to explore items available in their city or pincode.

---

## Features

- **Shop Discovery** — Find shops by city, pincode, or category
- **Seller Dashboard** — Manage products, view orders, update order status, bulk CSV import
- **Product Catalog** — Categories, search, stock tracking, image galleries
- **Cart & Checkout** — Session-based cart, multi-shop order splitting, address capture
- **Reviews & Ratings** — Customers rate shops and products
- **Platform Admin** — Custom admin panel at `/platform-admin/` for moderation, analytics, featured shops
- **PDF Catalog** — Sellers generate downloadable product catalogs
- **WhatsApp Integration** — Share shop links on WhatsApp
- **HTMX Live Search** — Instant search results without full page reload

---

## Tech Stack

| Layer       | Technology                            |
|-------------|---------------------------------------|
| Backend     | Django 5, Python 3.11+                |
| Database    | SQLite                                |
| Frontend    | TailwindCSS (CDN), HTMX, Crispy Forms|
| Static      | WhiteNoise                            |
| Server      | Gunicorn                              |
| PDF         | WeasyPrint                            |
| Images      | Cloudinary, Pillow, django-imagekit   |

---

## Project Structure

```
localbazaarhub/
├── apps/
│   ├── accounts/        # Custom user model, auth, registration
│   ├── analytics/       # Shop analytics tracking
│   ├── cart/            # Cart, checkout, orders
│   ├── core/            # Homepage, city select, search
│   ├── platform_admin/  # Custom admin dashboard
│   ├── products/        # Product catalog, categories
│   ├── reviews/         # Shop & product reviews
│   └── shops/           # Shop CRUD, seller dashboard
├── localbazaarhub/
│   ├── settings/
│   │   ├── base.py          # Shared settings
│   │   ├── development.py   # DEBUG=True, SQLite
│   │   └── production.py    # DEBUG=False, SQLite, security
│   ├── urls.py
│   └── wsgi.py
├── templates/           # All HTML templates
├── static/              # CSS, JS, images
├── manage.py
├── requirements.txt
├── build.sh             # Deployment build script
├── start.sh             # Gunicorn start script
├── render.yaml          # Render deployment config
├── .env.example         # Environment variable template
└── .gitignore
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd localbazaarhub
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---

## Note

> Shop and product images are stored in Cloudinary when its credentials are configured. Orders are placed for shop pickup and paid at the shop; buyers contact the seller through WhatsApp after checkout.

---

## Deployment

### Render

1. Push your code to GitHub
2. Create a new **Web Service** on [Render](https://render.com)
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` and configures the web service
5. Add the `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, and `CLOUDINARY_API_SECRET` environment variables on the Render dashboard.

The free Render service uses SQLite on ephemeral storage. Its database can reset when the service restarts, so seed categories are restored at startup. Do not rely on this setup for permanent customer or order data.

---

## Deployment Checklist

- [x] `.gitignore` created
- [x] `requirements.txt` created
- [x] `DEBUG` disabled in production
- [x] Static files configured
- [x] Gunicorn installed
- [x] Migrations ready
- [x] README documentation included

---

## License

This project is for educational and portfolio purposes.
