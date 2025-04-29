DROP TABLE IF EXISTS PAYMENT;
DROP TABLE IF EXISTS FINANCIAL_OBLIGATION;
DROP TABLE IF EXISTS SERVES;
DROP TABLE IF EXISTS MEMBER_DEGREE_PROGRAM;
DROP TABLE IF EXISTS ORGANIZATION;
DROP TABLE IF EXISTS MEMBER;

-- create: MEMBER table
CREATE TABLE MEMBER(
    member_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    batch INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    gender CHAR(1),
    is_admin BOOLEAN DEFAULT FALSE,
    PRIMARY KEY(member_id, username)
);

-- create: MEMBER_DEGREE_PROGRAM table
CREATE TABLE MEMBER_DEGREE_PROGRAM(
    member_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    degree_program VARCHAR(100) NOT NULL,
    PRIMARY KEY(member_id, username, degree_program),
    FOREIGN KEY(member_id, username) REFERENCES MEMBER(member_id, username)
);

-- create: ORGANIZATION table
CREATE TABLE ORGANIZATION (
    organization_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    number_of_members INT NOT NULL,
    PRIMARY KEY (organization_id)
);

-- create: FINANCIAL_OBLIGATION table 
CREATE TABLE FINANCIAL_OBLIGATION(
    record_id INT NOT NULL,
    semester VARCHAR(50) NOT NULL,
    academic_year INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    total_due INT NOT NULL,
    due_date DATE NOT NULL,
    organization_id INT NOT NULL,
    PRIMARY KEY(record_id),
    FOREIGN KEY(organization_id) REFERENCES ORGANIZATION(organization_id)
);

-- create: PAYMENT table
CREATE TABLE PAYMENT(
    payment_id INT NOT NULL,
    amount_paid DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
    payment_date DATE NOT NULL,
    record_id INT NOT NULL,
    member_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    PRIMARY KEY(payment_id),
    FOREIGN KEY(record_id) REFERENCES FINANCIAL_OBLIGATION(record_id),
    FOREIGN KEY(member_id, username) REFERENCES MEMBER(member_id, username)
);

-- create: SERVES table
CREATE TABLE SERVES (
    member_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    organization_id INT NOT NULL,
    role VARCHAR(100) NOT NULL,
    school_year VARCHAR(10) NOT NULL,
    committee VARCHAR(100) NOT NULL,
    semester VARCHAR(50) NOT NULL,
    PRIMARY KEY (member_id, username, organization_id, role, school_year, committee, semester),
    FOREIGN KEY (organization_id) REFERENCES ORGANIZATION(organization_id),
    FOREIGN KEY (member_id, username) REFERENCES MEMBER(member_id, username)
);

-- ADD: new member
INSERT INTO MEMBER(member_id, username, name, password, batch, status, gender, is_admin)
VALUES(1, 'jalonzo', 'Joejean Alonzo', '123456789', 2023, 'Active', 'F', FALSE); 
INSERT INTO MEMBER(member_id, username, name, password, batch, status, gender, is_admin)
VALUES(2, 'jpmonreal', 'Jomar Monreal', '123456789', 2023, 'Active', 'M', FALSE); 
INSERT INTO MEMBER(member_id, username, name, password, batch, status, gender, is_admin)
VALUES(3, 'blanot', 'Brian Lanot', '123456789', 2023, 'Active', 'M', FALSE); 
INSERT INTO MEMBER(member_id, username, name, password, batch, status, gender, is_admin)
VALUES(4, 'ttralala', 'Tralero Tralala', '123456789', 2023, 'Active', 'M', FALSE); 

-- ADD: member's degree program
INSERT INTO MEMBER_DEGREE_PROGRAM(member_id, username, degree_program)
VALUES(1, 'jalonzo', 'BSCS');

-- ADD: organization
INSERT INTO ORGANIZATION(organization_id, name, number_of_members)
VALUES(1, 'UPLB GDS', 39); 
INSERT INTO ORGANIZATION(organization_id, name, number_of_members)
VALUES(2, 'YCSS', 21); 

-- ADD: financial obligation
INSERT INTO FINANCIAL_OBLIGATION(record_id, semester, academic_year, name, total_due, due_date, organization_id)
VALUES(1, '1st semester', 2025, 'Membership Fee', 500, '2025-06-15', 1); 
INSERT INTO FINANCIAL_OBLIGATION(record_id, semester, academic_year, name, total_due, due_date, organization_id)
VALUES(2, '1st semester', 2025, 'FRA Fee', 1000, '2025-10-15', 2); 

