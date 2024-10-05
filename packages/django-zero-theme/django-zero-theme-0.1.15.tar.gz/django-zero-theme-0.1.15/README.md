
# Django Zero Theme

## Project Status

This project is being actively maintained, though with a reduced feature set, we are looking for contributors to help
maintain and improve the project, please get in touch if you would like to help.

Help needed with:

- Triaging issues
- Frontend fixes and UI improvements
- Testing
- Documentation

Pull requests are welcome, though ive been pre-occupied with other projects lately, so have not been able to review
them as quickly as I would like, but im trying to get through them all now, hopefully with some outside help.

## Installation

```bash
pip install django-zero-theme
```

## Configuration

```python
INSTALLED_APPS = (
    "zero_theme",
    "django.contrib.admin",
    # ...
)
```

If you want to the better performance, need to enable the middleware. You must configure middleware `settings` correctly:
```python
MIDDLEWARE = [
    # ...
    "zero_theme.middleware.ZeroMiddleware",
]
```

## Create A Custom Widget
> Documentation is coming soon

## Enable Export Import Features
> Documentation is coming soon

~Thank You