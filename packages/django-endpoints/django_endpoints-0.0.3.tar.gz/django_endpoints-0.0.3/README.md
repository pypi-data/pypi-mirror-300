# Django Endpoints

**Django Endpoints** is a small Django application that 
displays your project's URLs, grouping them by
applications. 
> Sometimes I use this in different projects, so I decided to put it on pypi

## Installation
```bash
pip install django-endpoints
```

## Settings

* ### Add the application to the project.
    ```python
    INSTALLED_APPS = [
        #...
        'endpoints',
    ]
    ```
* ### In `settings.py` set the params
    ```python
    # required * URL to which unauthenticated or non-staff users will be redirected (is_staff=False).
    EP_NOT_AUTH_REDIRECT_URL = '/admin/login/?next=/endpoints/'
    
    # A tuple of application names that you want to exclude from the list of URLs to display.
    EP_EXCLUDED_APPS = (
        'logui',
        'swagger',
        'rest_framework',
    )
  
    # Section with custom links
    EP_CUSTOM_LINKS = [
        {'name': 'Logs', 'url': 'https://xxx.xxx/logs/'},
        {'name': 'Nginx', 'url': 'http://42.33.125.119:81/'},
        {'name': 'Swagger', 'url': 'https://xxx.xxx/swagger/'},
        {'name': 'Minio', 'url': 'https://minio.xxx.xxx/'},
        {'name': 'Pg Admin', 'url': 'https://pgadmin.xxx.xxx/'},
        {'name': 'Flower', 'url': 'https://flower.xxx.xxx/'},
    ]
    ```
* ### Add routes

    Only `is_staff` have access.
    ```python
    from django.urls import path, include
  
    urlpatterns = [
        #...
        path('endpoints/', include('endpoints.urls')),
    ]
    ```
* ### Open https://localhost:8000/endpoints/