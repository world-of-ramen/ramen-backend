-- name: create-whitelist_contracts<!
INSERT INTO whitelist_contracts (contract_address, status)
VALUES (contract_address, 1)
RETURNING
    id, created_at, updated_at;

-- name: get-whitelist_contracts
SELECT contract_address
FROM whitelist_contracts
LIMIT :limit
OFFSET :offset;

-- name: update-whitelist_contracts<!
UPDATE
    whitelist_contracts
SET status       = :new_status
WHERE contract_address = :contract_address
RETURNING
    updated_at;
