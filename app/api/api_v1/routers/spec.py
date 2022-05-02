from fastapi import APIRouter

router = APIRouter(
    prefix="/specs",
    tags=["specs"]
)


# •	/schemas/upload/ - загрузка схемы
# •	/schemas/{id}/update/ - обновление схемы
# •	/schemas/{id}/delete/ - удаление схемы
# •	/schemas/{id}/deprecated/ - пометка схемы устаревшей ???
# •	/schemas/{id}/ - просмотр схемы по id
# •	/schemas/ - просмотр всех схем
