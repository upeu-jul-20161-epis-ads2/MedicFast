# Backend Manager for Django

Módulo Backend para aplicaciones web SaaS seguras escritas (update) en Django 1.9.4 y con la elegancia de Bootstrap 3.

Por medio de este Backend podrás gestionar las diferentes partes del sistema: usuarios, perfiles, recursos, permisos, módulos, planes SaaS, menús, asociaciones, empresas, sedes, logs, seguridad, internacionalización y mucho más!.

Ahora, cuando inicias un proyecto comenzarás directamente a atender(implementar) los requisitos de tu nuevo sistema, ya que Backengo se encargó de todo el trabajo inicial repetitivo de todo proyecto de software así como de los componentes o librerías que necesitas antes de comenzar a desarrollar una aplicación web moderna y segura.



![desktop](https://github.com/submitconsulting/backengo/blob/master/media/test_images/img1.png)
![mobile](https://github.com/submitconsulting/backengo/blob/master/media/test_images/img3.png)
## Documentation


- [Diseño UML][uml]
- [Guía del desarrollador][manual]
- [Demo en línea][demo]

Usuario: `admin`

Password: `12345`

[uml]: http://backengo-model.appspot.com
[demo]: http://educaci-dns.com:8001/
[manual]: https://github.com/submitconsulting/backengo/blob/master/Backengo---Manual.docx?raw=true

## How to Get Started

1 Install python 3.5.1, for win

2 clone this repo or download .zip file

    D:\>md pydev
    D:\pydev>git clone https://github.com/submitconsulting/backengo.git

3 install all the necessary packages (best done inside of a virtual environment)

    D:\pydev>cd backengo
    D:\pydev\backengo>virtualenv ve_backengo
    D:\pydev\backengo>ve_backengo\Scripts\activate

    (ve_backengo) D:\pydev\backengo>pip install -r requirements.txt

    (ve_backengo) D:\pydev\backengo>manage.py runserver

 para instalar pip revise [Guía del desarrollador][manual]

4 run the app

    (ve_backengo) D:\pydev\backengo>manage.py runserver
    ó
    (ve_backengo) D:\pydev\backengo>python manage.py runserver

5 Estructura de carpeta

```
D:\>
└── pydev
    └── backengo
        └── backengo
        └── ve_backengo

```

ó

```
D:
└── pydev
    ├── backengo
    │   └── backengo
    │   └── manage.py
    └── ve_backengo
        └── Scripts 
            └── activate.bat   
```

## Dev commands:

    (veb) D:\dev\apps\backengo-root\backengo>python -m django-admin makemessages -l es_PE 

    (veb) D:\dev\apps\backengo-root\backengo>python -m django-admin makemessages -d djangojs -l es_PE --ignore=admin

    (veb) D:\dev\apps\backengo-root\backengo>python -m django-admin compilemessages

    (veb) D:\dev\apps\backengo-root\backengo>python manage.py makemigrations params
    (veb) D:\dev\apps\backengo-root\backengo>python manage.py migrate params

  For makemessages or compilemessages, configure gettext-utils and add Path 
  >D:\dev\apps\backengo-root\veb\Scripts;C:\gettext-utils\gettext-tools-0.17\bin;
  
  View https://docs.djangoproject.com/en/dev/topics/i18n/translation/#gettext-on-windows 

Backup/load database
-------------------
See in the settings.py setting for FIXTURE_DIRS

    $python manage.py dumpdata > fixtures/ini_data.json
    $python manage.py loaddata ini_data


Clean/restore database
-------------------
Run the following command:

    $python manage.py flush


exec

  >delete from django_content_type;

  >delete from auth_permission;

 
And run the following command:

    $ manage.py loaddata ini_data

    ó

    $ manage.py loaddata fixtures\ini_data.json


3rd-Party Apps/Libraries/Plugins
--------------------------------

This app uses the following:

* Twitter Bootstrap 3 (http://getbootstrap.com)
* Django Crispy Forms (http://django-crispy-forms.readthedocs.org/en/latest)



## Author

- Angel Sullon Macalupu (asullom@gmail.com)

## Contributors

See https://github.com/submitconsulting/backengo/contributors

## Important

* Todas las vistas están basadas en clases (class-based views)
* `django_migrations` es nuevo desde django 1.7.x 


