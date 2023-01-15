-- Querying each platform usage number on the current date
SELECT
    metrics.platform AS "platform",
    SUM(metrics.usage_number) AS "usage number"
FROM metrics
WHERE DATE(metrics.perform_datetime) = CURRENT_DATE
GROUP BY metrics.platform
ORDER BY SUM(metrics.usage_number) DESC
;

-- Querying each platform usage number on the current month
SELECT
    metrics.platform AS "platform",
    SUM(metrics.usage_number) AS "usage number"
FROM metrics
WHERE TO_CHAR(DATE(metrics.perform_datetime), 'YYYY-MM') = TO_CHAR(CURRENT_DATE, 'YYYY-MM')
GROUP BY metrics.platform
ORDER BY SUM(metrics.usage_number) DESC
;

-- Querying each platform overall usage number
SELECT
    metrics.platform AS "platform",
    SUM(metrics.usage_number) AS "usage number"
FROM metrics
GROUP BY metrics.platform
ORDER BY SUM(metrics.usage_number) DESC
;

-- Querying each command usage number on the current date
SELECT
    metrics.platform AS "platform",
    metrics.action AS "action",
    SUM(metrics.usage_number) AS "usage number"
FROM metrics
WHERE DATE(metrics.perform_datetime) = CURRENT_DATE
GROUP BY
    metrics.platform,
    metrics.action
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
WHERE TO_CHAR(DATE(metrics.perform_datetime), 'YYYY-MM') = TO_CHAR(CURRENT_DATE, 'YYYY-MM')
GROUP BY
    metrics.platform,
    metrics.action
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
