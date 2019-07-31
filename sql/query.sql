/* create template table(s) */
DROP TABLE IF EXISTS profile;
CREATE TABLE IF NOT EXISTS profile (
  id BIGSERIAL PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  email TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ
);

DROP TABLE IF EXISTS skill;
CREATE TABLE IF NOT EXISTS skill (
  id BIGSERIAL PRIMARY KEY,
  profile_id BIGSERIAL REFERENCES profile(id),
  name TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  updated_at TIMESTAMPTZ
);


/* add data */
INSERT INTO profile
VALUES
  (1, 'John', 'Smith', 'test1@gmail.com', now() AT TIME ZONE 'UTC'),
  (2, 'Paul', 'Smith', 'test2@gmail.com', now() AT TIME ZONE 'UTC' + interval '1' second),
  (3, 'Allen', 'Smith', 'test3@gmail.com', now() AT TIME ZONE 'UTC' + interval '2' second),
  (4, 'Teddy', 'Smith', 'test4@gmail.com', now() AT TIME ZONE 'UTC' + interval '3' second),
  (5, 'Mark', 'Smith', 'test5@gmail.com', now() AT TIME ZONE 'UTC' + interval '4' second)
;


/* managing tables */
ALTER TABLE profile DROP COLUMN IF EXISTS updated_at;
ALTER TABLE profile ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ;
ALTER TABLE profile RENAME COLUMN updated_at TO updated;
ALTER TABLE profile RENAME COLUMN updated TO updated_at;


/* temporary table */
DROP TABLE IF EXISTS profile_temp;

SELECT *
INTO TEMPORARY profile_temp 
FROM profile
WHERE first_name ILIKE '%a%';


SELECT *
FROM profile;

select
	sum(
		case when first_name ilike '%a%' then 2 else 4 end
	)
from profile;

SELECT *
FROM profile_temp;

SELECT *
FROM skill;

SELECT *
FROM profile
ORDER BY created_at
LIMIT 5 OFFSET 2;

SELECT substring(first_name, 1, 3)
FROM profile;

SELECT to_char(created_at, 'D')
FROM profile;

SELECT *
FROM profile
ORDER BY CASE
   WHEN first_name='Mark' THEN 1
   WHEN first_name='John' THEN 2
   WHEN first_name='Allen' THEN 3
   WHEN first_name='Teddy' THEN 4
   ELSE 5
END;

select string_agg(first_name || ' ' || created_at, '; ' order by created_at desc)
from profile;

select last_name, string_agg(first_name, ', ')
from profile
group by last_name;

select concat(first_name, ', ', last_name)
from profile
order by created_at desc;

select concat_ws(', ', first_name, last_name, created_at)
from profile;

select last_name, array_agg(first_name)
from profile
group by last_name;