from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime, timedelta

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 启用跨域资源共享

# 配置
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///curtains.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

# 配置上传文件夹
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 确保上传文件夹存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 初始化扩展
db = SQLAlchemy(app)
jwt = JWTManager(app)

# 数据模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    curtains = db.relationship('Curtain', backref='category', lazy=True)

class Curtain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=True)
    material = db.Column(db.String(100), nullable=True)
    width = db.Column(db.String(50), nullable=True)
    pattern = db.Column(db.String(100), nullable=True)
    style = db.Column(db.String(100), nullable=True)
    features = db.Column(db.Text, nullable=True)
    in_stock = db.Column(db.Boolean, default=True)
    is_new = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 辅助函数
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        # 返回可访问的URL
        return f"/api/uploads/{unique_filename}"
    return None

# 路由
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    
    if not user or not user.check_password(data.get('password')):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'is_admin': user.is_admin
        }
    })

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'is_admin': user.is_admin
    })

# 分类API
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{
        'id': category.id,
        'name': category.name,
        'description': category.description
    } for category in categories])

@app.route('/api/categories', methods=['POST'])
@jwt_required()
def create_category():
    data = request.json
    category = Category(name=data.get('name'), description=data.get('description'))
    db.session.add(category)
    db.session.commit()
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description
    }), 201

@app.route('/api/categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.json
    category.name = data.get('name', category.name)
    category.description = data.get('description', category.description)
    db.session.commit()
    return jsonify({
        'id': category.id,
        'name': category.name,
        'description': category.description
    })

@app.route('/api/categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': '分类已删除'})

@app.route('/api/categories/<int:id>/curtains', methods=['GET'])
def get_curtains_by_category(id):
    curtains = Curtain.query.filter_by(category_id=id).all()
    return jsonify([{
        'id': curtain.id,
        'name': curtain.name,
        'description': curtain.description,
        'image_url': curtain.image_url,
        'price': curtain.price,
        'material': curtain.material,
        'width': curtain.width,
        'pattern': curtain.pattern,
        'style': curtain.style,
        'features': curtain.features,
        'in_stock': curtain.in_stock,
        'is_new': curtain.is_new,
        'category_id': curtain.category_id,
        'category_name': curtain.category.name
    } for curtain in curtains])

# 窗帘样本API
@app.route('/api/curtains', methods=['GET'])
def get_curtains():
    curtains = Curtain.query.all()
    return jsonify([{
        'id': curtain.id,
        'name': curtain.name,
        'description': curtain.description,
        'image_url': curtain.image_url,
        'price': curtain.price,
        'material': curtain.material,
        'width': curtain.width,
        'pattern': curtain.pattern,
        'style': curtain.style,
        'features': curtain.features,
        'in_stock': curtain.in_stock,
        'is_new': curtain.is_new,
        'category_id': curtain.category_id,
        'category_name': curtain.category.name
    } for curtain in curtains])

@app.route('/api/curtains/<int:id>', methods=['GET'])
def get_curtain(id):
    curtain = Curtain.query.get_or_404(id)
    return jsonify({
        'id': curtain.id,
        'name': curtain.name,
        'description': curtain.description,
        'image_url': curtain.image_url,
        'price': curtain.price,
        'material': curtain.material,
        'width': curtain.width,
        'pattern': curtain.pattern,
        'style': curtain.style,
        'features': curtain.features,
        'in_stock': curtain.in_stock,
        'is_new': curtain.is_new,
        'category_id': curtain.category_id,
        'category_name': curtain.category.name
    })

# 重复的create_curtain函数已删除

# 重复的update_curtain函数已删除

@app.route('/api/curtains/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_curtain(id):
    curtain = Curtain.query.get_or_404(id)
    db.session.delete(curtain)
    db.session.commit()
    return jsonify({'message': '窗帘样本已删除'})

# 提供上传的图片
@app.route('/api/uploads/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 初始化数据库和创建管理员账户
# 在较新版本的Flask中，before_first_request已被弃用
# 我们在app.py底部添加初始化代码
if __name__ == '__main__':
    with app.app_context():
        # 初始化数据库
        db.create_all()
        
        # 创建管理员账户（如果不存在）
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

# 重复的create_curtain函数已删除

# 重复的update_curtain函数已删除

# 初始化数据库和创建管理员账户已在前面定义
# 这里是文件结尾