-- name: is-user-following-for-another^
SELECT CASE
           WHEN following_uid IS NULL THEN
               FALSE
           ELSE
               TRUE
           END AS is_following
FROM users u
         LEFT OUTER JOIN followers_to_followings f ON u.uid = f.follower_uid
    AND f.following_uid = (
        SELECT uid
        FROM users
        WHERE uid = :following_uid)
WHERE u.uid = :follower_uid
LIMIT 1;

-- name: is-user-blocked-by-another^
SELECT CASE
           WHEN blocked_uid IS NULL THEN
               FALSE
           ELSE
               TRUE
           END AS is_blocked
FROM users u
         LEFT OUTER JOIN block f ON u.uid = f.uid
    AND f.blocked_uid = (
        SELECT uid
        FROM users
        WHERE uid = :blocked_uid)
WHERE u.uid = :uid
LIMIT 1;

-- name: subscribe-user-to-another!
INSERT INTO followers_to_followings (follower_uid, following_uid)
VALUES ((
            SELECT uid
            FROM users
            WHERE uid = :follower_uid), (
            SELECT uid
            FROM users
            WHERE uid = :following_uid));

-- name: unsubscribe-user-from-another!
DELETE
FROM followers_to_followings
WHERE follower_uid = (
    SELECT uid
    FROM users
    WHERE uid = :follower_uid)
  AND following_uid = (
    SELECT uid
    FROM users
    WHERE uid = :following_uid);

-- name: block-user!
INSERT INTO block (uid, blocked_uid)
VALUES ((
            SELECT uid
            FROM users
            WHERE uid = :uid), (
            SELECT uid
            FROM users
            WHERE uid = :blocked_uid));

-- name: unblock-user!
DELETE
FROM block
WHERE uid = (
    SELECT uid
    FROM users
    WHERE uid = :uid)
  AND blocked_uid = (
    SELECT uid
    FROM users
    WHERE uid = :blocked_uid);

-- name: get-user-following-count$
SELECT count(*) as following_count
FROM followers_to_followings
WHERE follower_uid = :follower_uid;

-- name: get-user-follower-count$
SELECT count(*) as follower_count
FROM followers_to_followings
WHERE following_uid = :following_uid;

-- name: get-user-plan-applied-count$
SELECT count(*) as applied_count
FROM plans
WHERE applied_author_uid = :uid;
