from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, BooleanField, PasswordField, SelectField, SubmitField
from wtforms.fields import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, EqualTo, ValidationError, InputRequired, NumberRange
from app.models import User, Category



# ==================== FORM ĐĂNG NHẬP ====================
class LoginForm(FlaskForm):
    """Form đăng nhập admin"""
    email = StringField('Email', validators=[
        DataRequired(message='Vui lòng nhập email'),
        Email(message='Email không hợp lệ')
    ])
    password = PasswordField('Mật khẩu', validators=[
        DataRequired(message='Vui lòng nhập mật khẩu')
    ])
    remember_me = BooleanField('Ghi nhớ đăng nhập')
    submit = SubmitField('Đăng nhập')


# ==================== FORM LIÊN HỆ ====================
class ContactForm(FlaskForm):
    """Form liên hệ từ khách hàng"""
    name = StringField('Họ và tên', validators=[
        DataRequired(message='Vui lòng nhập họ tên'),
        Length(min=2, max=100, message='Họ tên từ 2-100 ký tự')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Vui lòng nhập email'),
        Email(message='Email không hợp lệ')
    ])
    phone = StringField('Số điện thoại', validators=[
        Optional(),
        Length(max=20)
    ])
    subject = StringField('Tiêu đề', validators=[
        Optional(),
        Length(max=200)
    ])
    message = TextAreaField('Nội dung', validators=[
        DataRequired(message='Vui lòng nhập nội dung'),
        Length(min=10, message='Nội dung tối thiểu 10 ký tự')
    ])
    submit = SubmitField('Gửi liên hệ')


# ==================== FORM DANH MỤC ====================
class CategoryForm(FlaskForm):
    """Form quản lý danh mục"""
    name = StringField('Tên danh mục', validators=[
        DataRequired(message='Vui lòng nhập tên danh mục'),
        Length(min=2, max=100)
    ])
    slug = StringField('Slug (URL)', validators=[
        DataRequired(message='Vui lòng nhập slug'),
        Length(min=2, max=100)
    ])
    description = TextAreaField('Mô tả', validators=[Optional()])
    image = FileField('Hình ảnh', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], 'Chỉ chấp nhận ảnh!')
    ])
    is_active = BooleanField('Kích hoạt')
    submit = SubmitField('Lưu danh mục')


# ==================== FORM SẢN PHẨM ====================
class ProductForm(FlaskForm):
    """Form quản lý sản phẩm"""
    name = StringField('Tên sản phẩm', validators=[
        DataRequired(message='Vui lòng nhập tên sản phẩm'),
        Length(min=2, max=200)
    ])
    slug = StringField('Slug (URL)', validators=[
        DataRequired(message='Vui lòng nhập slug'),
        Length(min=2, max=200)
    ])
    description = TextAreaField('Mô tả sản phẩm', validators=[Optional()])
    price = FloatField('Giá bán', validators=[
        InputRequired(message='Vui lòng nhập giá'),
        NumberRange(min=0, message='Giá phải >= 0')
    ])
    old_price = FloatField('Giá cũ', validators=[Optional(), NumberRange(min=0)])
    category_id = SelectField('Danh mục', coerce=int, validators=[
        DataRequired(message='Vui lòng chọn danh mục')
    ])
    image = FileField('Hình ảnh chính', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], 'Chỉ chấp nhận ảnh!')
    ])
    is_featured = BooleanField('Sản phẩm nổi bật')
    is_active = BooleanField('Kích hoạt', default=True)
    submit = SubmitField('Lưu sản phẩm')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        # Load danh mục vào dropdown
        self.category_id.choices = [(0, '-- Chọn danh mục --')] + [
            (c.id, c.name) for c in Category.query.filter_by(is_active=True).all()
        ]


# ==================== FORM BANNER ====================
class BannerForm(FlaskForm):
    """Form quản lý banner slider"""
    title = StringField('Tiêu đề', validators=[
        Optional(),
        Length(max=200)
    ])
    subtitle = StringField('Phụ đề', validators=[
        Optional(),
        Length(max=255)
    ])
    image = FileField('Hình ảnh', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], 'Chỉ chấp nhận ảnh!')
    ])
    link = StringField('Link', validators=[Optional(), Length(max=255)])
    button_text = StringField('Text nút', validators=[Optional(), Length(max=50)])
    order = FloatField('Thứ tự', validators=[Optional()])
    is_active = BooleanField('Kích hoạt')
    submit = SubmitField('Lưu banner')


