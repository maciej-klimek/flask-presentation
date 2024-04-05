from flask import Flask, render_template

posts_list = [
    {
        'title': 'Szampan',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla fermentum ex sit amet aliquet suscipit. Sed ac ligula nec est commodo convallis.'
    },
    {
        'title': 'Post 2: Dolor Sit Amet',
        'content': 'Donec placerat, elit a consequat vehicula, eros dolor dapibus purus, id facilisis ligula neque eget leo. Vivamus lacinia eleifend ante, id tincidunt eros efficitur vel.'
    },
    {
        'title': 'Post 3: Consectetur Adipiscing',
        'content': 'Curabitur convallis turpis non libero pretium, vitae venenatis sapien commodo. Vestibulum at semper mauris. In scelerisque dui non finibus vulputate.'
    }
]

products_list = [
    {"name": "Janosik 7.3%", "price": 10, "stock": 5},
    {"name": "Blachotrapez", "price": 20, "stock": 4},
    {"name": "Mega rollo mieszany mieszany", "price": 15, "stock": 3},
    {"name": "Kurczak curry z mekonga", "price": 25, "stock": 0}
]

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html', name="Strona główna", posts=posts_list)

@app.route('/contact')
def contant():
    return render_template('contact.html',name="Kontakt", adress="Kalinowa 7", phone="530708858")

@app.route('/shop')
def shop():
    return render_template('shop.html',name="Sklep", products=products_list)

if __name__ == '__main__':
    app.run(debug=True)