import json
from typing import Optional

import googlemaps
from asyncpg import Record

from app.core.config import get_app_settings
from app.db.errors import EntityDoesNotExist
from app.db.queries.queries import queries
from app.db.repositories.base import BaseRepository
from app.models.domain.business_hours import BusinessHours
from app.models.domain.google import Place
from app.models.domain.google import PlaceId
from app.models.domain.image import Image
from app.models.domain.social_media import SocialMedia
from app.models.domain.stores import Store
from app.models.schemas.stores import StoreListResponse

SETTINGS = get_app_settings()


class StoresRepository(BaseRepository):
    # def __init__(self, conn: Connection) -> None:
    #     super().__init__(conn)
    #     self._tags_repo = TagsRepository(conn)

    async def get_store_by_id(self, *, id: int) -> Store:
        store_row = await queries.get_store_by_id(self.connection, id=id)

        if store_row:
            return await self._get_store_from_db_record(store_row=store_row)

        raise EntityDoesNotExist(f"store with id {id} does not exist")

    async def get_store_list(
        self, *, limit: int = 100, offset: int = 0
    ) -> StoreListResponse:
        store_rows = await queries.get_store_list(self.connection, limit, offset)

        total = (
            await self._get_store_list_total_from_db_record(store_row=store_rows[0])
            if store_rows
            else 0
        )

        store_list = [
            await self._get_store_from_db_record(store_row=store_row)
            for store_row in store_rows
        ]

        return StoreListResponse(stores=store_list, total=total)

    async def _get_store_from_db_record(self, *, store_row: Record) -> Store:
        place_id = store_row["place_id"]
        place = (
            await self._get_rating_n_reviews_by_place_id_from_google(place_id=place_id)
            if place_id and SETTINGS.use_google_place_api
            else None
        )
        return Store(
            id_=store_row["id"],
            name=store_row["name"],
            phone=store_row["phone"],
            address=store_row["address"],
            rating=store_row["rating"] if place is None else place.rating,
            review_count=store_row["review_count"]
            if place is None
            else place.review_count,
            image=json.loads(store_row["image"]) if store_row["image"] else None,
            social_media=json.loads(store_row["social_media"])
            if store_row["social_media"]
            else None,
            business_hours=json.loads(store_row["business_hours"])
            if store_row["business_hours"]
            else None,
            place_id=place_id,
            status=store_row["status"],
            created_at=store_row["created_at"],
            updated_at=store_row["updated_at"],
        )

    async def _get_store_list_total_from_db_record(self, *, store_row: Record) -> int:
        return store_row["total"]

    async def create_new_store(
        self,
        *,
        name: str,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        rating: Optional[float] = None,
        review_count: Optional[int] = None,
        image: Optional[Image] = None,
        social_media: Optional[SocialMedia] = None,
        business_hours: Optional[BusinessHours] = None,
        place_id: Optional[str] = None,
        status: int,
    ) -> Store:
        new_store = Store(
            name=name,
            phone=phone,
            address=address,
            rating=rating,
            review_count=review_count,
            image=image,
            social_media=social_media,
            business_hours=business_hours,
            place_id=place_id,
            status=status,
        )

        async with self.connection.transaction():
            store_row = await queries.create_store(
                self.connection,
                name=name,
                phone=phone,
                address=address,
                rating=rating,
                review_count=review_count,
                image=json.dumps(image) if image else None,
                social_media=json.dumps(social_media) if social_media else None,
                business_hours=json.dumps(business_hours) if business_hours else None,
                place_id=place_id,
                status=status,
            )

        return new_store.copy(update=dict(store_row))

    async def update_store(
        self,
        *,
        store_in_db: Store,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        rating: Optional[float] = None,
        review_count: Optional[int] = None,
        image: Optional[Image] = None,
        social_media: Optional[SocialMedia] = None,
        business_hours: Optional[BusinessHours] = None,
        place_id: Optional[str] = None,
        status: Optional[int] = None,
    ) -> Store:
        store_in_db.name = name or store_in_db.name
        store_in_db.phone = phone or store_in_db.phone
        store_in_db.address = address or store_in_db.address
        store_in_db.rating = rating if rating is not None else store_in_db.rating
        store_in_db.review_count = (
            review_count if review_count is not None else store_in_db.review_count
        )
        store_in_db.image = image if image is not None else store_in_db.image
        store_in_db.social_media = social_media or store_in_db.social_media
        store_in_db.business_hours = business_hours or store_in_db.business_hours
        store_in_db.place_id = place_id or store_in_db.place_id
        store_in_db.status = status if status is not None else store_in_db.status

        new_image = None
        if image:
            new_image = json.dumps(store_in_db.image)
        elif store_in_db.image:
            new_image = json.dumps(store_in_db.image.__dict__)

        new_social_media = None
        if social_media:
            new_social_media = json.dumps(store_in_db.social_media)
        elif store_in_db.social_media:
            new_social_media = json.dumps(store_in_db.social_media.__dict__)

        new_business_hours = None
        if business_hours:
            new_business_hours = json.dumps(store_in_db.business_hours)
        elif store_in_db.business_hours:
            new_business_hours = json.dumps(store_in_db.business_hours.__dict__)

        async with self.connection.transaction():
            store_in_db.updated_at = await queries.update_store_by_id(
                self.connection,
                id=store_in_db.id_,
                new_name=store_in_db.phone,
                new_phone=store_in_db.phone,
                new_address=store_in_db.address,
                new_rating=store_in_db.rating,
                new_review_count=store_in_db.review_count,
                new_image=new_image,
                new_social_media=new_social_media,
                new_business_hours=new_business_hours,
                new_place_id=store_in_db.place_id,
                new_status=store_in_db.status,
            )

        return store_in_db

    async def _get_google_place_id_by_name(self, *, name: str) -> PlaceId:
        gmaps = googlemaps.Client(key=SETTINGS.google_api_key)
        g_results = gmaps.places(name)
        place_id = (
            g_results["results"][0]["place_id"]
            if "results" in g_results and "place_id" in g_results["results"][0]
            else None
        )

        return PlaceId(place_id=place_id)

    async def _get_rating_n_reviews_by_place_id_from_google(
        self, *, place_id: str
    ) -> Place:
        gmaps = googlemaps.Client(key=SETTINGS.google_api_key)
        g_result = gmaps.place(place_id=place_id)
        rating = (
            g_result["result"]["rating"]
            if "result" in g_result and "rating" in g_result["result"]
            else 0
        )
        review_count = (
            g_result["result"]["user_ratings_total"]
            if "result" in g_result and "user_ratings_total" in g_result["result"]
            else 0
        )

        return Place(rating=rating, review_count=review_count)
