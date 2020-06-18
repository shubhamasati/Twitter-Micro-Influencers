-- Creating a database
CREATE DATABASE twitter;

-- Changing database to twitter
USE twitter;

-- Adding JAR file for custom SerDe to read and write JSON file from and into the TABLE
ADD JAR json-serde-1.3.6-SNAPSHOT-jar-with-dependencies.jar;

-- External table to hold the tweets
CREATE EXTERNAL TABLE IF NOT EXISTS tweets(
    text STRING,
    entities STRUCT<hashtags:ARRAY<STRUCT<text:string>>>,
    `user` STRUCT<
    name:STRING,
    screen_name:STRING,
    `location`:STRING,
    friends_count:INT,
    followers_count:INT,
    statuses_count:INT,
    varified:BOOLEAN,
    utc_offset:INT,
    time_zone:STRING>
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION '/twitter/data';


-- Storing the result of query in HDFS
INSERT OVERWRITE  DIRECTORY '/twitter/output/'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE
-- Fetching the users from 'India' having most number of followers 
SELECT DISTINCT `user`.name as name, `user`.screen_name as username, `user`.followers_count as followers
FROM tweets
WHERE size(entities.hashtags) > 0
AND `user`.`location` LIKE '%India%'
ORDER BY followers DESC
LIMIT 10;