-- name: get-post-by-id^
SELECT id,
       store_id,
       user_id,
       body,
       image_url,
       rating,
       status,
       created_at,
       updated_at
FROM posts
WHERE id = :id AND status = 1
LIMIT 1;

-- name: get-posts-by-store-id
SELECT *, count(*) OVER() AS total
FROM (
    SELECT
        id,
        store_id,
        user_id,
        body,
        image_url,
        rating,
        status,
        created_at,
        updated_at
    FROM posts) AS posts
WHERE status = 1 AND store_id = :store_id
ORDER BY posts.created_at DESC
LIMIT :limit
OFFSET :offset;

-- name: get-posts-by-user-id
SELECT *, count(*) OVER() AS total
FROM (
    SELECT
        id,
        store_id,
        user_id,
        body,
        image_url,
        rating,
        status,
        created_at,
        updated_at
    FROM posts) AS posts
WHERE status = 1 AND user_id = :user_id
ORDER BY posts.created_at DESC
LIMIT :limit
OFFSET :offset;

-- name: create-post<!
INSERT INTO posts (store_id, user_id, body, image_url, rating, status)
VALUES (:store_id, :user_id, :body, :image_url, :rating, :status)
RETURNING
    id, created_at, updated_at;

-- name: update-post-by-id<!
UPDATE
    posts
SET store_id     = :new_store_id,
    user_id      = :new_user_id,
    body         = :new_body,
    image_url    = :new_image_url,
    rating       = :new_rating,
    status       = :new_status
WHERE id = :id
RETURNING
    updated_at;
