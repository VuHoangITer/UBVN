"""
SEO Keywords Configuration
Dễ dàng chỉnh sửa keywords mà không cần sửa code logic
"""

# Keywords cho Media/Image SEO
MEDIA_KEYWORDS = {
    'primary': [
        'cát sấy',
        'cát sấy số 1',
        'cát sấy số 2',
        'cát sấy số 3',
        'cát sấy số 4',
        'cát sấy số 5',
        'catsay.com.vn'
    ],
    'secondary': [
        'cát sấy loại 1 0.15mm-0.3mm',
        'cát sấy loại 2 0.3mm-0.6mm',
        'cát sấy loại 3 0.6mm-1.2mm',
        'cát công nghiệp',
        'cát lọc',
        'keo ốp lát',
        'công trinh',
        'sản xuất',
        'gạch',
        'vữa khô',
        'keo ốp lát',
        'cát làm sạch'
    ],
    'brand': [
        'ub',
        'cát sấy',
        'cong ty ub'
    ],
    'general': [
        'vật liệu',
        'xây dựng',
        'công nghiệp',
        'sản phẩm',
        'công trình',
        'dịch vụ',
        'cát',
        'nhà máy sản xuất vữa'
        'vật liệu lọc'
    ]
}

# Scoring weights (có thể tùy chỉnh)
KEYWORD_SCORES = {
    'primary': 20,      # Full score nếu có primary keyword
    'secondary_brand': 17,  # Secondary + Brand
    'secondary': 12,    # Chỉ có secondary
    'brand': 8,         # Chỉ có brand
    'general': 5        # Chỉ có general keywords
}