CREATE DATABASE db_name;
SHOW DATABASES;
USE db_name;

---

CREATE TABLE table_name (column_name TYPE, ....);
SHOW TABLES;

DESCIBE TABLE table_names;

SHOW COLUMNS FROM table_name;

---

# Data Types

TINYINT - 1 byte
SMALLINT - 2 bytes
MEDIUMINT - 3
INT - 4
BIGINT - 8


FLOAT - 4 bytes
DOUBLE - 8 bytes

DECIMAL(p,s) - 4 bytes

CHAR(n) - Max length  of 255 characters
VARCHAR(n) - Max lenght of 65,535 characters

> In MySQL, CHAR stores fixed-length strings by padding shorter values with trailing spaces, whereas VARCHAR stores variable-length strings using only the space needed for the actual characters plus a small length prefix

TINYTEXT
MEDIUMTEXT
LONGTEXT

BINARY
VARBINARY
BLOB


DATE
TIME
DATETIME
TIMESTAMP - similar to DATETIME, but also tracks timezone and updates automatically when records are modified

---

SELECT DISTINCT column_name FROM table_name WHERE another_column_name = 'some value';

---

# Constraints

NOT NULL
UNIQUE
PRIMARY KEY -> Immutable, Unique and NonNULL
FOREIGN KEY
DEFAULT
AUTO_INCREMENT

---

# Comparison operators

- = 
- != or <> 
- < 
- >
- <=
- >=
- BETWEEN 
- LIKE
- IN
- IS NULL 
- IS NOT NULL

---

# Logical Operators

- AND
- OR
- NOT
- XOR

---

# String Functions

- CONCAT(string1, string2)
- CONCAT_WS("-", string1, string2)
- LENGTH() -> returns number of **bytes**
- CHAR_LENGTH() -> returns number of characters
- SUBSTRING(string, start_index, length) ->length is optional
- LEFT(string, length) -> returns specific number of characters from start of string
- RIGHT(string, length)
- UPPER(string)
- LOWER(string)
- TRIM(string) -> removes leading and trailing spaces
- LTRIM(string)
- RTRIM(string)
- REPLACE(original_str, find_str, replace_with_str) -> replaces all occurances of a substring in a given string with another string
- INSTR(string, sub_string) -> returns **first** occurance index of a substring if exists, else returns 0
- LOCATE(substring, string, start_position)
- ASCII(string) -> returns the ascii value of the **first character only**
- CHAR(x) -> returns the character representation of the value passed.. eg: CHAR(65 USING ASCII)
- REGEXP pattern -> eg: select * from emp where name REGXP '^R';
- REVERSE(string)

---

# Arithematic Operations

- +
- -
- *
- /
- DIV --> Integer division, discards fractional part toward zero
- % or MOD

---

# Modifying Tables

ALTER TABLE table_name ADD COLUMN column_name TYPE;
ALTER TABLE table_name DROP COLUMN column_name;

ALTER TABLE table_name MODIFY COLUMN column_name NEW_TYPE;

ALTER TABLE table_name CHANGE column_name new_column_name;

ALTER TABLE table_name DROP PRIMARY KEY;
ALTER TABLE table_name MODIFY column_name TYPE; -> This drops any constraints on the column because MODIFY was not given any constraints.. hence it defaults to having none.
ALTER TABLE table_name DROP FOREIGN KEY fk_name;
ALTER TABLE table_name DROP INDEX column_name -> Drops Unique constraint.

ALTER TABLE table_name RENAME TO new_table_name;

---

# CRUD

insert into
select 

select * from table_name order by column_name desc;

select * from table_name LIMIT 5;

update table_name set column_name = value where <condition>

delete from table_name where <condition>

---

# Aggregate Functions

- AVG() -> SELECT AVG(age) FROM people WHERE country = 'IN';

- COUNT() -> Counts number of NON-NULL rows
- Eg: SELECT COUNT(DISTINCT country) FROM people;

- MIN()
- MAX()
- SUM()

- GROUP BY

---

# Foreign Key Constraint

- Enforces Referential Integrity

CREATE TABLE orders(
order_id INT PRIMARY KEY AUTO_INCREMENT,
customer_id INT,
FOREIGN KEY(customer_id) REFERENCES customers(id)
);

---

# Relationships

- 1:1 relationship -> Apply unique constraint on FK column

- 1:m relationship

- m:m -> use junction table

---

# Views

- CREATE OR REPLACE VIEW view_name AS <QUERY>
- DROP VIEW view_name

---

# Window Functions
