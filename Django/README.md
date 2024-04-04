Django/
│ 
├── DjangoProject/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│    
├── Administration/
│   ├── migrations/
│   ├── templates/
│   │   ├── administration/
│   │   └── views/
│   │       ├── views.py
│   │       └── login.py
│   ├──  models.py
│   ├──  urls.py
│   ├──  forms.py
│   ├──  backends.py
│   ├──  apps.py
│   ├──  admin.py
│   └──  test.py
│    
├── Functionalities/
│   ├── migrations/
│   ├── templates/
│   │   └── functionalities/
│   │       ├── historique_page.html
│   │       ├── nouveautes_page.html
│   │       ├── prediction_page.html
│   │       └── recettes_page.html
│   ├──  views.py
│   ├──  models.py
│   ├──  urls.py
│   ├──  forms.py
│   ├──  apps.py
│   ├──  admin.py
│   └──  test.py
│    
├── Main/
│   ├── migrations/
│   ├── templates/
│   │   └── main/
│   │       └── home_page.html
│   ├── views.py
│   ├──  models.py
│   ├──  urls.py
│   ├──  forms.py
│   ├──  apps.py
│   ├──  admin.py
│   └──  test.py
│
├── venv/
│       └── (environnement virtuel Python)
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   ├── home.css
│   │   ├── header.css
│   │   └── footer.css
│   ├── js/
│   │   ├── style.js
│   │   └── header.js
│   └── img/
│       ├── logo.png
│       └── user.jpeg
│
├── templates/
│   ├── includes/
│   │   ├── header.html
│   │   └── footer.html
│   ├── registration/
│   │   ├── login.html
│   │   └── signup.html
│   └── base.html
│
├── theme/ (tailwinds themes)
│   ├── static_src/
│   ├── tempaltes/
│   ├── __init__.py
│   └── apps.py
│
├── .env
│
├── manage.py
│
└── README.md


python manage.py tailwind install