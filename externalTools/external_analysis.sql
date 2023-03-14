CALL run_query_with_custom_delimiter('|~|', '|*|', 'SELECT id, body INTO OUTFILE "/dev/shm/file_10.csv" FROM posts WHERE tags like "%<javascript>%" and body like "%<pre><code>%" LIMIT 300');


DELIMITER //

CREATE PROCEDURE run_query_with_custom_delimiter(
  IN delimiter_str VARCHAR(10),
  IN enclosing_char VARCHAR(10),
  IN query_str TEXT
)
BEGIN
  SET @delimiter_stmt = CONCAT("FIELDS TERMINATED BY '", delimiter_str, "' ");
  SET @enclosed_stmt = CONCAT("ENCLOSED BY '", enclosing_char, "' ");
  SET @query = CONCAT(query_str, " ", @delimiter_stmt, @enclosed_stmt);
  PREPARE stmt FROM @query;
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END;

DELIMITER ;


SELECT
id, body
INTO OUTFILE [PFAD]
FIELDS TERMINATED BY '|' ENCLOSED BY '~'
LINES TERMINATED BY '\n'
FROM posts
WHERE tags like "%<javascript>%" and body like '%<pre><code>%'

--USE THIS QUERY BECAUSE THE SCRIPTS ARE DESIGNED TO SEPARATE THE FIELDS.
--write all posts and answers that contain javascript code to a csv file.
SELECT
id, body
INTO OUTFILE 'output.csv'
FIELDS TERMINATED BY '|' ENCLOSED BY '~'
LINES TERMINATED BY '\n'
FROM posts
WHERE tags like "%<javascript>%" and body like '%<pre><code>%'

DELIMITER |~|

CREATE PROCEDURE sp_name()
BEGIN
  SELECT
  id, body
INTO OUTFILE 'output.csv'
FIELDS TERMINATED BY '|~|' ENCLOSED BY '|*|'
LINES TERMINATED BY '\n'
FROM posts
WHERE tags like "%<javascript>%" and body like '%<pre><code>%'
LIMIT 300;
END |~|

DELIMITER ;



SELECT
  id, body
INTO OUTFILE 'output.csv'
FIELDS TERMINATED BY '|' ENCLOSED BY '~'
LINES TERMINATED BY '\n'
FROM posts
WHERE tags like "%<javascript>%" and posttypeid=1 and body like '%<pre><code>%'
LIMIT 300;


