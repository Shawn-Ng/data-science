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
ALTER TABLE PROFILE DROP COLUMN IF EXISTS updated_at;
ALTER TABLE PROFILE ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ;
ALTER TABLE PROFILE RENAME COLUMN updated_at TO updated;
ALTER TABLE PROFILE RENAME COLUMN updated TO updated_at;


/* temporary table */
DROP TABLE IF EXISTS profile_temp;

SELECT *
INTO TEMPORARY profile_temp 
FROM profile
WHERE first_name ILIKE '%a%';


SELECT *
FROM profile;

SELECT *
FROM profile_temp;

SELECT *
FROM skill;