"""
SEO Keywords Configuration
Dễ dàng chỉnh sửa keywords mà không cần sửa code logic
"""

# Keywords cho Media/Image SEO
# ==================== MEDIA / IMAGE SEO KEYWORDS ====================
MEDIA_KEYWORDS = {
    'primary': [
        'cát sấy',
        'cát sấy số 1',
        'cát sấy số 2',
        'cát sấy số 3',
        'cát sấy số 4',
        'cát sấy số 5',
        'UBVN.com.vn',
        'cát sấy UB',
        'cát sấy công ty UB',
        'cát sấy công ty UBVN',
        'ubvn.onrender.com',
        'cát sấy ubvn.onrender.com'
    ],
    'secondary': [
        'cát sấy loại 1 0.15mm-0.3mm',
        'cát sấy loại 2 0.3mm-0.6mm',
        'cát sấy loại 3 0.6mm-1.2mm',
        'cát công nghiệp',
        'cát lọc nước',
        'keo ốp lát',
        'công trình xây dựng',
        'sản xuất vật liệu',
        'gạch xây dựng',
        'vữa khô trộn sẵn',
        'cát làm sạch bề mặt'
    ],
    'brand': [
        'UB',
        'cát sấy UB',
        'công ty UB'
    ],
    'general': [
        'vật liệu xây dựng',
        'công nghiệp',
        'sản phẩm',
        'công trình',
        'dịch vụ',
        'cát',
        'nhà máy sản xuất vữa',
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