SELECT * FROM  frost_data fd 
WHERE fd.frost <> 0

SELECT * FROM frost_data fd 
WHERE fd.min_temperature <=0




SELECT * FROM frost_data_all fd 

SELECT
    TRIM(to_char(date, 'Month')) as month,
    AVG(min_temp) as average_min_temp
FROM
    frost_data_all
WHERE
    date >= '1991-01-01' AND date <= '2020-12-31'
GROUP BY
    EXTRACT(MONTH FROM date), month
ORDER BY
    EXTRACT(MONTH FROM date);
    
   
   
   
WITH monthly_mins AS (
    SELECT
        EXTRACT(YEAR FROM date) as year,
        EXTRACT(MONTH FROM date) as month,
        MIN(min_temp) as min_monthly_temp
    FROM
        frost_data_all
    WHERE
        date >= '1991-01-01' AND date <= '2020-12-31'
    GROUP BY
        year, month
)
SELECT
    to_char(make_date(2000, month::int, 1), 'Month') as month_name,
    AVG(min_monthly_temp) as average_of_yearly_mins
FROM
    monthly_mins
GROUP BY
    month
ORDER BY
    month;