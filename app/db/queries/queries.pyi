"""Typings for queries generated by aiosql"""

from typing import Dict, Optional, Sequence, List

from asyncpg import Connection, Record

class UsersQueriesMixin:
    async def get_user_by_uid(self, conn: Connection, *, uid: str) -> Record: ...
    async def get_users(self, conn: Connection, limit: int, offset: int) -> Record: ...
    async def get_users_for_admin(self, conn: Connection, limit: int, offset: int) -> Record: ...
    async def get_users_by_email(self, conn: Connection, email: str, limit: int, offset: int) -> Record: ...
    async def get_users_by_email_for_admin(self, conn: Connection, email: str, limit: int, offset: int) -> Record: ...
    async def get_user_by_pid(self, conn: Connection, *, pid: str, provider: str ) -> Record: ...
    async def get_user_by_email(self, conn: Connection, *, email: str) -> Record: ...
    async def get_user_by_username(
        self, conn: Connection, *, username: str
    ) -> Record: ...
    async def get_followers(self, conn: Connection, uid: str, limit: int, offset: int) -> Record: ...
    async def create_new_user(
        self,
        conn: Connection,
        *,
        username: Optional[str],
        uid: str,
        role_id: int,
        email: str
    ) -> Record: ...
    async def update_user_by_uid(
        self,
        conn: Connection,
        *,
        uid: str,
        new_username: str,
        new_email: str,
        new_bio: Optional[str],
        new_image: Optional[str],
        new_cover: Optional[str],
        new_subject: Optional[str],
        new_school: Optional[str],
        new_ig: Optional[str],
        new_fb: Optional[str],
        new_yt: Optional[str],
    ) -> Record: ...
    async def update_user_by_uid_admin(
        self,
        conn: Connection,
        *,
        uid: str,
        new_role_id: Optional[int],
    ) -> Record: ...
    async def update_user_by_pid(
        self,
        conn: Connection,
        *,
        uid: str,
        new_username: str,
        new_email: str,
        new_bio: Optional[str],
        new_image: Optional[str],
        new_cover: Optional[str],
        new_subject: Optional[str],
        new_school: Optional[str],
        new_ig: Optional[str],
        new_fb: Optional[str],
        new_yt: Optional[str],
    ) -> Record: ...

class ProfilesQueriesMixin:
    async def is_user_following_for_another(
        self, conn: Connection, *, follower_uid: str, following_uid: str
    ) -> Record: ...
    async def is_user_blocked_by_another(
        self, conn: Connection, *, uid: str, blocked_uid: str
    ) -> Record: ...
    async def subscribe_user_to_another(
        self, conn: Connection, *, follower_uid: str, following_uid: str
    ) -> None: ...
    async def unsubscribe_user_from_another(
        self, conn: Connection, *, follower_uid: str, following_uid: str
    ) -> None: ...
    async def block_user(
        self, conn: Connection, *, uid: str, blocked_uid: str
    ) -> None: ...
    async def unblock_user(
        self, conn: Connection, *, uid: str, blocked_uid: str
    ) -> None: ...
    async def get_user_following_count(
        self, conn: Connection, *, follower_uid: str
    ) -> Record: ...
    async def get_user_follower_count(
        self, conn: Connection, *, following_uid: str
    ) -> Record: ...
    async def get_user_plan_applied_count(
        self, conn: Connection, *, uid: str
    ) -> Record: ...



class Queries(
    UsersQueriesMixin,
    ProfilesQueriesMixin,
): ...

queries: Queries
