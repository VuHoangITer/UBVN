from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


# ==================== USER MODEL ====================
class User(UserMixin, db.Model):
    """Model quản lý người dùng (Admin)"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Hash password trước khi lưu vào DB"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Kiểm tra password có đúng không"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login dùng hàm này để load user từ session"""
    return User.query.get(int(user_id))


# ==================== CATEGORY MODEL ====================
class Category(db.Model):
    """Model danh mục sản phẩm"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship với Product
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<Category {self.name}>'


# ==================== PRODUCT MODEL ====================
class Product(db.Model):
    """Model sản phẩm"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0)
    old_price = db.Column(db.Float)
    image = db.Column(db.String(255))
    images = db.Column(db.Text)  # JSON string chứa nhiều ảnh
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    image_alt_text = db.Column(db.String(255))
    image_title = db.Column(db.String(255))
    image_caption = db.Column(db.Text)

    # Trong class Product
    def get_media_seo_info(self):
        """Lấy thông tin SEO từ Media Library dựa vào image path"""
        if not self.image:
            return None

        # Tìm media có filepath khớp với product.image
        media = Media.query.filter_by(filepath=self.image).first()

        if media:
            return {
                'alt_text': media.alt_text,
                'title': media.title,
                'caption': media.caption
            }
        return None


    def __repr__(self):
        return f'<Product {self.name}>'


# ==================== BANNER MODEL ====================
class Banner(db.Model):
    """Model banner slider trang chủ"""
    __tablename__ = 'banners'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    subtitle = db.Column(db.String(255))
    image = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255))
    button_text = db.Column(db.String(50))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Trong class Banner
    def get_media_seo_info(self):
        """Lấy thông tin SEO từ Media Library dựa vào image path"""
        if not self.image:
            return None

        media = Media.query.filter_by(filepath=self.image).first()

        if media:
            return {
                'alt_text': media.alt_text,
                'title': media.title,
                'caption': media.caption
            }
        return None

    def __repr__(self):
        return f'<Banner {self.title}>'


# ==================== BLOG MODEL ====================
class Blog(db.Model):
    """Model tin tức / blog với SEO optimization"""
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    excerpt = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))
    author = db.Column(db.String(100))
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Legacy image SEO fields (giữ lại để tương thích)
    image_alt_text = db.Column(db.String(255))
    image_title = db.Column(db.String(255))
    image_caption = db.Column(db.Text)

    # SEO
    meta_title = db.Column(db.String(70))  # SEO title tag (50-60 ký tự tối ưu)
    meta_description = db.Column(db.String(160))  # Meta description (120-160 ký tự)
    meta_keywords = db.Column(db.String(255))  # Keywords (optional, ít quan trọng)
    focus_keyword = db.Column(db.String(100))  # Từ khóa chính để tính SEO score

    # Reading metrics
    reading_time = db.Column(db.Integer)  # Thời gian đọc ước tính (phút)
    word_count = db.Column(db.Integer)  # Số từ trong bài viết

    # SEO Score tracking
    seo_score = db.Column(db.Integer, default=0)
    seo_grade = db.Column(db.String(5), default='F')
    seo_last_checked = db.Column(db.DateTime)

    def get_media_seo_info(self):
        """Lấy thông tin SEO từ Media Library dựa vào image path"""
        if not self.image:
            return None

        media = Media.query.filter_by(filepath=self.image).first()

        if media:
            return {
                'alt_text': media.alt_text,
                'title': media.title,
                'caption': media.caption
            }
        return None

    def calculate_reading_time(self):
        """Tính thời gian đọc dựa trên số từ (200 từ/phút)"""
        if self.content:
            from html import unescape
            import re
            # Strip HTML tags
            text = re.sub(r'<[^>]+>', '', self.content)
            text = unescape(text)
            words = len(text.split())
            self.word_count = words
            self.reading_time = max(1, round(words / 200))
        else:
            self.word_count = 0
            self.reading_time = 1

    def update_seo_score(self):
        """Tính và lưu điểm SEO vào database"""
        from app.admin.routes import calculate_blog_seo_score
        result = calculate_blog_seo_score(self)
        self.seo_score = result['score']
        self.seo_grade = result['grade']
        self.seo_last_checked = datetime.utcnow()
        return result

    def get_seo_info(self):
        """Lấy thông tin SEO (ưu tiên từ cache nếu chưa quá 1 giờ)"""
        if (self.seo_score is None or
                self.seo_last_checked is None or
                (datetime.utcnow() - self.seo_last_checked).total_seconds() > 3600):
            return self.update_seo_score()

        from app.admin.routes import calculate_blog_seo_score
        current_result = calculate_blog_seo_score(self)

        if current_result['score'] != self.seo_score:
            self.seo_score = current_result['score']
            self.seo_grade = current_result['grade']
            self.seo_last_checked = datetime.utcnow()
            db.session.commit()

        return current_result

    def __repr__(self):
        return f'<Blog {self.title}>'


# ==================== FAQ MODEL ====================
class FAQ(db.Model):
    """Model câu hỏi thường gặp"""
    __tablename__ = 'faqs'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FAQ {self.question[:50]}>'


# ==================== CONTACT MODEL ====================
class Contact(db.Model):
    """Model lưu thông tin liên hệ từ khách hàng"""
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Contact {self.name} - {self.email}>'


# ==================== MEDIA MODEL ====================
class Media(db.Model):
    """Model quản lý hình ảnh/media files với SEO optimization"""
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255))
    filepath = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

    # SEO Fields
    alt_text = db.Column(db.String(255))
    title = db.Column(db.String(255))
    caption = db.Column(db.Text)

    # Organization
    album = db.Column(db.String(100))

    # ✅ THÊM 3 FIELD NÀY ĐỂ LƯU ĐIỂM SEO
    seo_score = db.Column(db.Integer, default=0)
    seo_grade = db.Column(db.String(5), default='F')
    seo_last_checked = db.Column(db.DateTime)

    # Metadata
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Media {self.filename}>'

    def get_url(self):
        return self.filepath if self.filepath.startswith('/') else f'/{self.filepath}'

    def get_size_mb(self):
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return 0

    # ✅ THAY THẾ 2 METHOD CŨ BẰNG 2 METHOD MỚI
    def update_seo_score(self):
        """Tính và lưu điểm SEO vào database"""
        from app.admin.routes import calculate_seo_score
        result = calculate_seo_score(self)
        self.seo_score = result['score']
        self.seo_grade = result['grade']
        self.seo_last_checked = datetime.utcnow()
        return result

    def get_seo_info(self):
        """Lấy thông tin SEO (ưu tiên từ cache)"""
        # Nếu chưa tính lần nào hoặc đã quá 1 giờ, tính lại
        if (self.seo_score is None or
                self.seo_last_checked is None or
                (datetime.utcnow() - self.seo_last_checked).total_seconds() > 3600):
            return self.update_seo_score()

        # Nếu có rồi, tính nhanh để so sánh
        from app.admin.routes import calculate_seo_score
        current_result = calculate_seo_score(self)

        # Nếu điểm thay đổi, update
        if current_result['score'] != self.seo_score:
            self.seo_score = current_result['score']
            self.seo_grade = current_result['grade']
            self.seo_last_checked = datetime.utcnow()
            db.session.commit()

        return current_result

