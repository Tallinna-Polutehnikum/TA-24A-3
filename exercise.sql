-- SQL töö - kirjuta iga kommentaari alla oma SQL lause.
-- Andmed tulevad failist companies.sql (tabel companies, 1000 rida).

-- 1. select all columns and rows from companies table
SELECT * FROM companies;

-- 2. select only id, name and start_year columns from companies table
SELECT id, name, start_year FROM companies;

-- 3. select all columns from companies table where currency is "EUR"
SELECT * FROM companies WHERE currency = 'EUR';

-- 4. select all columns from companies table where start_year is 2001 and currency is "RUB"
SELECT * FROM companies WHERE start_year = 2001 AND currency = 'RUB';

-- 5. select id, name, currency and profit from companies table where country is "Ukraine"
SELECT id, name, currency, profit FROM companies WHERE country = 'Ukraine';

-- 6. select all columns where profit is higher than 1000000
SELECT * FROM companies WHERE profit > 1000000;

-- 7. select all columns where profit is lower than or equal to 1000000
SELECT * FROM companies WHERE profit <= 1000000;

-- 8. get sum of all profit in companies table where country is "Poland"
SELECT SUM(profit) FROM companies WHERE country = 'Poland';

-- 9. get average profit for all companies in Germany
SELECT AVG(profit) FROM companies WHERE country = 'Germany';

-- 10. get all columns for companies table where name starts with letter E
SELECT * FROM companies WHERE name LIKE 'E%';

-- 11. get all columns for companies table where name starts with letter U or name ends with letter s
SELECT * FROM companies WHERE name LIKE 'U%' OR name LIKE '%s';

-- 12. get all columns for companies table where name or country contains letter l
SELECT * FROM companies WHERE name LIKE '%l%' OR country LIKE '%l%';

-- 13. get all columns for companies table where currency is "CNY" and sort them by start_year older companies first
SELECT * FROM companies WHERE currency = 'CNY' ORDER BY start_year ASC;

-- 14. return top 10 rows with lowest profit (sort by profit and then return first 10)
SELECT * FROM companies ORDER BY profit ASC LIMIT 10;

-- 15. return next 10 with lowest profit (skipping first 10)
SELECT * FROM companies ORDER BY profit ASC LIMIT 10 OFFSET 10;

-- 16. return all unique currencies
SELECT DISTINCT currency FROM companies;

-- 17. return all companies in china with start_year between 2000 - 2020
SELECT * FROM companies WHERE country = 'China' AND start_year BETWEEN 2000 AND 2020;

-- 18. return count of companies in china with start_year between 2000 - 2020
SELECT COUNT(*) FROM companies WHERE country = 'China' AND start_year BETWEEN 2000 AND 2020;

-- 19. return all companies in china, germany, italy and russia
SELECT * FROM companies WHERE country IN ('China', 'Germany', 'Italy', 'Russia');

-- 20. insert one row into companies where id is 1001, name is 'Aphotheka', currency is "EUR", profit is 25000, start_year is 2025 and country is "Estonia"
INSERT INTO companies (id, name, currency, profit, start_year, country) VALUES (1001, 'Aphotheka', 'EUR', 25000, 2025, 'Estonia');

-- 21. Update all rows where country is 'Russia' and set profit to 0
UPDATE companies SET profit = 0 WHERE country = 'Russia';

-- 22. Delete all rows where start_year is less than 2000
DELETE FROM companies WHERE start_year < 2000;

-- 23. Create table "products" where there are fields id, name, price, ean, description, is_alcoholic - figure out reasonable types for those fields yourself
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    ean VARCHAR(13),
    description TEXT,
    is_alcoholic BOOLEAN NOT NULL DEFAULT FALSE
);

-- 24. Remove the products table from the database
DROP TABLE products;
