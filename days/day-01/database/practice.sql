-- Day 1 practice: tables, data types, CREATE TABLE, INSERT, basic SELECT
--
-- Before you start (once):  psql -d interview_prep -f days/day-01/database/setup.sql
-- Work in psql (`psql -d interview_prep`) or run this file piece by piece.
-- Write your query under each exercise. No solutions in this file.
-- Useful in psql:  \dt  (list tables)   \d employees  (describe a table)   \q  (quit)
-- ---------------------------------------------------------------------


-- 1. (Easy) Show everything in the departments table.
--    Expected columns: id, name, location   (5 rows)




-- 2. (Easy) Show the first name, last name and salary of every employee.
--    Expected columns: first_name, last_name, salary   (10 rows)
--    Look at the CEO's row: what is shown for a missing department? (That's NULL, more on Day 2.)




-- 3. (Easy) Show the name and price of every product.
--    Expected columns: name, price   (10 rows)




-- 4. (Medium) Create a new table `reviews` for product reviews with these columns:
--      id          auto-generated whole number, the primary key
--      product_id  whole number
--      customer_id whole number
--      rating      whole number
--      comment     text of any length
--      created_at  timestamp that defaults to the current time
--    Check it with  \d reviews




-- 5. (Medium) Insert 3 reviews of your choice (use real product ids 1-10 and customer ids 1-8),
--    then select all rows from `reviews`.
--    Expected columns: id, product_id, customer_id, rating, comment, created_at   (3 rows)
--    Do NOT insert the id or created_at yourself. Let the table fill them in.




-- 6. (Medium) Add yourself as a new customer (name, email, city), then select the
--    customer you just added.
--    Expected columns: id, name, email, city, created_at   (1 row, and its id should be 9)




-- 7. (Interview-level) A salon app needs a table `salon_bookings` to store:
--      a booking id, the customer's name, the customer's phone number (like +91 98765 43210),
--      the service name, the price (e.g. 499.50), the start date and time,
--      and whether the booking is confirmed.
--    Write the CREATE TABLE with the most appropriate data type for each column.
--    Then answer in a comment:
--      (a) why must the phone number NOT be an INT?
--      (b) why is NUMERIC better than FLOAT for the price?
--      (c) TIMESTAMP vs DATE: which did you pick and why?




-- Reset your changes any time by re-running setup.sql (it recreates the shared tables).
-- Note: `reviews` and `salon_bookings` are not part of setup.sql, so drop them yourself:
--   DROP TABLE IF EXISTS reviews, salon_bookings;