-- ADD: payment
INSERT INTO PAYMENT(payment_id, amount_paid, payment_date, record_id, member_id, username)
VALUES(1, 100.00, '2025-10-25', 1, 1, 'jalonzo'); 
INSERT INTO PAYMENT(payment_id, amount_paid, payment_date, record_id, member_id, username)
VALUES(2, 100.00, '2025-04-25', 1, 1, 'jalonzo'); 
INSERT INTO PAYMENT(payment_id, amount_paid, payment_date, record_id, member_id, username)
VALUES(3, 400.00, '2025-10-25', 1, 1, 'jalonzo'); 
INSERT INTO PAYMENT(payment_id, amount_paid, payment_date, record_id, member_id, username)
VALUES(4, 500.00, '2025-10-25', 1, 2, 'jpmonreal'); 
INSERT INTO PAYMENT(payment_id, amount_paid, payment_date, record_id, member_id, username)
VALUES(5, 200.00, '2025-10-25', 2, 3, 'blanot'); 
INSERT INTO PAYMENT(payment_id, amount_paid, payment_date, record_id, member_id, username)
VALUES(6, 200.00, '2025-04-25', 2, 4, 'ttralala'); 

-- ADD: member role (SERVES)
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(1, 'jalonzo', 1, 'Member', '2024-2025', 'Member', '2nd semester');
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(2, 'jpmonreal', 1, 'Member', '2024-2025', 'Member', '1st semester');
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(3, 'blanot', 2, 'President', '2024-2025', 'Executive', '2nd semester');
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(4, 'ttralala', 1, 'Member', '2022-2023', 'Member', '2nd semester');
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(4, 'ttralala', 2, 'Member', '2022-2023', 'Member', '2nd semester');

-- UPDATE: member's status
UPDATE MEMBER
SET status = 'Active' 
WHERE member_id = 1 AND username = 'jalonzo'; 

-- UPDATE: degree program
UPDATE MEMBER_DEGREE_PROGRAM
SET degree_program = 'BSCA' 
WHERE member_id = 1 AND username = 'jalonzo'; 

-- UPDATE: amount due financial obligation
UPDATE FINANCIAL_OBLIGATION
SET total_due = 600
WHERE record_id = 1;

-- UPDATE: payment 
UPDATE PAYMENT
SET amount_paid = 200.00, payment_date = '2025-04-26'
WHERE payment_id = 1;

-- UPDATE: organization's number of members
UPDATE ORGANIZATION
SET number_of_members = 40
WHERE organization_id = 1;

-- UPDATE: member's role in SERVES
UPDATE SERVES
SET role = 'Member', committee = 'Pub', semester = '2nd semester'
WHERE member_id = 1 AND username = 'jalonzo' AND organization_id = 1;

--DELETE: FROM SERVES
DELETE FROM SERVES
WHERE member_id = 1 AND username = 'jalonzo';

--DELETE: FROM Payment
DELETE FROM PAYMENT
WHERE member_id = 1 AND username = 'jalonzo';

--DELETE: FROM Financial obligation
DELETE FROM FINANCIAL_OBLIGATION
WHERE record_id = 1; -- Adjust based on actual record_id

--DELETE: FROM MEMBER_DEGREE_PROGRAM
DELETE FROM MEMBER_DEGREE_PROGRAM
WHERE member_id = 1 AND username = 'jalonzo';

--DELETE: FROM MEMBER
DELETE FROM MEMBER
WHERE member_id = 1 AND username = 'jalonzo';

--DELETE: FROM ORGANIZATION
DELETE FROM ORGANIZATION
WHERE organization_id = 1; -- Adjust on actual organization_id 

--SEARCH MEMBER
SELECT * FROM MEMBER
WHERE member_id = 1 OR username = 'jalonzo';

-- SELECT: track member current roles
SELECT ranked.member_id, ranked.username, ranked.role, ranked.committee, ranked.semester
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY school_year DESC, FIELD(semester, 'First semester', 'Second semester', 'Mid semester') DESC) AS rn
    FROM SERVES
) ranked
WHERE rn = 1;

-- SELECT: track member status
SELECT member_id, username, status FROM MEMBER;

