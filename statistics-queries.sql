-- METRICS

-- Querying each platform usage number on the current date
SELECT
    metrics.platform AS "platform",
    SUM(metrics.usage_number) AS "usage number"
FROM metrics
WHERE
    DATE(metrics.perform_datetime) = CURRENT_DATE
GROUP BY metrics.platform
ORDER BY
    SUM(metrics.usage_number) DESC
;

-- Querying each platform usage number on the current month
SELECT
    metrics.platform AS "platform",
    SUM(metrics.usage_number) AS "usage number"
FROM metrics
WHERE
    TO_CHAR(DATE(metrics.perform_datetime), 'YYYY-MM') = TO_CHAR(CURRENT_DATE, 'YYYY-MM')
GROUP BY metrics.platform
ORDER BY
    SUM(metrics.usage_number) DESC
;

-- Querying each platform overall usage number
SELECT
    metrics.platform AS "platform",
    SUM(metrics.usage_number) AS "usage number"
FROM metrics
GROUP BY metrics.platform
ORDER BY
    SUM(metrics.usage_number) DESC
;

-- Querying each command usage number on the current date
SELECT
    metrics.platform AS "platform",
    metrics.action AS "action",
    SUM(metrics.usage_number) AS "usage number"
FROM metrics
WHERE
    DATE(metrics.perform_datetime) = CURRENT_DATE
GROUP BY metrics.platform, metrics.action
ORDER BY
    metrics.platform,
    SUM(metrics.usage_number) DESC
;

-- Querying each command usage number on the current month
SELECT
    metrics.platform AS "platform",
    metrics.action AS "action",
    SUM(metrics.usage_number) AS "usage number"
FROM metrics
WHERE
    TO_CHAR(DATE(metrics.perform_datetime), 'YYYY-MM') = TO_CHAR(CURRENT_DATE, 'YYYY-MM')
GROUP BY metrics.platform, metrics.action
ORDER BY
    metrics.platform,
    SUM(metrics.usage_number) DESC
;

-- Querying each command overall usage number
SELECT
    metrics.platform AS "platform",
    metrics.action AS "action",
    SUM(metrics.usage_number) AS "usage number"
FROM metrics
GROUP BY metrics.platform, metrics.action
ORDER BY
    metrics.platform,
    SUM(metrics.usage_number) DESC
;

-- Querying users number of each command on the current date
SELECT
    metrics.platform AS "platform",
    metrics.action AS "action",
    COUNT(metrics.user_id) AS "users number"
FROM metrics
WHERE
    DATE(metrics.perform_datetime) = CURRENT_DATE
GROUP BY metrics.platform, metrics.action
ORDER BY
    metrics.platform,
    SUM(metrics.usage_number) DESC
;


-- USERS

-- Querying unique users number on a date
SELECT
    user_on_date.date AS "date",
    COUNT(CASE WHEN "user".telegram_id IS NOT NULL AND "user".vk_id IS NOT NULL THEN "user".user_id END) AS "telegram & vk users",
    COUNT(CASE WHEN "user".telegram_id IS NOT NULL AND "user".vk_id IS NULL THEN "user".user_id END) AS "telegram users",
    COUNT(CASE WHEN "user".vk_id IS NOT NULL AND "user".telegram_id IS NULL THEN "user".user_id END) AS "vk users",
    COUNT(user_on_date.user_id) AS "all users"
FROM (
    SELECT
        TO_CHAR(metrics.perform_datetime, 'YYYY-MM-DD') AS "date",
        metrics.user_id
    FROM metrics
    GROUP BY "date", metrics.user_id
    ORDER BY "date"
) AS user_on_date
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


-- DONATIONS

-- Querying monthly donations statistics
SELECT
    donations_basic_statistics."month" AS "month",
    donations_basic_statistics."donations number" AS "donations number",
    donations_basic_statistics."average donation amount" AS "average donation amount",
    donations_basic_statistics."sum of donations" AS "sum of donations",
    SUM(donations_basic_statistics."sum of donations") OVER (ROWS UNBOUNDED PRECEDING) AS "donations sum growth",
    SUM(donations_basic_statistics."donations number") OVER (ROWS UNBOUNDED PRECEDING) AS "donations number growth"
FROM (
    SELECT
        TO_CHAR(donation.date, 'YYYY-MM') AS "month",
        COUNT(donation.donation_id) AS "donations number",
        ROUND(AVG(donation.amount)::NUMERIC, 2) AS "average donation amount",
        ROUND(SUM(donation.amount)::NUMERIC, 2) AS "sum of donations"
    FROM donation
    GROUP BY "month"
    ORDER BY "month"
) AS donations_basic_statistics;

-- Querying yearly donations statistics
SELECT
    donations_basic_statistics."year" AS "year",
    donations_basic_statistics."donations number" AS "donations number",
    donations_basic_statistics."average donation amount" AS "average donation amount",
    donations_basic_statistics."sum of donations" AS "sum of donations",
    SUM(donations_basic_statistics."sum of donations") OVER (ROWS UNBOUNDED PRECEDING) AS "donations sum growth",
    SUM(donations_basic_statistics."donations number") OVER (ROWS UNBOUNDED PRECEDING) AS "donations number growth"
FROM (
    SELECT
        TO_CHAR(donation.date, 'YYYY') AS "year",
        COUNT(donation.donation_id) AS "donations number",
        ROUND(AVG(donation.amount)::NUMERIC, 2) AS "average donation amount",
        ROUND(SUM(donation.amount)::NUMERIC, 2) AS "sum of donations"
    FROM donation
    GROUP BY "year"
    ORDER BY "year"
) AS donations_basic_statistics;
