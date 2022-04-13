-- name: get-nft-by-id^
SELECT id,
       user_id,
       wallet_address,
       image_url,
       token_address,
       token_id,
       name,
       symbol,
       created_at,
       updated_at
FROM nfts
WHERE id = :id
LIMIT 1;

-- name: get-nfts-by-user-id
SELECT id,
       user_id,
       wallet_address,
       image_url,
       token_address,
       token_id,
       name,
       symbol,
       created_at,
       updated_at
FROM nfts
WHERE user_id = :user_id;

-- name: get-nft^
SELECT id,
       user_id,
       wallet_address,
       image_url,
       token_address,
       token_id,
       name,
       symbol,
       created_at,
       updated_at
FROM nfts
WHERE user_id = :user_id AND wallet_address = :wallet_address AND token_address = :token_address AND token_id = :token_id
LIMIT 1;

-- name: create-new-nft<!
INSERT INTO nfts (user_id, wallet_address, image_url, token_address, token_id, name, symbol)
VALUES (:user_id, :wallet_address, :image_url, :token_address, :token_id, :name, :symbol)
RETURNING
    id, created_at, updated_at;

-- name: update-nft-by-id<!
UPDATE
    nfts
SET image_url    = :new_image_url
WHERE id = :id
RETURNING
    updated_at;
