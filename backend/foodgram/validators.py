from django.core.validators import RegexValidator, MinValueValidator


validate_time = MinValueValidator(
    limit_value=1,
    message='Укажите значение 1 и более',
)


validate_name = RegexValidator(
    r'^[а-яА-ЯёЁa-zA-Z]*$',
    ('Поле должно содержать только буквы кириллицы/латиницы'),
)


validate_color = RegexValidator(
    regex=r'^#([A-Fa-f0-9]{3,6})$',
    message='Укажите корректный HEX цвет',
    code='invalid_HEX_color',
)
