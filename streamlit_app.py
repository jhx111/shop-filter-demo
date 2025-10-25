import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# 设置页面
st.set_page_config(page_title="电商商品筛选系统", page_icon="🛒", layout="wide")


# 初始化session state
def initialize_session_state():
    defaults = {
        'current_page': 'home',
        'selected_product': None,
        'view_history': [],
        'price_alerts': [],
        'current_slide': 0,
        'carousel_running': True,
        'last_carousel_update': time.time(),
        'carousel_countdown': 3,
        'search_input': '',
        'category_select': '全部',
        'price_select': '全部',
        'shipping_select': '全部',
        'filtered_products': [],
        'show_no_results': False,
        'product_detail_slide': 0,
        'last_price_check': time.time(),
        'set_expression': ''
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# 立即初始化
initialize_session_state()

# 完整的45个商品数据
products = [
    # 家电类商品 (15个)
    {
        "id": 1, "name": "智能变频冰箱", "category": "家电", "price": 3599, "original_price": 4299,
        "free_shipping": True, "stock": 150, "sales": 3280, "rating": 4.8, "reviews": 1250,
        "image_url": "https://k.sinaimg.cn/n/sinacn20115/538/w640h698/20190601/acbe-hxvzhtf1763894.jpg/w700d1q75cms.jpg",
        "description": "智能变频节能冰箱，超大容量，智能温控",
        "details": """• 智能变频技术，节能省电
• 风冷无霜设计，食物更新鲜  
• 一级能效标准，环保节能
• 手机APP远程控制，智能便捷
• 超大冷冻空间，满足全家需求
• 静音运行，不打扰生活
• 多功能储物格，分类存放""",
        "specs": {
            "容量": "500L",
            "能效等级": "一级",
            "制冷方式": "风冷",
            "控制方式": "电脑控温",
            "尺寸": "180×60×65cm"
        },
        "store_name": "家电旗舰店",
        "store_rating": 4.9,
        "carousel_images": [
            "https://picx.zhimg.com/v2-ea75a2949b2be82e8a06f40553ceabe5_r.jpg?source=1940ef5c",
            "https://pic2.zhimg.com/v2-1ed398528603f70fda179dd316ec1ce9_r.jpg",
            "https://zhongces3.sina.com.cn/product/20220107/44d92e57ba69f677fea265304d78ab56.jpeg",
            "http://imgm.cnmo.com/manu_photo/new/home_pruduct_zhaimi_small/10_1024x768/499/ho8LxowssJavY.jpg"
        ],
        "product_images": [
            "https://pic2.zhimg.com/v2-1ed398528603f70fda179dd316ec1ce9_r.jpg",
            "https://zhongces3.sina.com.cn/product/20220107/44d92e57ba69f677fea265304d78ab56.jpeg",
            "http://imgm.cnmo.com/manu_photo/new/home_pruduct_zhaimi_small/10_1024x768/499/ho8LxowssJavY.jpg"
        ],
        "reviews_list": [
            {"user": "用户123", "rating": 5, "comment": "冰箱很好用，空间很大，制冷效果棒！", "date": "2024-01-15"},
            {"user": "购物达人", "rating": 4, "comment": "外观漂亮，就是声音稍微有点大", "date": "2024-01-10"},
            {"user": "家电爱好者", "rating": 5, "comment": "智能控制很方便，推荐购买", "date": "2024-01-08"}
        ]
    },
    {
        "id": 2, "name": "无线降噪耳机", "category": "家电", "price": 799, "original_price": 999,
        "free_shipping": True, "stock": 200, "sales": 5560, "rating": 4.9, "reviews": 2890,
        "image_url": "https://cdn.jsdelivr.net/gh/streamlit-lssx/images@main/2.jpg",
        "description": "高保真音质，主动降噪功能，持久续航30小时",
        "store_name": "数码专营店",
        "store_rating": 4.8,
        "carousel_images": [
            "https://cdn.jsdelivr.net/gh/streamlit-lssx/images@main/2_c0.jpg",
            "https://cdn.jsdelivr.net/gh/streamlit-lssx/images@main/2_c1.jpg",
            "https://cdn.jsdelivr.net/gh/streamlit-lssx/images@main/2_c2.jpg"
        ]
    },
    {
        "id": 3, "name": "4K超清电视", "category": "家电", "price": 2999, "original_price": 3999,
        "free_shipping": True, "stock": 80, "sales": 2230, "rating": 4.7, "reviews": 1560,
        "image_url": "https://cdn.jsdelivr.net/gh/streamlit-lssx/images@main/3.jpg",
        "description": "4K超清显示，智能语音控制，沉浸式观影体验",
        "store_name": "家电旗舰店",
        "store_rating": 4.9
    },
    {
        "id": 4, "name": "滚筒洗衣机", "category": "家电", "price": 1899, "original_price": 2399,
        "free_shipping": True, "stock": 120, "sales": 1890, "rating": 4.6, "reviews": 980,
        "image_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "description": "智能变频，省水省电，多种洗涤模式",
        "store_name": "家电旗舰店",
        "store_rating": 4.9
    },
    {
        "id": 5, "name": "空调挂机", "category": "家电", "price": 2599, "original_price": 3199,
        "free_shipping": False, "stock": 90, "sales": 3120, "rating": 4.8, "reviews": 2100,
        "image_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "description": "变频节能，快速制冷，静音设计",
        "store_name": "空调专营店",
        "store_rating": 4.7
    },
    {
        "id": 6, "name": "微波炉", "category": "家电", "price": 399, "original_price": 599,
        "free_shipping": True, "stock": 300, "sales": 4560, "rating": 4.5, "reviews": 2890,
        "image_url": "https://images.unsplash.com/photo-1616627561687-3bb119db79da?w=400",
        "description": "多功能微波炉，智能菜单，简单易用",
        "store_name": "厨房电器店",
        "store_rating": 4.6
    },
    {
        "id": 7, "name": "电饭煲", "category": "家电", "price": 299, "original_price": 399,
        "free_shipping": True, "stock": 500, "sales": 7890, "rating": 4.7, "reviews": 4560,
        "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400",
        "description": "智能电饭煲，多种烹饪模式，精准控温",
        "store_name": "厨房电器店",
        "store_rating": 4.6
    },
    {
        "id": 8, "name": "吸尘器", "category": "家电", "price": 699, "original_price": 899,
        "free_shipping": True, "stock": 180, "sales": 2340, "rating": 4.6, "reviews": 1670,
        "image_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "description": "无线手持吸尘器，强力吸尘，轻便设计",
        "store_name": "清洁电器店",
        "store_rating": 4.5
    },
    {
        "id": 9, "name": "电风扇", "category": "家电", "price": 199, "original_price": 299,
        "free_shipping": True, "stock": 400, "sales": 5670, "rating": 4.4, "reviews": 3120,
        "image_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "description": "静音电风扇，多档风速，节能省电",
        "store_name": "家电旗舰店",
        "store_rating": 4.9
    },
    {
        "id": 10, "name": "热水器", "category": "家电", "price": 1299, "original_price": 1699,
        "free_shipping": False, "stock": 100, "sales": 1780, "rating": 4.7, "reviews": 1230,
        "image_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "description": "即热式电热水器，安全节能，快速加热",
        "store_name": "卫浴电器店",
        "store_rating": 4.6
    },
    {
        "id": 11, "name": "空气净化器", "category": "家电", "price": 899, "original_price": 1199,
        "free_shipping": True, "stock": 150, "sales": 2670, "rating": 4.8, "reviews": 1890,
        "image_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "description": "高效空气净化，智能检测，静音运行",
        "store_name": "健康电器店",
        "store_rating": 4.7
    },
    {
        "id": 12, "name": "榨汁机", "category": "家电", "price": 199, "original_price": 299,
        "free_shipping": True, "stock": 350, "sales": 4230, "rating": 4.5, "reviews": 2780,
        "image_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "description": "多功能榨汁机，易清洗，操作简单",
        "store_name": "厨房电器店",
        "store_rating": 4.6
    },
    {
        "id": 13, "name": "电磁炉", "category": "家电", "price": 299, "original_price": 399,
        "free_shipping": True, "stock": 280, "sales": 3340, "rating": 4.6, "reviews": 2230,
        "image_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "description": "智能电磁炉，多档火力，安全耐用",
        "store_name": "厨房电器店",
        "store_rating": 4.6
    },
    {
        "id": 14, "name": "电水壶", "category": "家电", "price": 129, "original_price": 199,
        "free_shipping": True, "stock": 600, "sales": 7890, "rating": 4.5, "reviews": 5120,
        "image_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "description": "快速电水壶，食品级材质，自动断电",
        "store_name": "厨房电器店",
        "store_rating": 4.6
    },
    {
        "id": 15, "name": "面包机", "category": "家电", "price": 399, "original_price": 499,
        "free_shipping": True, "stock": 120, "sales": 1560, "rating": 4.4, "reviews": 980,
        "image_url": "https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=400",
        "description": "全自动面包机，多种程序，简单烘焙",
        "store_name": "厨房电器店",
        "store_rating": 4.6
    },

    # 服装类商品 (15个)
    {
        "id": 16, "name": "纯棉休闲T恤", "category": "服装", "price": 89, "original_price": 129,
        "free_shipping": False, "stock": 150, "sales": 4890, "rating": 4.6, "reviews": 3120,
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
        "description": "100%纯棉材质，舒适透气，多色可选",
        "store_name": "时尚服饰店",
        "store_rating": 4.7
    },
    {
        "id": 17, "name": "牛仔裤", "category": "服装", "price": 199, "original_price": 299,
        "free_shipping": True, "stock": 200, "sales": 3340, "rating": 4.7, "reviews": 2230,
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
        "description": "修身牛仔裤，弹性面料，多尺码可选",
        "store_name": "牛仔专营店",
        "store_rating": 4.8
    },
    {
        "id": 18, "name": "羽绒服", "category": "服装", "price": 599, "original_price": 899,
        "free_shipping": True, "stock": 80, "sales": 1560, "rating": 4.8, "reviews": 980,
        "image_url": "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=400",
        "description": "保暖羽绒服，防风防水，冬季必备",
        "store_name": "冬季服饰店",
        "store_rating": 4.7
    },
    {
        "id": 19, "name": "运动鞋", "category": "服装", "price": 299, "original_price": 399,
        "free_shipping": True, "stock": 250, "sales": 4230, "rating": 4.6, "reviews": 2890,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        "description": "舒适运动鞋，透气耐磨，多色可选",
        "store_name": "运动专营店",
        "store_rating": 4.8
    },
    {
        "id": 20, "name": "衬衫", "category": "服装", "price": 159, "original_price": 229,
        "free_shipping": False, "stock": 180, "sales": 2780, "rating": 4.5, "reviews": 1670,
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400",
        "description": "商务衬衫，挺括有型，多尺码",
        "store_name": "商务服饰店",
        "store_rating": 4.6
    },
    {
        "id": 21, "name": "连衣裙", "category": "服装", "price": 259, "original_price": 359,
        "free_shipping": True, "stock": 120, "sales": 1890, "rating": 4.7, "reviews": 1230,
        "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400",
        "description": "优雅连衣裙，修身设计，多种场合",
        "store_name": "女装专营店",
        "store_rating": 4.7
    },
    {
        "id": 22, "name": "卫衣", "category": "服装", "price": 139, "original_price": 199,
        "free_shipping": True, "stock": 200, "sales": 3120, "rating": 4.6, "reviews": 2230,
        "image_url": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400",
        "description": "休闲卫衣，舒适保暖，时尚潮流",
        "store_name": "潮流服饰店",
        "store_rating": 4.6
    },
    {
        "id": 23, "name": "西装外套", "category": "服装", "price": 499, "original_price": 699,
        "free_shipping": False, "stock": 60, "sales": 890, "rating": 4.8, "reviews": 560,
        "image_url": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400",
        "description": "商务西装，精致剪裁，正式场合",
        "store_name": "商务服饰店",
        "store_rating": 4.7
    },
    {
        "id": 24, "name": "休闲裤", "category": "服装", "price": 179, "original_price": 259,
        "free_shipping": True, "stock": 150, "sales": 2340, "rating": 4.5, "reviews": 1670,
        "image_url": "https://images.unsplash.com/photo-1542272454315-7ad49baa5d3f?w=400",
        "description": "舒适休闲裤，弹性面料，多尺码",
        "store_name": "休闲服饰店",
        "store_rating": 4.6
    },
    {
        "id": 25, "name": "毛衣", "category": "服装", "price": 219, "original_price": 319,
        "free_shipping": True, "stock": 100, "sales": 1670, "rating": 4.7, "reviews": 1120,
        "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400",
        "description": "温暖毛衣，柔软舒适，冬季必备",
        "store_name": "冬季服饰店",
        "store_rating": 4.7
    },
    {
        "id": 26, "name": "短袖T恤", "category": "服装", "price": 69, "original_price": 99,
        "free_shipping": False, "stock": 300, "sales": 4560, "rating": 4.4, "reviews": 3120,
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
        "description": "夏季短袖T恤，清凉透气，多色可选",
        "store_name": "夏季服饰店",
        "store_rating": 4.5
    },
    {
        "id": 27, "name": "风衣", "category": "服装", "price": 399, "original_price": 599,
        "free_shipping": True, "stock": 70, "sales": 1230, "rating": 4.8, "reviews": 890,
        "image_url": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400",
        "description": "时尚风衣，防风保暖，春秋必备",
        "store_name": "外套专营店",
        "store_rating": 4.7
    },
    {
        "id": 28, "name": "运动裤", "category": "服装", "price": 129, "original_price": 189,
        "free_shipping": True, "stock": 180, "sales": 2780, "rating": 4.6, "reviews": 1890,
        "image_url": "https://images.unsplash.com/photo-1542272454315-7ad49baa5d3f?w=400",
        "description": "舒适运动裤，弹性面料，运动休闲",
        "store_name": "运动专营店",
        "store_rating": 4.7
    },
    {
        "id": 29, "name": "皮夹克", "category": "服装", "price": 699, "original_price": 999,
        "free_shipping": False, "stock": 40, "sales": 670, "rating": 4.9, "reviews": 450,
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        "description": "真皮夹克，时尚有型，质感出众",
        "store_name": "皮革专营店",
        "store_rating": 4.8
    },
    {
        "id": 30, "name": "针织衫", "category": "服装", "price": 189, "original_price": 279,
        "free_shipping": True, "stock": 120, "sales": 1890, "rating": 4.6, "reviews": 1340,
        "image_url": "https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400",
        "description": "柔软针织衫，舒适保暖，多色可选",
        "store_name": "针织专营店",
        "store_rating": 4.6
    },

    # 食品类商品 (15个)
    {
        "id": 31, "name": "薯片零食大礼包", "category": "食品", "price": 39, "original_price": 59,
        "free_shipping": False, "stock": 500, "sales": 12890, "rating": 4.3, "reviews": 7890,
        "image_url": "https://images.unsplash.com/photo-1566476969070-0154d61da1bf?w=400",
        "description": "香脆可口，多种口味，休闲零食",
        "store_name": "零食专营店",
        "store_rating": 4.5
    },
    {
        "id": 32, "name": "进口巧克力", "category": "食品", "price": 69, "original_price": 99,
        "free_shipping": True, "stock": 300, "sales": 5670, "rating": 4.8, "reviews": 4120,
        "image_url": "https://images.unsplash.com/photo-1575377427642-087cf684f29d?w=400",
        "description": "比利时进口巧克力，丝滑口感，精美包装",
        "store_name": "进口食品店",
        "store_rating": 4.9
    },
    {
        "id": 33, "name": "坚果礼盒", "category": "食品", "price": 129, "original_price": 189,
        "free_shipping": True, "stock": 200, "sales": 2340, "rating": 4.7, "reviews": 1670,
        "image_url": "https://images.unsplash.com/photo-1550258987-190a2d41a8ba?w=400",
        "description": "精选坚果，营养丰富，送礼佳品",
        "store_name": "坚果专营店",
        "store_rating": 4.8
    },
    {
        "id": 34, "name": "速溶咖啡", "category": "食品", "price": 49, "original_price": 79,
        "free_shipping": False, "stock": 400, "sales": 6780, "rating": 4.4, "reviews": 4560,
        "image_url": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400",
        "description": "香浓速溶咖啡，提神醒脑，方便快捷",
        "store_name": "咖啡专营店",
        "store_rating": 4.6
    },
    {
        "id": 35, "name": "有机大米", "category": "食品", "price": 89, "original_price": 129,
        "free_shipping": False, "stock": 300, "sales": 4560, "rating": 4.6, "reviews": 3120,
        "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400",
        "description": "有机种植大米，香糯可口，健康营养",
        "store_name": "粮油专营店",
        "store_rating": 4.7
    },
    {
        "id": 36, "name": "瓶装矿泉水", "category": "食品", "price": 24, "original_price": 36,
        "free_shipping": True, "stock": 800, "sales": 12340, "rating": 4.2, "reviews": 7890,
        "image_url": "https://images.unsplash.com/photo-1548839149-851a5e9115dd?w=400",
        "description": "天然矿泉水，清凉解渴，24瓶装",
        "store_name": "饮料专营店",
        "store_rating": 4.4
    },
    {
        "id": 37, "name": "饼干礼盒", "category": "食品", "price": 59, "original_price": 89,
        "free_shipping": True, "stock": 250, "sales": 3450, "rating": 4.5, "reviews": 2340,
        "image_url": "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400",
        "description": "精美饼干礼盒，多种口味，送礼佳品",
        "store_name": "糕点专营店",
        "store_rating": 4.6
    },
    {
        "id": 38, "name": "茶叶礼盒", "category": "食品", "price": 199, "original_price": 299,
        "free_shipping": True, "stock": 150, "sales": 1890, "rating": 4.8, "reviews": 1340,
        "image_url": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400",
        "description": "特级茶叶，清香醇厚，精美包装",
        "store_name": "茶叶专营店",
        "store_rating": 4.8
    },
    {
        "id": 39, "name": "蜂蜜", "category": "食品", "price": 79, "original_price": 119,
        "free_shipping": True, "stock": 180, "sales": 2670, "rating": 4.7, "reviews": 1890,
        "image_url": "https://images.unsplash.com/photo-1587049633312-d628ae50a8ae?w=400",
        "description": "纯天然蜂蜜，营养丰富，健康养生",
        "store_name": "养生食品店",
        "store_rating": 4.7
    },
    {
        "id": 40, "name": "方便面", "category": "食品", "price": 12, "original_price": 18,
        "free_shipping": False, "stock": 600, "sales": 15670, "rating": 4.1, "reviews": 10230,
        "image_url": "https://images.unsplash.com/photo-1612927601601-6638404737ce?w=400",
        "description": "美味方便面，多种口味，快捷方便",
        "store_name": "速食专营店",
        "store_rating": 4.3
    },
    {
        "id": 41, "name": "果汁饮料", "category": "食品", "price": 15, "original_price": 25,
        "free_shipping": True, "stock": 400, "sales": 7890, "rating": 4.3, "reviews": 5670,
        "image_url": "https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=400",
        "description": "鲜榨果汁，营养美味，多种口味",
        "store_name": "饮料专营店",
        "store_rating": 4.4
    },
    {
        "id": 42, "name": "牛肉干", "category": "食品", "price": 45, "original_price": 68,
        "free_shipping": True, "stock": 220, "sales": 3450, "rating": 4.6, "reviews": 2340,
        "image_url": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400",
        "description": "香辣牛肉干，嚼劲十足，休闲零食",
        "store_name": "肉制品专营店",
        "store_rating": 4.7
    },
    {
        "id": 43, "name": "奶粉", "category": "食品", "price": 159, "original_price": 229,
        "free_shipping": False, "stock": 120, "sales": 1890, "rating": 4.7, "reviews": 1340,
        "image_url": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400",
        "description": "婴幼儿奶粉，营养均衡，安全可靠",
        "store_name": "奶粉专营店",
        "store_rating": 4.8
    },
    {
        "id": 44, "name": "橄榄油", "category": "食品", "price": 89, "original_price": 139,
        "free_shipping": True, "stock": 150, "sales": 2230, "rating": 4.6, "reviews": 1670,
        "image_url": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=400",
        "description": "特级初榨橄榄油，健康烹饪，营养丰富",
        "store_name": "食用油专营店",
        "store_rating": 4.7
    },
    {
        "id": 45, "name": "速冻水饺", "category": "食品", "price": 29, "original_price": 45,
        "free_shipping": False, "stock": 350, "sales": 5670, "rating": 4.4, "reviews": 3890,
        "image_url": "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=400",
        "description": "美味速冻水饺，多种馅料，方便快捷",
        "store_name": "速冻食品店",
        "store_rating": 4.5
    }
]

# 为所有商品添加默认的轮播图和评价数据
for product in products:
    if 'carousel_images' not in product:
        product['carousel_images'] = [
            product['image_url'],
            "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=600",
            "https://cdn.jsdelivr.net/gh/streamlit-lssx/images@main/2_c0.jpg"
        ]
    if 'product_images' not in product:
        product['product_images'] = [
            product['image_url'],
            "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=600",
            "https://cdn.jsdelivr.net/gh/streamlit-lssx/images@main/2_c0.jpg",
            "https://cdn.jsdelivr.net/gh/streamlit-lssx/images@main/1_c2.jpg"
        ]
    if 'reviews_list' not in product:
        product['reviews_list'] = [
            {"user": f"用户{random.randint(1000, 9999)}", "rating": random.randint(4, 5),
             "comment": "商品质量很好，很满意！", "date": f"2024-01-{random.randint(10, 20)}"},
            {"user": f"买家{random.randint(1000, 9999)}", "rating": random.randint(4, 5),
             "comment": "性价比很高，推荐购买", "date": f"2024-01-{random.randint(5, 15)}"},
            {"user": f"顾客{random.randint(1000, 9999)}", "rating": random.randint(3, 5),
             "comment": "还不错，符合预期", "date": f"2024-01-{random.randint(1, 10)}"}
        ]
    if 'specs' not in product:
        product['specs'] = {
            "品牌": "知名品牌",
            "材质": "优质材料",
            "产地": "中国",
            "保质期": "12个月",
            "存储方式": "阴凉干燥处"
        }
    if 'details' not in product:
        product['details'] = "优质商品，精心制作，满足您的需求"


# 自定义CSS
def setup_css():
    st.markdown("""
    <style>
    /* ===== 通用背景图 ===== */
    body, .main, [data-testid="stAppViewContainer"]{
        background-image: url("https://images.unsplash.com/photo-1557683316-973673baf926?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }
    /* 让卡片/详情容器带一点毛玻璃效果，避免背景太花 */
    .main-container, .detail-container, .product-card, .store-info{
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
    }
    /* 其余样式保持你原来即可 */
    

    /* 轮播图样式 */
    .carousel-container {
        position: relative;
        width: 100%;
        height: 300px;
        overflow: hidden;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .carousel-slide {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .countdown-timer {
        position: absolute;
        top: 15px;
        right: 15px;
        background: rgba(0,0,0,0.7);
        color: white;
        padding: 8px 12px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
    }

    /* 商品详情页轮播图 */
    .product-carousel {
        position: relative;
        width: 100%;
        height: 500px;
        overflow: hidden;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .product-carousel-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .carousel-controls {
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 10px;
    }

    .carousel-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: rgba(255,255,255,0.5);
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .carousel-dot.active {
        background: white;
        transform: scale(1.2);
    }

    /* 商品卡片 */
    .product-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid #f0f0f0;
        cursor: pointer;
        margin-bottom: 20px;
    }

    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }

    .product-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 10px;
    }

    .product-name {
        font-weight: bold;
        font-size: 16px;
        margin: 8px 0;
        color: #333;
    }

    .product-price {
        color: #ff4444;
        font-weight: bold;
        font-size: 18px;
        margin: 5px 0;
    }

    .original-price {
        color: #999;
        text-decoration: line-through;
        font-size: 14px;
        margin-right: 8px;
    }

    .discount-badge {
        background: #ff4444;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 12px;
        margin-left: 8px;
    }

    /* 降价提醒 */
    .price-alert {
        background: linear-gradient(135deg, #ff6b6b, #ff8e8e);
        color: white;
        padding: 12px 16px;
        border-radius: 10px;
        margin: 10px 0;
        animation: slideIn 0.5s ease-out;
    }

    @keyframes slideIn {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    /* 无结果提示 */
    .no-results {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin: 20px 0;
    }

    /* 详情页样式 */
    .detail-container {
        background: white;
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 20px 0;
    }

    .specs-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }

    .specs-table td {
        padding: 10px;
        border-bottom: 1px solid #f0f0f0;
    }

    .specs-table td:first-child {
        font-weight: bold;
        color: #666;
        width: 30%;
    }

    /* 评价样式 */
    .review-item {
        border-bottom: 1px solid #f0f0f0;
        padding: 15px 0;
    }

    .review-header {
        display: flex;
        justify-content: between;
        align-items: center;
        margin-bottom: 8px;
    }

    .review-user {
        font-weight: bold;
        color: #333;
    }

    .review-rating {
        color: #ffa500;
    }

    .review-date {
        color: #999;
        font-size: 12px;
    }

    .review-comment {
        color: #666;
        line-height: 1.5;
    }

    /* 店铺信息 */
    .store-info {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
    }

    /* 集合表达式样式 */
    .set-expression {
        background: #e3f2fd;
        border: 2px solid #2196f3;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        text-align: center;
    }

    .set-operation {
        font-weight: bold;
        color: #2196f3;
    }

    .set-name {
        font-weight: bold;
        color: #ff5722;
    }
    </style>
    """, unsafe_allow_html=True)


def auto_carousel():
    """自动轮播逻辑"""
    current_time = time.time()

    # 更新倒计时
    time_passed = current_time - st.session_state.last_carousel_update
    st.session_state.carousel_countdown = max(0, 3 - int(time_passed))

    # 检查是否需要切换轮播图
    if (st.session_state.carousel_running and
            time_passed >= 3):  # 3秒切换一次
        st.session_state.current_slide = (st.session_state.current_slide + 1) % 3
        st.session_state.last_carousel_update = current_time
        st.session_state.carousel_countdown = 3
        st.rerun()


def create_carousel():
    """纯手动轮播图，不自动切换"""
    imgs = [
        "https://images.unsplash.com/photo-1607082350899-7e105aa886ae?w=1200",
        "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=1200",
        "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=1200"
    ]
    caps = [
        "🔥 限时特惠 · 全场低至 5 折",
        "🎁 新用户专享 · 注册立减 200 元",
        "🚚 今夜下单 · 明日送达"
    ]
    current_slide = st.session_state.current_slide

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        # 在 create_carousel() 函数里
        st.image(imgs[current_slide], use_container_width=True)
        st.markdown(f"<center><h4>{caps[current_slide]}</h4></center>", unsafe_allow_html=True)

        # 左右切换
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("◀ 上一个", use_container_width=True):
                st.session_state.current_slide = (current_slide - 1) % 3
        with c3:
            if st.button("下一个 ▶", use_container_width=True):
                st.session_state.current_slide = (current_slide + 1) % 3
        with c2:
            st.markdown(f"<center>{current_slide + 1} / 3</center>", unsafe_allow_html=True)


def show_price_alerts():
    """显示降价提醒"""
    if st.session_state.price_alerts:
        st.markdown("### 💰 降价提醒")
        for alert in st.session_state.price_alerts[-3:]:  # 显示最近3条
            with st.container():
                st.markdown(f"""
                <div class="price-alert">
                    <strong>🎉 价格提醒！</strong><br>
                    {alert['product_name']} 已从 <span style="text-decoration: line-through;">¥{alert['old_price']}</span> 
                    降至 <span style="font-weight: bold;">¥{alert['new_price']}</span>
                    <span style="font-size: 12px; opacity: 0.9;">（立省 ¥{alert['old_price'] - alert['new_price']}）</span>
                </div>
                """, unsafe_allow_html=True)


def create_product_carousel(product):
    """创建商品详情页轮播图"""
    current_slide = st.session_state.product_detail_slide

    # 轮播图主体
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(product['carousel_images'][current_slide], use_container_width=True)

        # 轮播控制
        col_prev, col_dots, col_next = st.columns([1, 2, 1])

        with col_prev:
            if st.button("◀ 上一张", key="product_prev"):
                st.session_state.product_detail_slide = (current_slide - 1) % len(product['carousel_images'])
                st.rerun()

        with col_dots:
            dots_html = "<div style='text-align: center; margin: 10px 0;'>"
            for i in range(len(product['carousel_images'])):
                dot_class = "carousel-dot active" if i == current_slide else "carousel-dot"
                dots_html += f"<span class='{dot_class}' onclick='setProductSlide({i})' style='margin: 0 5px;'></span>"
            dots_html += "</div>"
            st.markdown(dots_html, unsafe_allow_html=True)

        with col_next:
            if st.button("下一张 ▶", key="product_next"):
                st.session_state.product_detail_slide = (current_slide + 1) % len(product['carousel_images'])
                st.rerun()


def product_detail_page(product):
    """商品详情页 - 模仿淘宝布局"""
    st.button("← 返回首页", on_click=lambda: setattr(st.session_state, 'current_page', 'home'))

    st.markdown(f"<div class='detail-container'>", unsafe_allow_html=True)

    # 第一行：商品轮播图和基本信息
    col1, col2 = st.columns([1, 1])

    with col1:
        # 商品轮播图
        create_product_carousel(product)

    with col2:
        # 商品基本信息
        st.title(product['name'])
        st.write(f"**商品描述:** {product['description']}")

        # 价格和销量信息
        st.subheader("💰 价格信息")
        col_price1, col_price2, col_price3 = st.columns(3)
        with col_price1:
            st.metric("当前价格", f"¥{product['price']}")
        with col_price2:
            if product.get('original_price', 0) > product['price']:
                discount = int((1 - product['price'] / product['original_price']) * 100)
                st.metric("优惠幅度", f"{discount}%", delta=f"-{discount}%")
        with col_price3:
            st.metric("累计销量", f"{product['sales']}+")

        # 评分和评价
        st.subheader("⭐ 商品评价")
        col_rating1, col_rating2, col_rating3 = st.columns(3)
        with col_rating1:
            st.metric("综合评分", product['rating'])
        with col_rating2:
            st.metric("评价人数", f"{product['reviews']}+")
        with col_rating3:
            st.metric("好评率", f"{int(product['rating'] * 20)}%")

        # 购买操作
        st.subheader("🛒 立即购买")
        col_buy1, col_buy2 = st.columns(2)
        with col_buy1:
            if st.button("加入购物车", use_container_width=True, type="secondary", key="add_cart"):
                st.success("✅ 已加入购物车！")
        with col_buy2:
            if st.button("立即购买", use_container_width=True, type="primary", key="buy_now"):
                st.success("🎉 购买成功！感谢您的购买！")

    # 店铺信息
    st.markdown("---")
    st.subheader("🏪 店铺信息")
    with st.container():
        st.markdown(f"""
        <div class="store-info">
            <h4>{product['store_name']}</h4>
            <p>店铺评分: ⭐{product['store_rating']} | 商品描述相符: ⭐{product['rating']} | 物流服务: ⭐{random.uniform(4.5, 5.0):.1f}</p>
            <p>📍 店铺地址: 北京市朝阳区xxx街道</p>
            <p>⏰ 营业时间: 9:00-22:00</p>
        </div>
        """, unsafe_allow_html=True)

    # 商品详情图片（下滑展示）
    st.markdown("---")
    st.subheader("📸 商品详情")
    for img_url in product['product_images']:
        st.image(img_url, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # 商品规格
    st.markdown("---")
    st.subheader("📋 商品规格")
    specs_html = "<table class='specs-table'>"
    for key, value in product['specs'].items():
        specs_html += f"<tr><td>{key}</td><td>{value}</td></tr>"
    specs_html += "</table>"
    st.markdown(specs_html, unsafe_allow_html=True)

    # 商品评价
    st.markdown("---")
    st.subheader("💬 商品评价")

    # 评价统计
    col_review1, col_review2, col_review3, col_review4 = st.columns(4)
    with col_review1:
        st.metric("全部评价", product['reviews'])
    with col_review2:
        st.metric("好评", f"{int(product['reviews'] * 0.8)}+")
    with col_review3:
        st.metric("中评", f"{int(product['reviews'] * 0.15)}+")
    with col_review4:
        st.metric("差评", f"{int(product['reviews'] * 0.05)}+")

    # 评价列表
    for review in product['reviews_list']:
        with st.container():
            st.markdown(f"""
            <div class="review-item">
                <div class="review-header">
                    <span class="review-user">{review['user']}</span>
                    <span class="review-rating">{"⭐" * review['rating']}</span>
                    <span class="review-date">{review['date']}</span>
                </div>
                <div class="review-comment">{review['comment']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# 修复的筛选函数
def apply_filters():
    """应用筛选条件 - 修复版本"""
    filtered_products = []

    # 应用所有筛选条件（AND逻辑）
    for product in products:
        match = True

        # 搜索筛选
        if st.session_state.search_input and st.session_state.search_input.lower() not in product['name'].lower():
            match = False

        # 类别筛选
        if st.session_state.category_select != "全部" and product['category'] != st.session_state.category_select:
            match = False

        # 价格筛选
        if st.session_state.price_select != "全部":
            if st.session_state.price_select == "0-100元" and product['price'] > 100:
                match = False
            elif st.session_state.price_select == "100-500元" and (product['price'] <= 100 or product['price'] > 500):
                match = False
            elif st.session_state.price_select == "500-1000元" and (product['price'] <= 500 or product['price'] > 1000):
                match = False
            elif st.session_state.price_select == "1000元以上" and product['price'] <= 1000:
                match = False

        # 包邮筛选
        if st.session_state.shipping_select != "全部":
            if st.session_state.shipping_select == "包邮" and not product['free_shipping']:
                match = False
            elif st.session_state.shipping_select == "不包邮" and product['free_shipping']:
                match = False

        if match:
            filtered_products.append(product)

    st.session_state.filtered_products = filtered_products
    st.session_state.show_no_results = len(filtered_products) == 0

    # 生成集合表达式
    generate_set_expression()


def generate_set_expression():
    """生成集合运算表达式"""
    expressions = []

    # 全集合
    if (st.session_state.category_select == "全部" and
            st.session_state.price_select == "全部" and
            st.session_state.shipping_select == "全部" and
            not st.session_state.search_input):
        st.session_state.set_expression = "S (全商品集合)"
        return

    # 类别集合
    if st.session_state.category_select != "全部":
        expressions.append(f"A_{st.session_state.category_select}")

    # 价格集合
    if st.session_state.price_select != "全部":
        expressions.append(f"B_{st.session_state.price_select}")

    # 配送集合
    if st.session_state.shipping_select != "全部":
        expressions.append(f"C_{st.session_state.shipping_select}")

    # 搜索条件
    if st.session_state.search_input:
        expressions.append(f"搜索:'{st.session_state.search_input}'")

    if expressions:
        set_expression = " ∩ ".join(expressions)
    else:
        set_expression = "S"

    # 添加集合定义
    definition = "其中：\nS = 全商品集合\n"
    definition += "A_家电 = 家电商品集合\nA_服装 = 服装商品集合\nA_食品 = 食品商品集合\n"
    definition += "B_0-100元 = 0-100元商品集合\nB_100-500元 = 100-500元商品集合\nB_500-1000元 = 500-1000元商品集合\nB_1000元以上 = 1000元以上商品集合\n"
    definition += "C_包邮 = 包邮商品集合\nC_不包邮 = 不包邮商品集合"

    st.session_state.set_expression = f"{set_expression}\n\n{definition}"

def check_recent_view_price_drop():
    """
    返回首页时检查：最近一次浏览的商品是否降价
    """
    if not st.session_state.view_history:
        return False

    last = st.session_state.view_history[-1]
    old_price = last.get('view_price')      # 可能为 None
    if old_price is None:                   # 第一次无参考价，直接跳过
        return False

    pid = last['product_id']
    product = next((p for p in products if p['id'] == pid), None)
    if not product:
        return False

    new_price = product['price']
    if new_price >= old_price:
        return False

    # 确实降价了 -> 生成提醒
    alert = {
        'product_name': product['name'],
        'old_price': old_price,
        'new_price': new_price,
        'time': datetime.now().strftime("%H:%M")
    }
    st.session_state.price_alerts.append(alert)
    # 更新记录，避免重复提醒
    last['view_price'] = new_price
    return True

# 将下面的 home_page() 函数整个替换掉原来的即可
def home_page():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    # === 返回首页时：检查刚刚浏览的商品是否降价 ===
    if st.session_state.selected_product is not None:
        check_recent_view_price_drop()
        # 清除标记，避免下次重复检查
        st.session_state.selected_product = None

    # 降价提醒（含刚刚检测到的）
    show_price_alerts()
    """首页"""


    # 标题
    st.markdown("""
    <div style="text-align: center; padding: 30px 0;">
        <h1 style="color: #333; margin-bottom: 10px;">🛒 电商商品筛选系统</h1>
        <p style="color: #666; font-size: 1.2rem;">基于集合运算的多条件商品筛选</p>
    </div>
    """, unsafe_allow_html=True)

    # 降价提醒
    show_price_alerts()

    # 轮播图
    st.markdown("### 🎯 热门推荐")
    create_carousel()



    # 搜索和筛选
    st.markdown("### 🔍 商品筛选")
    col1, col2, col3, col4 = st.columns(4)

    # ---------- 统一 on_change 回调 ----------
    def _update_filter(key, widget_key):
        """把 widget 当前值同步到 session 并立即筛选"""
        st.session_state[key] = st.session_state[widget_key]
        apply_filters()

    with col1:
        st.text_input(
            "搜索商品",
            value=st.session_state.search_input,
            placeholder="输入商品名称...",
            key="search_input_display",
            on_change=_update_filter,
            args=("search_input", "search_input_display")
        )

    with col2:
        categories = ["全部", "家电", "服装", "食品"]
        st.selectbox(
            "商品类别",
            categories,
            index=categories.index(st.session_state.category_select),
            key="category_select_display",
            on_change=_update_filter,
            args=("category_select", "category_select_display")
        )

    with col3:
        price_ranges = ["全部", "0-100元", "100-500元", "500-1000元", "1000元以上"]
        st.selectbox(
            "价格区间",
            price_ranges,
            index=price_ranges.index(st.session_state.price_select),
            key="price_select_display",
            on_change=_update_filter,
            args=("price_select", "price_select_display")
        )

    with col4:
        shipping_options = ["全部", "包邮", "不包邮"]
        st.selectbox(
            "配送方式",
            shipping_options,
            index=shipping_options.index(st.session_state.shipping_select),
            key="shipping_select_display",
            on_change=_update_filter,
            args=("shipping_select", "shipping_select_display")
        )

    # 显示当前已选条件
    current_filters = []
    if st.session_state.search_input:
        current_filters.append(f"搜索: {st.session_state.search_input}")
    if st.session_state.category_select != "全部":
        current_filters.append(f"类别: {st.session_state.category_select}")
    if st.session_state.price_select != "全部":
        current_filters.append(f"价格: {st.session_state.price_select}")
    if st.session_state.shipping_select != "全部":
        current_filters.append(f"配送: {st.session_state.shipping_select}")
    if current_filters:
        st.info("当前筛选条件: " + " | ".join(current_filters))




    # 结果展示
    filtered_products = st.session_state.filtered_products
    if st.session_state.show_no_results:
        st.markdown("""
        <div class="no-results">
            <h3>😔 没有找到符合条件的商品</h3>
            <p>请尝试调整筛选条件，或者看看下面的推荐商品：</p>
        </div>
        """, unsafe_allow_html=True)
        filtered_products = random.sample(products, min(3, len(products)))

    # 商品网格
    st.markdown(f"### 🛍️ 筛选结果 ({len(filtered_products)} 个商品)")
    if filtered_products:
        cols = st.columns(3)
        for idx, product in enumerate(filtered_products):
            with cols[idx % 3]:
                has_discount = product.get('original_price', 0) > product['price']
                discount_amount = product['original_price'] - product['price'] if has_discount else 0
                card_html = f"""
                <div class="product-card">
                    <img src="{product['image_url']}" class="product-image" alt="{product['name']}">
                    <div class="product-name">{product['name']}</div>
                    <div class="product-price">
                        {"<span class='original-price'>¥" + str(product['original_price']) + "</span>" if has_discount else ""}
                        ¥{product['price']}
                        {"<span class='discount-badge'>立省¥" + str(discount_amount) + "</span>" if has_discount else ""}
                    </div>
                    <div style="color: #666; font-size: 12px; margin: 3px 0;">{product['category']} • ⭐{product['rating']}</div>
                    {"<div style='background: #e8f5e8; color: #2e7d32; padding: 2px 8px; border-radius: 12px; font-size: 11px; display: inline-block; margin-top: 5px;'>✅ 包邮</div>" if product['free_shipping'] else "<div style='background: #ffebee; color: #c62828; padding: 2px 8px; border-radius: 12px; font-size: 11px; display: inline-block; margin-top: 5px;'>❌ 不包邮</div>"}
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                if st.button("查看详情", key=f"btn_{product['id']}", use_container_width=True):
                    st.session_state.selected_product = product
                    st.session_state.current_page = 'detail'
                    st.session_state.product_detail_slide = 0
                    st.session_state.view_history.append({
                        'product_id': product['id'],
                        'product_name': product['name'],
                        'view_time': datetime.now().strftime("%H:%M:%S"),
                        'view_price': product['price']  # ← 新增
                    })
                    st.session_state.view_history.append({
                        'product_id': product['id'],
                        'product_name': product['name'],
                        'view_time': datetime.now().strftime("%H:%M:%S")
                    })
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def simulate_price_drop():
    """模拟降价功能"""
    if random.random() < 0.2:  # 20%概率触发降价
        product = random.choice(products)
        if product['price'] > 50:
            old_price = product['price']
            new_price = max(50, old_price - random.randint(10, 100))

            if new_price < old_price:
                product['price'] = new_price
                alert = {
                    'product_name': product['name'],
                    'old_price': old_price,
                    'new_price': new_price,
                    'time': datetime.now().strftime("%H:%M")
                }
                st.session_state.price_alerts.append(alert)


def main():
    setup_css()

    # 初始化筛选结果
    if not st.session_state.filtered_products:
        st.session_state.filtered_products = products




    # 页面路由
    if st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'detail' and st.session_state.selected_product:
        product_detail_page(st.session_state.selected_product)


if __name__ == "__main__":
    main()