import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Category, Product, Blog, FAQ
import datetime
from app.models import User

app = create_app()

with app.app_context():
    print("🚀 Bắt đầu seed dữ liệu...")

    # Clear any pending transactions and refresh cache
    db.session.rollback()
    db.session.expire_all()

    # ==================== USERS ====================
    try:
        existing_admin = User.query.filter_by(email="admin@example.com").first()
        if not existing_admin:
            admin = User(
                username="admin",
                email="admin@example.com",
                password_hash=User.hash_password("admin123"),
                is_admin=True,
                created_at=datetime.datetime.utcnow()
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created")
        else:
            print("⚠️ Admin user đã tồn tại, bỏ qua tạo mới")
    except Exception as e:
        db.session.rollback()
        print(f"⚠️ Lỗi khi tạo admin user (có thể đã tồn tại): {e}")

    # ==================== CATEGORIES ====================
    categories_data = [
        {
            'name': f'Cát Sấy Số {i}',
            'slug': f'cat-say-so-{i}',
            'description': f'Cát sấy số {i} chất lượng cao, dùng trong công nghiệp và xây dựng'
        }
        for i in range(1, 6)
    ]

    for cat_data in categories_data:
        if not Category.query.filter_by(slug=cat_data['slug']).first():
            cat = Category(**cat_data, is_active=True)
            db.session.add(cat)
            print(f"✅ Category: {cat_data['name']}")

    db.session.commit()

    # ==================== PRODUCTS ====================
    sizes = [
        ("Loại 1 (0.15mm - 0.3mm)", "0-15-0-3mm", 180000),
        ("Loại 2 (0.3mm - 0.6mm)", "0-3-0-6mm", 185000),
        ("Loại 3 (0.6mm - 1.2mm)", "0-6-1-2mm", 190000),
    ]

    products_data = []
    for i in range(1, 6):  # 5 loại cát
        for idx, (name, slug_part, price) in enumerate(sizes, start=1):
            products_data.append({
                'name': f'Cát Sấy Số {i} - {name}',
                'slug': f'cat-say-so-{i}-loai-{idx}-{slug_part}',
                'description': f'Cát sấy số {i}, {name}, dùng cho công nghiệp và xây dựng',
                'price': price,
                'old_price': price + 20000,
                'category_id': i,
                'is_featured': (idx == 1)
            })

    for prod_data in products_data:
        if not Product.query.filter_by(slug=prod_data['slug']).first():
            prod = Product(**prod_data, is_active=True)
            db.session.add(prod)
            print(f"✅ Product: {prod_data['name']}")

    db.session.commit()

    # ==================== BLOGS ====================
    blogs_data = [
        {
            'title': 'Ứng dụng cát sấy trong công nghiệp',
            'slug': 'ung-dung-cat-say',
            'excerpt': 'Cát sấy được ứng dụng trong nhiều ngành nghề từ xây dựng, lọc nước đến sản xuất công nghiệp.',
            'content': '''<p>Cát sấy là vật liệu quan trọng...</p>''',
            'focus_keyword': 'cát sấy',
            'meta_title': 'Ứng dụng cát sấy trong công nghiệp | Cát Sấy',
            'meta_description': 'Tìm hiểu ứng dụng cát sấy trong công nghiệp và xây dựng.'
        },
        {
            'title': 'Bảng giá cát sấy mới nhất 2025',
            'slug': 'bang-gia-cat-say-2025',
            'excerpt': 'Cập nhật bảng giá cát sấy số 1 → số 5 mới nhất thị trường năm 2025.',
            'content': '''<p>Bảng giá cát sấy cập nhật mới nhất...</p>''',
            'focus_keyword': 'giá cát sấy',
            'meta_title': 'Bảng giá cát sấy 2025 | Giá tốt nhất',
            'meta_description': 'Cập nhật bảng giá cát sấy số 1 → số 5 mới nhất 2025.'
        }
    ]

    for blog_data in blogs_data:
        if not Blog.query.filter_by(slug=blog_data['slug']).first():
            blog = Blog(**blog_data, is_active=True)
            blog.calculate_reading_time()
            db.session.add(blog)
            print(f"✅ Blog: {blog_data['title']}")

    db.session.commit()

    # ==================== FAQs ====================
    faqs_data = [
        {'question': 'Cát sấy là gì?', 'answer': 'Cát sấy là loại cát đã qua xử lý...', 'order': 1},
        {'question': 'Có bao nhiêu loại cát sấy?', 'answer': 'Hiện có 5 loại...', 'order': 2},
        {'question': 'Cát sấy dùng để làm gì?', 'answer': 'Cát sấy thường dùng...', 'order': 3},
        {'question': 'Giá cát sấy bao nhiêu?', 'answer': 'Giá dao động 180,000 - 220,000đ/m³.', 'order': 4}
    ]

    for faq_data in faqs_data:
        if not FAQ.query.filter_by(question=faq_data['question']).first():
            faq = FAQ(**faq_data, is_active=True)
            db.session.add(faq)
            print(f"✅ FAQ: {faq_data['question']}")

    db.session.commit()

    # ==================== SUMMARY ====================
    print("\n🎉 Seed hoàn tất!")
    print(f"📊 Thống kê:")
    print(f"  - Categories: {Category.query.count()}")
    print(f"  - Products: {Product.query.count()}")
    print(f"  - Blogs: {Blog.query.count()}")
    print(f"  - FAQs: {FAQ.query.count()}")