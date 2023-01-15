-- Querying monthly donations statistics
WITH donations_basic_statistics AS (
    SELECT
        TO_CHAR(donation.date, 'YYYY-MM') AS "month",
        COUNT(donation.donation_id) AS "donations number",
        ROUND(AVG(donation.amount)::NUMERIC, 2) AS "average donation amount",
        ROUND(SUM(donation.amount)::NUMERIC, 2) AS "sum of donations"
    FROM donation
    GROUP BY "month"
    ORDER BY "month"
)
SELECT
    donations_basic_statistics."month" AS "month",
    donations_basic_statistics."donations number" AS "donations number",
    donations_basic_statistics."average donation amount" AS "average donation amount",
    donations_basic_statistics."sum of donations" AS "sum of donations",
    SUM(donations_basic_statistics."sum of donations") OVER(ROWS UNBOUNDED PRECEDING) AS "donations sum growth",
    SUM(donations_basic_statistics."donations number") OVER(ROWS UNBOUNDED PRECEDING) AS "donations number growth"
FROM donations_basic_statistics;

-- Querying yearly donations statistics
WITH donations_basic_statistics AS (
    SELECT
        TO_CHAR(donation.date, 'YYYY') AS "year",
        COUNT(donation.donation_id) AS "donations number",
        ROUND(AVG(donation.amount)::NUMERIC, 2) AS "average donation amount",
        ROUND(SUM(donation.amount)::NUMERIC, 2) AS "sum of donations"
    FROM donation
    GROUP BY "year"
    ORDER BY "year"
)
SELECT
    donations_basic_statistics."year" AS "year",
    donations_basic_statistics."donations number" AS "donations number",
    donations_basic_statistics."average donation amount" AS "average donation amount",
    donations_basic_statistics."sum of donations" AS "sum of donations",
    SUM(donations_basic_statistics."sum of donations") OVER(ROWS UNBOUNDED PRECEDING) AS "donations sum growth",
    SUM(donations_basic_statistics."donations number") OVER(ROWS UNBOUNDED PRECEDING) AS "donations number growth"
FROM donations_basic_statistics;
