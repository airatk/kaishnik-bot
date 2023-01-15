-- Querying unique users number on a date
WITH user_on_date AS (
    SELECT
        TO_CHAR(metrics.perform_datetime, 'YYYY-MM-DD') AS "date",
        metrics.user_id
    FROM metrics
    GROUP BY
        "date",
        metrics.user_id
    ORDER BY "date"
)
SELECT
    user_on_date.date AS "date",
    COUNT(CASE WHEN "user".telegram_id IS NOT NULL AND "user".vk_id IS NOT NULL THEN "user".user_id END) AS "telegram & vk users",
    COUNT(CASE WHEN "user".telegram_id IS NOT NULL AND "user".vk_id IS NULL THEN "user".user_id END) AS "telegram users",
    COUNT(CASE WHEN "user".vk_id IS NOT NULL AND "user".telegram_id IS NULL THEN "user".user_id END) AS "vk users",
    COUNT(user_on_date.user_id) AS "all users"
FROM user_on_date
LEFT JOIN "user" ON user_on_date.user_id = "user".user_id
GROUP BY user_on_date.date
ORDER BY user_on_date.date;

-- Querying all users statistics
SELECT
    COUNT(CASE WHEN "user".telegram_id IS NOT NULL AND "user".vk_id IS NOT NULL AND "user".is_setup THEN "user".user_id END) AS "telegram & vk users",
    COUNT(CASE WHEN "user".telegram_id IS NOT NULL AND "user".vk_id IS NULL AND "user".is_setup THEN "user".user_id END) AS "telegram users",
    COUNT(CASE WHEN "user".vk_id IS NOT NULL AND "user".telegram_id IS NULL AND "user".is_setup THEN "user".user_id END) AS "vk users",
    COUNT(CASE WHEN "user".telegram_id IS NOT NULL AND "user".vk_id IS NULL AND NOT "user".is_setup THEN "user".user_id END) AS "telegram unsetup users",
    COUNT(CASE WHEN "user".vk_id IS NOT NULL AND "user".telegram_id IS NULL AND NOT "user".is_setup THEN "user".user_id END) AS "vk unsetup users",
    COUNT(CASE WHEN NOT "user".is_setup THEN "user".user_id END) AS "unsetup users",
    COUNT("user".user_id) AS "all users"
FROM "user";

-- Querying new users number on a date
SELECT
    TO_CHAR("user".start_datetime, 'YYYY-MM-DD') AS "join date",
    COUNT(CASE WHEN "user".telegram_id IS NOT NULL AND "user".vk_id IS NOT NULL THEN "user".user_id END) AS "telegram & vk users",
    COUNT(CASE WHEN "user".telegram_id IS NOT NULL AND "user".vk_id IS NULL THEN "user".user_id END) AS "telegram users",
    COUNT(CASE WHEN "user".vk_id IS NOT NULL AND "user".telegram_id IS NULL THEN "user".user_id END) AS "vk users",
    COUNT("user".user_id) AS "all users"
FROM "user"
GROUP BY "join date"
ORDER BY "join date";

-- Querying users growth statistics
SELECT
    TO_CHAR("user".start_datetime, 'YYYY-MM-DD') AS "join date",
    SUM(COUNT(CASE WHEN "user".telegram_id IS NOT NULL AND "user".vk_id IS NOT NULL THEN "user".user_id END)) OVER (ROWS UNBOUNDED PRECEDING) AS "telegram & vk users",
    SUM(COUNT(CASE WHEN "user".telegram_id IS NOT NULL AND "user".vk_id IS NULL THEN "user".user_id END)) OVER (ROWS UNBOUNDED PRECEDING) AS "telegram users",
    SUM(COUNT(CASE WHEN "user".vk_id IS NOT NULL AND "user".telegram_id IS NULL THEN "user".user_id END)) OVER (ROWS UNBOUNDED PRECEDING) AS "vk users",
    SUM(COUNT("user".user_id)) OVER (ROWS UNBOUNDED PRECEDING) AS "all users"
FROM "user"
GROUP BY "join date"
ORDER BY "join date";
