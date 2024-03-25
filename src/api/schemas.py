from drf_spectacular.utils import OpenApiExample, extend_schema

from api.constants import CARGO_RETRIEVE_EXAMPLE

cargo_schema = {
    'list': extend_schema(
        summary='Получение списка грузов',
        description='Возвращает список всех грузов, с количеством '
                    'грузовиков находящихся в радиусе 450 миль.',
    ),
    'retrieve': extend_schema(
        summary='Получение груза по ID',
        description='Возвращает детальную информацию о грузе с указанным ID '
                    'со всеми грузовиками и расстоянием до них.',
        examples=[
            OpenApiExample(
                'retrieve_cargo_example',
                summary='Пример ответа на получение груза по ID',
                value=CARGO_RETRIEVE_EXAMPLE,
                response_only=True,
            )
        ]
    ),
    'create': extend_schema(
        summary='Создание нового груза',
        description='Позволяет создать новый груз. Использует почтовый индекс '
                    'для нахождения соответствующих локаций погрузки и '
                    'разгрузки.',
    ),
    'partial_update': extend_schema(
        summary='Частичное обновление груза по ID',
        description='Позволяет частично обновить данные груза с указанным ID. '
                    'Использует почтовый индекс для локаций '
                    'погрузки и разгрузки',
    ),
    'update': extend_schema(
        summary='Обновление груза по ID',
        description='Позволяет обновить данные груза с указанным ID. '
                    'Использует почтовый индекс для локаций '
                    'погрузки и разгрузки ',
    ),
    'destroy': extend_schema(
        summary='Удаление груза по ID',
        description='Удаляет груз с указанным ID.',
    )
}

locations_schema = {
    'list': extend_schema(
        summary='Получение списка локаций',
        description='Возвращает список всех локаций с пагинацией '
                    '(50 на страницу).',
    ),
    'retrieve': extend_schema(
        summary='Получение локации по ID',
        description='Возвращает информацию о локации с указанным ID.',
    ),
    'create': extend_schema(
        summary='Создание новой локации',
        description='Позволяет создать новую локацию.',
    ),
    'partial_update': extend_schema(
        summary='Частичное обновление локации по ID',
        description='Позволяет частично обновить данные локации '
                    'с указанным ID.',
    ),
    'update': extend_schema(
        summary='Обновление локации по ID',
        description='Позволяет обновить данные локации с указанным ID.',
    ),
    'destroy': extend_schema(
        summary='Удаление локации по ID',
        description='Удаляет локацию с указанным ID.',
    )
}

trucks_schema = {
    'list': extend_schema(
        summary='Получение списка грузовиков',
        description='Возвращает список всех грузов.',
    ),
    'retrieve': extend_schema(
        summary='Получение грузовика по ID',
        description='Возвращает детальную информацию о грузовике '
                    'с указанным ID',
    ),
    'create': extend_schema(
        summary='Создание нового грузовика',
        description='Позволяет создать новый грузовик. Использует '
                    'почтовый индекс для определения местоположения.',
    ),
    'partial_update': extend_schema(
        summary='Частичное обновление грузовика по ID',
        description='Позволяет частично обновить данные грузовика с '
                    'указанным ID. Использует почтовый индекс для '
                    'определения местоположения.',
    ),
    'update': extend_schema(
        summary='Обновление грузовика по ID',
        description='Позволяет обновить данные грузовика с указанным ID. '
                    'Использует почтовый индекс определения местоположения.',
    ),
    'destroy': extend_schema(
        summary='Удаление грузовика по ID',
        description='Удаляет грузовик с указанным ID.',
    )
}