-- View members payment given semester and academic year
SELECT osmfp.mem_id as 'member_id', osmfp.full_name, osmfp.record_id, osmfp.name as 'obligation_name', osmfp.org_id as 'organization_id', osmfp.org_name, osmfp.academic_year, osmfp.semester, COALESCE(SUM(osmfp.amount_paid),0)  total_amount_paid, osmfp.total_due 
FROM (
    SELECT *
    FROM (
        SELECT *
        FROM (
            SELECT DISTINCT organization_id as `org_id`, name as 'org_name', member_id as 'mem_id', full_name FROM (
                SELECT *
                FROM (SELECT * FROM ORGANIZATION) o
                LEFT JOIN (SELECT organization_id as org_id, member_id as 'mem_id' FROM SERVES) s
                ON o.organization_id=s.org_id
            ) os
            LEFT JOIN (SELECT member_id, username, name as 'full_name', password, batch, status, gender, is_admin FROM MEMBER) m
            ON os.mem_id=m.member_id
        ) osm   
        LEFT JOIN  (
            SELECT * 
            FROM FINANCIAL_OBLIGATION
        ) fp
        ON osm.org_id=fp.organization_id
    ) r
    LEFT JOIN (
        SELECT payment_id, amount_paid, payment_date, record_id as 'p_record_id', member_id FROM PAYMENT
    ) p
    ON p.member_id = r.mem_id
) osmfp 
GROUP BY member_id, record_id, organization_id 


-- View all Presidents (or any other role) of a given organization for every academic year in reverse chronological order
SELECT member_id, username, role, school_year, semester 
FROM SERVES
WHERE role = 'Member'
ORDER BY 
  school_year DESC,
  FIELD(semester, '1st semester', '2nd semester', 'Mid semester') DESC;

--View all members of the organization by role, status, gender, degree program, batch (year of membership), and committee. (Note: we assume one committee membership only per organization per semester)
SELECT 
    m.member_id,
    m.username,
    m.name,
    m.status,
    m.gender,
    md.degree_program,
    m.batch,
    s.role,
    s.committee
FROM 
    MEMBER m
JOIN 
    MEMBER_DEGREE_PROGRAM md ON m.member_id = md.member_id AND m.username = md.username
JOIN 
    SERVES s ON m.member_id = s.member_id AND m.username = s.username
WHERE 
    s.organization_id = 1; -- Replace with the actual organization_id


-- View members for a given organization with unpaid membership fees or dues for a given semester and academic year
SELECT osmfp.mem_id as 'member_id', osmfp.full_name, osmfp.record_id, osmfp.name as 'obligation_name', osmfp.org_id as 'organization_id', osmfp.org_name, osmfp.academic_year, osmfp.semester, COALESCE(SUM(osmfp.amount_paid),0)  total_amount_paid, osmfp.total_due 
FROM (
    SELECT *
    FROM (
        SELECT *
        FROM (
            SELECT DISTINCT organization_id as `org_id`, name as 'org_name', member_id as 'mem_id', full_name FROM (
                SELECT *
                FROM (SELECT * FROM ORGANIZATION) o
                LEFT JOIN (SELECT organization_id as org_id, member_id as 'mem_id' FROM SERVES) s
                ON o.organization_id=s.org_id
            ) os
            LEFT JOIN (SELECT member_id, username, name as 'full_name', password, batch, status, gender, is_admin FROM MEMBER) m
            ON os.mem_id=m.member_id
        ) osm   
        LEFT JOIN  (
            SELECT * 
            FROM FINANCIAL_OBLIGATION
        ) fp
        ON osm.org_id=fp.organization_id
    ) r
    LEFT JOIN (
        SELECT payment_id, amount_paid, payment_date, record_id as 'p_record_id', member_id FROM PAYMENT
    ) p
    ON p.member_id = r.mem_id
) osmfp 
GROUP BY member_id, record_id, organization_id 
HAVING total_amount_paid < total_due and org_id = 1 and academic_year = 2025 and semester = '1st semester' ;

--View a member’s unpaid membership fees or dues for all their organizations (Member’s POV).
SELECT 
    m.member_id,
    m.username,
    o.name AS organization_name,
    fo.record_id,
    fo.semester,
    fo.academic_year,
    fo.total_due,
    fo.amount_paid,
    (fo.total_due - fo.amount_paid) AS amount_unpaid
FROM 
    MEMBER m
JOIN 
    PAYMENT p ON m.member_id = p.member_id AND m.username = p.username
JOIN 
    FINANCIAL_OBLIGATION fo ON p.record_id = fo.record_id
JOIN 
    ORGANIZATION o ON fo.organization_id = o.organization_id
WHERE 
    m.member_id = 1 AND m.username = 'jalonzo' -- Can replace with the actual member's ID and username
    AND (fo.total_due - fo.amount_paid) > 0;

--View all executive committee members of a given organization for a given academic year.
SELECT 
    m.member_id,
    m.username,
    m.name,
    s.role,
    s.committee,
    s.school_year
FROM 
    MEMBER m
JOIN 
    SERVES s ON m.member_id = s.member_id AND m.username = s.username
