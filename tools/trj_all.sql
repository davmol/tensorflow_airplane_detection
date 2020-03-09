

CREATE MATERIALIZED VIEW trj_2019_11_27 AS

with sorted as (


select * from dump where  a_type in ('B735', 'C510','E170', 'B733', 'B763', 'E75S', 'B752', 'B788', 'CRJ9', 'B739', 'BCS1', 'A333', 'B77W', 'E190', 'B764', 'A332', 'E195', 'B737', 'AT76', 'DH8D', 'A21N', 'A20N', 'BCS3', 'A320', 'A318', 'A319','A321','B738') and altitude_cor < 13123.36  and 
timestamp > '2019-11-27' and timestamp < '2019-11-28'  order by flight, timestamp asc



),
 ptm AS (

   SELECT 
     st_makepoint(
       st_x(ST_TRANSFORM(sorted.geom, 4326)),
       st_y(ST_TRANSFORM(sorted.geom, 4326)),
       sorted.altitude_cor,
       date_part('epoch', sorted.timestamp)) AS pt,
     sorted.timestamp,
     sorted.flight
   FROM sorted
   ORDER BY flight, timestamp asc
 )
 SELECT row_number() OVER () AS id,
   st_makeline(ptm.pt) AS st_makeline,
   min(ptm.timestamp) AS min_t,
   max(ptm.timestamp) AS max_t,
 ptm.flight AS callsign
 FROM ptm
 GROUP BY  ptm.flight
WITH DATA;


CREATE MATERIALIZED VIEW trj_2019_11_28 AS

with sorted as (


select * from dump where  a_type in ('B735', 'C510','E170', 'B733', 'B763', 'E75S', 'B752', 'B788', 'CRJ9', 'B739', 'BCS1', 'A333', 'B77W', 'E190', 'B764', 'A332', 'E195', 'B737', 'AT76', 'DH8D', 'A21N', 'A20N', 'BCS3', 'A320', 'A318', 'A319','A321','B738') and altitude_cor < 13123.36  and 
timestamp >= '2019-11-28' and timestamp < '2019-11-29'  order by flight, timestamp asc



),
 ptm AS (

   SELECT 
     st_makepoint(
       st_x(ST_TRANSFORM(sorted.geom, 4326)),
       st_y(ST_TRANSFORM(sorted.geom, 4326)),
       sorted.altitude_cor,
       date_part('epoch', sorted.timestamp)) AS pt,
     sorted.timestamp,
     sorted.flight
   FROM sorted
   ORDER BY flight, timestamp asc
 )
 SELECT row_number() OVER () AS id,
   st_makeline(ptm.pt) AS st_makeline,
   min(ptm.timestamp) AS min_t,
   max(ptm.timestamp) AS max_t,
 ptm.flight AS callsign
 FROM ptm
 GROUP BY  ptm.flight
WITH DATA;


CREATE MATERIALIZED VIEW trj_2019_11_29 AS

with sorted as (


select * from dump where  a_type in ('B735', 'C510','E170', 'B733', 'B763', 'E75S', 'B752', 'B788', 'CRJ9', 'B739', 'BCS1', 'A333', 'B77W', 'E190', 'B764', 'A332', 'E195', 'B737', 'AT76', 'DH8D', 'A21N', 'A20N', 'BCS3', 'A320', 'A318', 'A319','A321','B738') and altitude_cor < 13123.36  and 
timestamp > '2019-11-29' and timestamp < '2019-11-30'  order by flight, timestamp asc



),
 ptm AS (

   SELECT 
     st_makepoint(
       st_x(ST_TRANSFORM(sorted.geom, 4326)),
       st_y(ST_TRANSFORM(sorted.geom, 4326)),
       sorted.altitude_cor,
       date_part('epoch', sorted.timestamp)) AS pt,
     sorted.timestamp,
     sorted.flight
   FROM sorted
   ORDER BY flight, timestamp asc
 )
 SELECT row_number() OVER () AS id,
   st_makeline(ptm.pt) AS st_makeline,
   min(ptm.timestamp) AS min_t,
   max(ptm.timestamp) AS max_t,
 ptm.flight AS callsign
 FROM ptm
 GROUP BY  ptm.flight
WITH DATA;


CREATE MATERIALIZED VIEW trj_2019_11_30 AS

with sorted as (


select * from dump where  a_type in ('B735', 'C510','E170', 'B733', 'B763', 'E75S', 'B752', 'B788', 'CRJ9', 'B739', 'BCS1', 'A333', 'B77W', 'E190', 'B764', 'A332', 'E195', 'B737', 'AT76', 'DH8D', 'A21N', 'A20N', 'BCS3', 'A320', 'A318', 'A319','A321','B738') and altitude_cor < 13123.36  and 
timestamp > '2019-11-30' and timestamp < '2019-12-01'  order by flight, timestamp asc



),
 ptm AS (

   SELECT 
     st_makepoint(
       st_x(ST_TRANSFORM(sorted.geom, 4326)),
       st_y(ST_TRANSFORM(sorted.geom, 4326)),
       sorted.altitude_cor,
       date_part('epoch', sorted.timestamp)) AS pt,
     sorted.timestamp,
     sorted.flight
   FROM sorted
   ORDER BY flight, timestamp asc
 )
 SELECT row_number() OVER () AS id,
   st_makeline(ptm.pt) AS st_makeline,
   min(ptm.timestamp) AS min_t,
   max(ptm.timestamp) AS max_t,
 ptm.flight AS callsign
 FROM ptm
 GROUP BY  ptm.flight
WITH DATA;

CREATE MATERIALIZED VIEW trj_2019_12_01 AS

with sorted as (


select * from dump where  a_type in ('B735', 'C510','E170', 'B733', 'B763', 'E75S', 'B752', 'B788', 'CRJ9', 'B739', 'BCS1', 'A333', 'B77W', 'E190', 'B764', 'A332', 'E195', 'B737', 'AT76', 'DH8D', 'A21N', 'A20N', 'BCS3', 'A320', 'A318', 'A319','A321','B738') and altitude_cor < 13123.36  and 
timestamp > '2019-12-01' and timestamp < '2019-12-02'  order by flight, timestamp asc



),
 ptm AS (

   SELECT 
     st_makepoint(
       st_x(ST_TRANSFORM(sorted.geom, 4326)),
       st_y(ST_TRANSFORM(sorted.geom, 4326)),
       sorted.altitude_cor,
       date_part('epoch', sorted.timestamp)) AS pt,
     sorted.timestamp,
     sorted.flight
   FROM sorted
   ORDER BY flight, timestamp asc
 )
 SELECT row_number() OVER () AS id,
   st_makeline(ptm.pt) AS st_makeline,
   min(ptm.timestamp) AS min_t,
   max(ptm.timestamp) AS max_t,
 ptm.flight AS callsign
 FROM ptm
 GROUP BY  ptm.flight
WITH DATA;


