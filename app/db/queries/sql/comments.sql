-- name: get-comment-by-id^
SELECT id,
       post_id,
       user_id,
       body,
       status,
       created_at,
       updated_at
FROM comments
WHERE id = :id AND status = 1
LIMIT 1;

-- name: get-comments-by-post-id
SELECT *, count(*) OVER() AS total
FROM (
    SELECT
        id,
        post_id,
        user_id,
        body,
        status,
        created_at,
        updated_at
    FROM comments) AS comments
WHERE status = 1 AND post_id = :post_id
ORDER BY comments.created_at DESC
LIMIT :limit
OFFSET :offset;

-- name: create-comment<!
INSERT INTO comments (post_id, user_id, body, status)
VALUES (:post_id, :user_id, :body, :status)
RETURNING
    id, created_at, updated_at;

-- name: update-comment-by-id<!
UPDATE
    comments
SET body         = :new_body,
    status       = :new_status
WHERE id = :id
RETURNING
    updated_at;