WHERE 
    s.organization_id = 1 AND -- Can replace with the actual organization ID
    s.school_year = '2024-2025' AND -- Can replace with the desired academic year
    s.role = 'Executive Committee'; 

-- View all late payments made by all members of a given organization for a given semester and academic year
SELECT osmfp.mem_id as 'member_id', osmfp.full_name, osmfp.record_id, osmfp.name as 'obligation_name', osmfp.org_id as 'organization_id', osmfp.org_name, osmfp.academic_year, osmfp.semester, COALESCE(osmfp.amount_paid, 0) 'amount_paid', osmfp.total_due , osmfp.payment_date, osmfp.due_date
FROM (
    SELECT *
    FROM (
        SELECT *
        FROM (
            SELECT DISTINCT organization_id as `org_id`, name as 'org_name', member_id as 'mem_id', full_name FROM (
                SELECT *
                FROM (SELECT * FROM ORGANIZATION) o
                LEFT JOIN (SELECT organization_id as org_id, member_id as 'mem_id' FROM SERVES) s
                ON o.organization_id=s.org_id
            ) os
            LEFT JOIN (SELECT member_id, username, name as 'full_name', password, batch, status, gender, is_admin FROM MEMBER) m
            ON os.mem_id=m.member_id
        ) osm   
        LEFT JOIN  (
            SELECT * 
            FROM FINANCIAL_OBLIGATION
        ) fp
        ON osm.org_id=fp.organization_id
    ) r
    LEFT JOIN (
        SELECT payment_id, amount_paid, payment_date, record_id as 'p_record_id', member_id FROM PAYMENT
    ) p
    ON p.member_id = r.mem_id
    WHERE (payment_date > due_date or payment_date is NULL) and academic_year = 2025 and semester = '1st semester' and org_id = 1
) osmfp 

-- View the total amount of unpaid and paid fees or dues of a given organization as of a given date.

SELECT grouped.organization_id, grouped.org_name, SUM(grouped.total_due - grouped.total_amount_paid) 'Amount unpaid'
FROM (
    SELECT osmfp.mem_id as 'member_id', osmfp.full_name, osmfp.record_id, osmfp.name as 'obligation_name', osmfp.org_id as 'organization_id', osmfp.org_name, osmfp.academic_year, osmfp.semester, COALESCE(SUM(osmfp.amount_paid),0)  total_amount_paid, osmfp.total_due 
    FROM (
        SELECT *
        FROM (
            SELECT *
            FROM (
                SELECT DISTINCT organization_id as `org_id`, name as 'org_name', member_id as 'mem_id', full_name FROM (
                    SELECT *
                    FROM (SELECT * FROM ORGANIZATION) o
                    LEFT JOIN (SELECT organization_id as org_id, member_id as 'mem_id' FROM SERVES) s
                    ON o.organization_id=s.org_id
                ) os
                LEFT JOIN (SELECT member_id, username, name as 'full_name', password, batch, status, gender, is_admin FROM MEMBER) m
                ON os.mem_id=m.member_id
            ) osm   
            LEFT JOIN  (
                SELECT * 
                FROM FINANCIAL_OBLIGATION
            ) fp
            ON osm.org_id=fp.organization_id
        ) r
        LEFT JOIN (
            SELECT payment_id, amount_paid, payment_date, record_id as 'p_record_id', member_id FROM PAYMENT
        ) p
        ON p.member_id = r.mem_id
    ) osmfp 
    GROUP BY member_id, record_id, organization_id 
) grouped
GROUP BY organization_id;

-- view all Presidents (or any other role) of a given organization for every academic year in reverse chronological order
SELECT 
    member_id, 
    username, 
    role, 
    school_year, 
    semester 
FROM 
    SERVES
WHERE 
    role = 'President'  -- replace 'President' with any other role (placeholder only)
    AND organization_id = 1  -- replace with the actual organization_id you want to filter by (placeholder only)
ORDER BY 
    school_year DESC, 
    FIELD(semester, '1st semester', '2nd semester', 'Mid semester') DESC;

-- view all members of the organization by role, status, gender, degree program, batch (year of membership), and committee
SELECT 
    m.member_id,
    m.username,
    m.name,
    m.status,
    m.gender,
    md.degree_program,
    m.batch,
    s.role,
    s.committee
FROM 
    MEMBER m
JOIN 
    MEMBER_DEGREE_PROGRAM md ON m.member_id = md.member_id AND m.username = md.username
JOIN 
    SERVES s ON m.member_id = s.member_id AND m.username = s.username
WHERE 
    s.organization_id = 1; --  replace with the actual organization_id you want to filter by (placeholder only)