# ==================== FORM BLOG ====================
class BlogForm(FlaskForm):
    """Form quản lý tin tức/blog với SEO optimization"""

    # Basic fields
    title = StringField('Tiêu đề', validators=[
        DataRequired(message='Vui lòng nhập tiêu đề'),
        Length(min=5, max=200)
    ])
    slug = StringField('Slug (URL)', validators=[
        DataRequired(message='Vui lòng nhập slug'),
        Length(min=5, max=200)
    ])
    excerpt = TextAreaField('Mô tả ngắn', validators=[Optional()])
    content = TextAreaField('Nội dung', validators=[
        DataRequired(message='Vui lòng nhập nội dung')
    ])
    image = FileField('Hình ảnh', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif', 'webp'], 'Chỉ chấp nhận ảnh!')
    ])
    author = StringField('Tác giả', validators=[Optional(), Length(max=100)])
    is_featured = BooleanField('Tin nổi bật')
    is_active = BooleanField('Kích hoạt')

    # ✅ THÊM SEO FIELDS
    focus_keyword = StringField('Focus Keyword', validators=[
        Optional(),
        Length(max=100, message='Focus Keyword tối đa 100 ký tự')
    ])
    meta_title = StringField('Meta Title (SEO Title)', validators=[
        Optional(),
        Length(max=70, message='Meta Title nên <= 60 ký tự để hiển thị đầy đủ trên Google')
    ])
    meta_description = TextAreaField('Meta Description', validators=[
        Optional(),
        Length(max=160, message='Meta Description nên 120-160 ký tự')
    ])
    meta_keywords = StringField('Meta Keywords (optional)', validators=[
        Optional(),
        Length(max=255)
    ])

    submit = SubmitField('Lưu bài viết')

# ==================== FORM FAQ ====================
class FAQForm(FlaskForm):
    """Form quản lý câu hỏi thường gặp"""
    question = StringField('Câu hỏi', validators=[
        DataRequired(message='Vui lòng nhập câu hỏi'),
        Length(min=5, max=255)
    ])
    answer = TextAreaField('Câu trả lời', validators=[
        DataRequired(message='Vui lòng nhập câu trả lời')
    ])
    order = FloatField('Thứ tự', validators=[Optional()])
    is_active = BooleanField('Kích hoạt')
    submit = SubmitField('Lưu FAQ')


# ==================== FORM USER ====================
class UserForm(FlaskForm):
    """Form quản lý người dùng"""
    username = StringField('Tên đăng nhập', validators=[
        DataRequired(message='Vui lòng nhập tên đăng nhập'),
        Length(min=3, max=80)
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Vui lòng nhập email'),
        Email(message='Email không hợp lệ')
    ])
    password = PasswordField('Mật khẩu', validators=[
        Optional(),
        Length(min=6, message='Mật khẩu tối thiểu 6 ký tự')
    ])
    confirm_password = PasswordField('Xác nhận mật khẩu', validators=[
        EqualTo('password', message='Mật khẩu không khớp')
    ])
    is_admin = BooleanField('Quản trị viên')
    submit = SubmitField('Lưu người dùng')

    def __init__(self, user=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate_username(self, username):
        """Kiểm tra username có trùng không"""
        user = User.query.filter_by(username=username.data).first()
        if user and (self.user is None or user.id != self.user.id):
            raise ValidationError('Tên đăng nhập đã tồn tại')

    def validate_email(self, email):
        """Kiểm tra email có trùng không"""
        user = User.query.filter_by(email=email.data).first()
        if user and (self.user is None or user.id != self.user.id):
            raise ValidationError('Email đã tồn tại')



class MediaSEOForm(FlaskForm):
    """Form chỉnh sửa SEO cho media (không upload file mới)"""
    alt_text = StringField('Alt Text', validators=[
        DataRequired(message='Alt Text là bắt buộc cho SEO'),
        Length(min=10, max=125, message='Alt Text nên từ 30-125 ký tự')
    ])
    title = StringField('Title', validators=[
        Optional(),
        Length(max=255)
    ])
    caption = TextAreaField('Caption', validators=[
        Optional(),
        Length(max=500)
    ])
    album = StringField('Album', validators=[Optional()])
    submit = SubmitField('Lưu thay đổi')

