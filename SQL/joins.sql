    -- All joins in one query, one by one

CREATE TABLE categories(
    id INT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE products(
    id INT PRIMARY KEY,
    name VARCHAR(50) not null,
    price FLOAT,
    category_id INT NOT NULL,
    subpart_of_id INT
);

INSERT INTO categories VALUES
(1, 'electronics'), (2, 'clothing'), (3, 'automotive');

INSERT INTO products VALUES
(1, 'laptop', 1000.00, 1, NULL),
(2, 'shirt', 25.00, 2, NULL),
(3, 'laptop charger', 50.00, 1, 1),
(4, 'tire', 500.00, 3, NULL);

    -- INNER JOIN

SELECT P.name, C.name, P.price
FROM products P
INNER JOIN categories C ON P.category_id = C.id;

    -- CROSS JOIN

SELECT P.name, C.name
FROM products P
CROSS JOIN categories C;

    -- LEFT JOIN

SELECT P.name, C.name
FROM products P
LEFT JOIN categories C ON P.category_id = C.id;

    -- RIGHT JOIN

SELECT P.name, C.name
FROM products P
RIGHT JOIN categories C ON P.category_id = C.id;

    -- FULL JOIN

SELECT P.name, C.name
FROM products P
FULL OUTER JOIN categories C ON P.category_id = C.id;

    -- SELF JOIN

SELECT Psub.name AS Accessory_Name, Pmain.name AS Compatible_With
FROM products Psub
JOIN products Pmain ON Psub.subpart_of_id = Pmain.id;

    -- NATURAL JOIN

SELECT *
FROM products
NATURAL JOIN categories;

    