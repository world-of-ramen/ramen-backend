-- name: get-user-by-uid^
SELECT uid,
       role_id,
       provider,
       pid,
       username,
       email,
       bio,
       image,
       cover,
       subject,
       school,
       ig,
       fb,
       yt,
       created_at,
       updated_at
FROM users
WHERE uid = :uid
LIMIT 1;

-- name: get-users
SELECT uid,
       role_id,
       pid,
       username,
       email,
       bio,
       image,
       cover,
       subject,
       school,
       ig,
       fb,
       yt,
       created_at,
       updated_at
FROM users
LIMIT :limit
OFFSET
:offset;

-- name: get-users-for-admin
SELECT uid,
       role_id,
       pid,
       username,
       email,
       bio,
       image,
       cover,
       subject,
       school,
       ig,
       fb,
       yt,
       created_at,
       updated_at,
       COUNT(*) OVER() AS total
FROM users
LIMIT :limit
OFFSET
:offset;

-- name: get-users-by-email
SELECT uid,
       role_id,
       pid,
       username,
       email,
       bio,
       image,
       cover,
       subject,
       school,
       ig,
       fb,
       yt,
       created_at,
       updated_at
FROM users
WHERE email = :email
LIMIT :limit
OFFSET
:offset;

-- name: get-users-by-email-for-admin
SELECT uid,
       role_id,
       pid,
       username,
       email,
       bio,
       image,
       cover,
       subject,
       school,
       ig,
       fb,
       yt,
       created_at,
       updated_at,
       COUNT(*) OVER() AS total
FROM users
WHERE email = :email
LIMIT :limit
OFFSET
:offset;

-- name: get-followers
SELECT uid,
       role_id,
       pid,
       username,
       email,
       bio,
       image,
       cover,
       subject,
       school,
       ig,
       fb,
       yt,
       created_at,
       updated_at
FROM users
WHERE
	uid in (
		SELECT
			follower_uid
		FROM
			followers_to_followings
		WHERE
			following_uid = :uid)

LIMIT :limit
OFFSET
:offset;


-- name: get-user-by-pid^
SELECT uid,
       role_id,
       provider,
       pid,
       username,
       email,
       bio,
       image,
       cover,
       subject,
       school,
       ig,
       fb,
       yt,
       created_at,
       updated_at
FROM users
WHERE pid = :pid and provider = :provider
LIMIT 1;

-- name: get-user-by-email^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       bio,
       image,
       subject,
       school,
       ig,
       fb,
       yt,
       created_at,
       updated_at
FROM users
WHERE email = :email
LIMIT 1;


-- name: get-user-by-username^
SELECT id,
       username,
       email,
       salt,
       hashed_password,
       bio,
       image,
       subject,
       school,
       ig,
       fb,
       yt,
       created_at,
       updated_at
FROM users
WHERE username = :username
LIMIT 1;


-- name: create-new-user<!
INSERT INTO users (uid, role_id, username, email, image, pid, provider)
VALUES (:uid, :role_id, :username, :email, :image, :pid, :provider)
RETURNING
    id, created_at, updated_at;


-- name: update-user-by-username<!
UPDATE
    users
SET username        = :new_username,
    email           = :new_email,
    salt            = :new_salt,
    hashed_password = :new_password,
    bio             = :new_bio,
    image           = :new_image,
    subject         = :new_subject,
    school          = :new_school,
    ig              = :new_ig,
    fb              = :new_fb,
    yt              = :new_yt
WHERE username = :username
RETURNING
    updated_at;


-- name: update-user-by-uid<!
UPDATE
    users
SET username        = :new_username,
    email           = :new_email,
    bio             = :new_bio,
    image           = :new_image,
    cover           = :new_cover,
    subject         = :new_subject,
    school          = :new_school,
    ig              = :new_ig,
    fb              = :new_fb,
    yt              = :new_yt
WHERE uid = :uid
RETURNING
    updated_at;

-- name: update-user-by-uid-admin<!
UPDATE
    users
SET role_id        = :new_role_id
WHERE uid = :uid
RETURNING
    updated_at;
