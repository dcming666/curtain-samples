import os
import sys
import random
from datetime import datetime, timedelta
from app import app, db, Category, Curtain

# 确保在应用上下文中运行
with app.app_context():
    # 首先创建所有数据库表
    db.create_all()
    
    # 检查是否已有分类数据
    categories = Category.query.all()
    
    # 如果没有分类，创建一些基础分类
    if not categories:
        print("创建窗帘分类...")
        categories_data = [
            {"name": "现代简约", "description": "简洁大方的现代风格窗帘，适合现代家居装饰"},
            {"name": "欧式奢华", "description": "华丽精致的欧式风格窗帘，彰显高贵与典雅"},
            {"name": "田园风光", "description": "自然清新的田园风格窗帘，营造温馨舒适的氛围"},
            {"name": "北欧风格", "description": "简约时尚的北欧风格窗帘，展现现代与自然的完美结合"},
            {"name": "中式古典", "description": "传统韵味的中式风格窗帘，体现东方美学与文化底蕴"}
        ]
        
        for cat_data in categories_data:
            category = Category(name=cat_data["name"], description=cat_data["description"])
            db.session.add(category)
        
        db.session.commit()
        categories = Category.query.all()
        print(f"成功创建 {len(categories)} 个窗帘分类")
    
    # 检查是否已有窗帘样本数据
    curtains_count = Curtain.query.count()
    if curtains_count >= 50:
        print(f"数据库中已有 {curtains_count} 条窗帘样本数据，无需添加")
        sys.exit(0)
    
    # 准备生成窗帘样本数据
    print("开始生成窗帘样本数据...")
    
    # 窗帘名称前缀和后缀，用于组合生成多样化的名称
    name_prefixes = ["优雅", "高贵", "典雅", "时尚", "简约", "奢华", "清新", "浪漫", "温馨", "舒适"]
    name_suffixes = ["遮光窗帘", "纱帘", "布艺窗帘", "卷帘", "百叶帘", "罗马帘", "蕾丝窗帘", "绒布窗帘", "提花窗帘", "印花窗帘"]
    
    # 材质选项
    materials = ["棉麻混纺", "纯棉", "涤纶", "丝绒", "亚麻", "真丝", "人造丝", "聚酯纤维", "尼龙", "羊毛混纺"]
    
    # 宽度选项
    widths = ["1.5米", "2.0米", "2.2米", "2.5米", "2.8米", "3.0米", "3.5米", "4.0米", "定制宽度"]
    
    # 图案选项
    patterns = ["纯色", "条纹", "格子", "花卉", "抽象", "几何", "动物", "风景", "水墨", "民族风"]
    
    # 风格选项
    styles = ["现代简约", "欧式古典", "美式乡村", "北欧风格", "中式传统", "地中海风格", "日式和风", "工业风", "波西米亚", "轻奢风格"]
    
    # 特点选项
    features_list = [
        "防水", "防霉", "隔热", "隔音", "防紫外线", "易清洗", "环保材质", "抗皱", "阻燃", "抗静电",
        "遮光率高", "透气性好", "手感柔软", "色牢度高", "不易褪色", "抗污渍", "防尘", "抗菌", "防过敏", "可机洗"
    ]
    
    # 描述模板
    description_templates = [
        "这款{style}风格的{name}采用{material}材质，{width}宽度，{pattern}图案设计，具有{features}等特点，是您家居装饰的理想选择。",
        "{name}以其{pattern}图案和{style}风格脱颖而出，{material}材质确保了其耐用性和舒适度，{width}的宽度适合大多数窗户，特别适合注重{features}的家庭。",
        "精选{material}面料打造的{name}，展现{style}风格的独特魅力，{pattern}图案设计时尚前卫，{width}规格满足多种需求，{features}等特性使其成为市场上的热门选择。",
        "{style}设计理念的{name}，采用高品质{material}制作，{width}尺寸灵活多变，{pattern}图案独具匠心，{features}等多重功能满足您的各种需求。",
        "这款{name}融合了{style}的设计元素，{material}材质触感舒适，{pattern}图案精致典雅，{width}宽度选择多样，具有{features}等实用功能，为您的窗户增添独特魅力。"
    ]
    
    # 生成50条窗帘样本数据
    curtains_to_add = 50 - curtains_count
    curtains_data = []
    
    for i in range(curtains_to_add):
        # 随机选择分类
        category = random.choice(categories)
        
        # 生成名称
        name = f"{random.choice(name_prefixes)}{random.choice(name_suffixes)}"
        
        # 随机选择属性
        material = random.choice(materials)
        width = random.choice(widths)
        pattern = random.choice(patterns)
        style = random.choice(styles)
        
        # 随机选择2-4个特点组合
        num_features = random.randint(2, 4)
        selected_features = random.sample(features_list, num_features)
        features = "、".join(selected_features)
        
        # 生成描述
        description_template = random.choice(description_templates)
        description = description_template.format(
            name=name,
            style=style,
            material=material,
            width=width,
            pattern=pattern,
            features=features
        )
        
        # 随机价格 (100-2000元)
        price = round(random.uniform(100, 2000), 2)
        
        # 随机库存状态 (80%有库存)
        in_stock = random.random() < 0.8
        
        # 随机新品状态 (20%为新品)
        is_new = random.random() < 0.2
        
        # 创建窗帘样本对象
        curtain = Curtain(
            name=name,
            description=description,
            price=price,
            material=material,
            width=width,
            pattern=pattern,
            style=style,
            features=features,
            in_stock=in_stock,
            is_new=is_new,
            category_id=category.id
        )
        
        db.session.add(curtain)
        curtains_data.append({
            "name": name,
            "category": category.name,
            "price": price,
            "in_stock": "有库存" if in_stock else "缺货",
            "is_new": "新品" if is_new else "常规"
        })
    
    # 提交到数据库
    db.session.commit()
    
    print(f"成功添加 {len(curtains_data)} 条窗帘样本数据")
    print("\n添加的窗帘样本概览:")
    for i, curtain in enumerate(curtains_data, 1):
        print(f"{i}. {curtain['name']} - {curtain['category']} - ¥{curtain['price']} - {curtain['in_stock']} - {curtain['is_new']}")