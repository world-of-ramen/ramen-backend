-- name: get-user-by-id^
SELECT id,
       wallet_address,
       image,
       status,
       created_at,
       updated_at
FROM users
WHERE id = :id AND status = 1
LIMIT 1;

-- name: get-user-by-wallet-address^
SELECT id,
       wallet_address,
       image,
       status,
       created_at,
       updated_at
FROM users
WHERE wallet_address = :wallet_address AND status = 1
LIMIT 1;

-- name: get-wallet-address-by-user-id^
SELECT wallet_address
FROM users
WHERE id = :user_id AND status = 1
LIMIT 1;

-- name: get-users
SELECT id,
       wallet_address,
       image,
       status,
       created_at,
       updated_at
FROM users
WHERE status = 1
LIMIT :limit
OFFSET
:offset;

-- name: create-new-user<!
INSERT INTO users (wallet_address, image, status)
VALUES (:wallet_address, :image, :status)
RETURNING
    id, created_at, updated_at;

-- name: update-user-by-id<!
UPDATE
    users
SET wallet_address  = :new_wallet_address,
    image           = :new_image,
    status          = :new_status
WHERE id = :id
RETURNING
    updated_at;
