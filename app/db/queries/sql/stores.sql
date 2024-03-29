-- name: get-store-by-id^
SELECT id,
       name,
       descriptions,
       phone,
       address,
       rating,
       review_count,
       image,
       social_media,
       business_hours,
       place_id,
       location,
       status,
       created_at,
       updated_at
FROM stores
WHERE id = :id and status = 1
LIMIT 1;

-- name: get-store-list
SELECT *, count(*) OVER() AS total
FROM (
    SELECT
        id,
        name,
        descriptions,
        phone,
        address,
        rating,
        review_count,
        image,
        social_media,
        business_hours,
        place_id,
        location,
        status,
        created_at,
        updated_at
    FROM stores) AS stores
WHERE status = 1
ORDER BY stores.created_at DESC
LIMIT :limit
OFFSET :offset;

-- name: create-store<!
INSERT INTO stores (name, descriptions, phone, address, rating, review_count, image, social_media, business_hours, place_id, location, status)
VALUES (:name, :descriptions, :phone, :address, :rating, :review_count, :image, :social_media, :business_hours, :place_id, :location, :status)
RETURNING
    id, created_at, updated_at;

-- name: update-store-by-id<!
UPDATE
    stores
SET name           = :new_name,
    descriptions   = :new_descriptions,
    phone          = :new_phone,
    address        = :new_address,
    rating         = :new_rating,
    review_count   = :new_review_count,
    image          = :new_image,
    social_media   = :new_social_media,
    business_hours = :new_business_hours,
    place_id       = :new_place_id,
    location       = :new_location,
    status         = :new_status
WHERE id = :id
RETURNING
    updated_at;
