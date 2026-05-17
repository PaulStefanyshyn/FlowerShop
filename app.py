from flask import Flask, render_template, request, redirect, session, jsonify

from config import Config
from database.db import db
from models import Client, Flower, Image
from crud import (
    create_client,
    get_all_clients
)
import uuid
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask import url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os 

from PIL import Image as PILImage


app = Flask(__name__)

app.secret_key = "your-secret-key"
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'QWEASD24'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)



#____________________________________ ADMIN ______________________________________________# 


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


#____ PAGES ____#
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin_index'))
        flash('IdiNaher')
    return render_template('admin/login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))






@app.route('/admin')
@login_required
def admin_index():
    flowers = Flower.query.order_by(Flower.id.desc()).all()
    return render_template('admin/index.html', flowers=flowers)




@app.route('/admin/flower/add', methods=['GET', 'POST'])
@login_required
def add_flower():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form.get('price', 0, type=int)
        tags = request.form.get('tags', '')
        description = request.form.get('description', '')
        
        flower = Flower(name=name, price=price, tags=tags, description=description)
        db.session.add(flower)
        db.session.flush()
        

        files = request.files.getlist('images')
        for file in files:
            if file and allowed_file(file.filename):
                img = PILImage.open(file)
                img.thumbnail((1200, 1200))
                filename = f"{uuid.uuid4().hex}.webp"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                img.save(filepath, "WEBP", quality=85, optimize=True)
                img_path = f"uploads/{filename}"
                image = Image(imgPath=img_path, flower_id=flower.id)
                db.session.add(image)
        
        db.session.commit()
        flash('superduper)', 'success')
        return redirect(url_for('admin_index'))
    return render_template('admin/add_flower.html')





@app.route('/admin/flower/edit/<int:flower_id>', methods=['GET', 'POST'])
@login_required
def edit_flower(flower_id):
    flower = Flower.query.get_or_404(flower_id)
    if request.method == 'POST':
        flower.name = request.form['name']
        flower.price = request.form.get('price', 0, type=int)
        flower.tags = request.form.get('tags', '')
        flower.description = request.form.get('description', '')
        
        files = request.files.getlist('new_images')
        for file in files:
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"{uuid.uuid4().hex}.{ext}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                img_path = f"uploads/{filename}"
                image = Image(imgPath=img_path, flower_id=flower.id)
                db.session.add(image)
        
        db.session.commit()
        flash('SuperDupeeer))', 'success')
        return redirect(url_for('admin_index'))
    return render_template('admin/edit_flower.html', flower=flower)

@app.route('/admin/image/delete/<int:image_id>')
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    flower_id = image.flower_id
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(image.imgPath))
    if os.path.exists(filepath):
        os.remove(filepath)
    db.session.delete(image)
    db.session.commit()
    flash('DobreYe)', 'success')
    return redirect(url_for('edit_flower', flower_id=flower_id))


@app.route('/admin/flower/delete/<int:flower_id>')
@login_required
def delete_flower(flower_id):
    flower = Flower.query.get_or_404(flower_id)
    for image in flower.images:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(image.imgPath))
        if os.path.exists(filepath):
            os.remove(filepath)
    db.session.delete(flower)
    db.session.commit()
    flash('Faino))', 'success')
    return redirect(url_for('admin_index'))





@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

















@app.route("/")
def index():
    bouquets = Flower.query.all()
    data = []
    print(bouquets)
    print(type(bouquets))
    for i in bouquets:
        img = Image.query.filter_by(flower_id=i.id).first()
        
        data.append({
            'name' : i.name,
            'tags' : i.tags.split(', ') if i.tags else [],
            'photo' : img.imgPath if img else None,
            'price' : i.price,
            'description' : i.description
        })
        
    print(data)

    return render_template(
        "home.html",
        data=data
    )


@app.route("/add", methods=["POST"])
def add_client():
    name = request.form.get("name")
    number = request.form.get("number")
    bouquet = request.form.get("bouquet")

    create_client(name, number, bouquet)

    return redirect("/")


@app.route("/save-data", methods=["POST"])
def save_data():
    data = request.get_json()

    session["product"] = {
        "name": data.get("name"),
        "price": data.get("price"),
        "count": data.get("count"),
        "img": data.get("img"),
        "tags": data.get("tags")
    }

    return jsonify({"success": True})

@app.route("/save-order", methods=["POST"])
def save_order():
    data = request.get_json()

    session["product"] = {
        "name": data.get("name"),
        "price": data.get("price"),
        "count": data.get("count"),
        "user": data.get("user"),
        "phone": data.get("phone")
    }

    return jsonify({"success": True})


@app.route("/bouquets")
def bouquets():
    product = session.get("product")

    if not product:
        return "No product in session", 400

    flower = Flower.query.filter_by(name=product["name"]).first()

    if not flower:
        return "Flower not found", 404

    images = Image.query.filter_by(flower_id=flower.id).all()

    product["img"] = [img.imgPath for img in images]

    return render_template("bouquets.html", product=product)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if Admin.query.count() == 0:
            admin = Admin(username="KurvaBober")
            admin.set_password("NeoPass15243")
            db.session.add(admin)
            db.session.commit()
    app.run(
        debug=True
    )