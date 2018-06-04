# Unter 
[![Build Status](https://travis-ci.org/EverythingWorks/Unter.svg?branch=master)](https://travis-ci.org/EverythingWorks/Unter)
[![Coverage Status](https://coveralls.io/repos/github/EverythingWorks/Unter/badge.svg)](https://coveralls.io/github/EverythingWorks/Unter)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/EverythingWorks/Unter/blob/master/LICENSE)
[![Website](https://img.shields.io/website-up-down-green-red/http/shields.io.svg?label=Website)](http://unter.pythonanywhere.com/)

### Prerequisites

Before installing, fulfil following requirements (you can install these packages using `pip install -r requirements` too)

* [Python 3.5.2](https://www.python.org/)      
* [Django 2.0.4](https://www.djangoproject.com/)           
* [django-leaflet 0.23.0](https://pypi.org/project/django-leaflet/)         
* [geographiclib 1.49](https://pypi.org/project/geographiclib/)     
* [geopy 1.14.0](https://pypi.org/project/geopy/)       
* [pytz 2018.4](https://pypi.org/project/pytz/)       


### Installing
Clone this repository and go  to  selected directory. Now you just need to type:
```
pip install -r requirements
python manage.py migrate
python manage.py runserver
```
App will work on port `8000` of localhost.


## Authors
* [Daniel Piskorski](https://github.com/danpisq)

* [Dorian Kossowski](https://github.com/DorianKossowski)

* [Aleksandra Poręba](https://github.com/karmazynow-a)

* [Grzegorz Podsiadło](https://github.com/arorias)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
