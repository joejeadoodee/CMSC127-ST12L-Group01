DROP TABLE IF EXISTS PAYMENT;
DROP TABLE IF EXISTS FINANCIAL_OBLIGATION;
DROP TABLE IF EXISTS SERVES;
DROP TABLE IF EXISTS MEMBER_DEGREE_PROGRAM;
DROP TABLE IF EXISTS ORGANIZATION;
DROP TABLE IF EXISTS MEMBER;

-- create: MEMBER table
CREATE TABLE MEMBER(
    member_id INT AUTO_INCREMENT  NOT NULL,
    username VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    batch INT NOT NULL,
    status VARCHAR(50) NOT NULL,
    gender CHAR(1),
    is_admin BOOLEAN DEFAULT FALSE,
    graduation_date DATE,
    PRIMARY KEY(member_id, username)
);

-- create: MEMBER_DEGREE_PROGRAM table
CREATE TABLE MEMBER_DEGREE_PROGRAM(
    member_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    degree_program VARCHAR(100) NOT NULL,
    PRIMARY KEY(member_id, username, degree_program),
    FOREIGN KEY(member_id, username) REFERENCES MEMBER(member_id, username) ON DELETE CASCADE
);

-- create: ORGANIZATION table
CREATE TABLE ORGANIZATION (
    organization_id INT AUTO_INCREMENT NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    number_of_members INT NOT NULL,
    PRIMARY KEY (organization_id)
);

-- create: FINANCIAL_OBLIGATION table 
CREATE TABLE FINANCIAL_OBLIGATION(
    record_id INT AUTO_INCREMENT NOT NULL,
    semester VARCHAR(50) NOT NULL,
    academic_year INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    total_due INT NOT NULL,
    due_date DATE NOT NULL,
    organization_id INT NOT NULL,
    PRIMARY KEY(record_id),
    FOREIGN KEY(organization_id) REFERENCES ORGANIZATION(organization_id) ON DELETE CASCADE
);

-- create: PAYMENT table
CREATE TABLE PAYMENT(
    payment_id INT AUTO_INCREMENT NOT NULL,
    amount_paid DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
    payment_date DATE NOT NULL,
    record_id INT NOT NULL,
    member_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    PRIMARY KEY(payment_id),
    FOREIGN KEY(record_id) REFERENCES FINANCIAL_OBLIGATION(record_id) ON DELETE CASCADE,
    FOREIGN KEY(member_id, username) REFERENCES MEMBER(member_id, username) ON DELETE CASCADE
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
    FOREIGN KEY (organization_id) REFERENCES ORGANIZATION(organization_id) ON DELETE CASCADE,
    FOREIGN KEY (member_id, username) REFERENCES MEMBER(member_id, username) ON DELETE CASCADE
);

-- ADD: new member
INSERT INTO MEMBER(member_id, username, name, password, batch, status, gender, is_admin)
VALUES(1, 'jalonzo', 'Joejean Alonzo', '1234', 2023, 'Active', 'F', FALSE); 
INSERT INTO MEMBER(member_id, username, name, password, batch, status, gender, is_admin)
VALUES(2, 'jpmonreal', 'Jomar Monreal', '1234', 2023, 'Active', 'M', FALSE); 
INSERT INTO MEMBER(member_id, username, name, password, batch, status, gender, is_admin)
VALUES(3, 'blanot', 'Brian Lanot', '1234', 2023, 'Active', 'M', FALSE); 
INSERT INTO MEMBER(member_id, username, name, password, batch, status, gender, is_admin)
VALUES(4, 'ttralala', 'Tralero Tralala', '1234', 2023, 'Inactive', 'M', TRUE); 
INSERT INTO MEMBER(member_id, username, name, password, batch, status, gender, is_admin, graduation_date)
VALUES(5, 'aalde', 'Aaron Alde', '1234', 2024, 'Graduated', 'M', TRUE, '2025-12-15'); 

-- ADD: member's degree program
INSERT INTO MEMBER_DEGREE_PROGRAM(member_id, username, degree_program)
VALUES(1, 'jalonzo', 'BSCS');
INSERT INTO MEMBER_DEGREE_PROGRAM(member_id, username, degree_program)
VALUES(2, 'jpmonreal', 'BSCS');
INSERT INTO MEMBER_DEGREE_PROGRAM(member_id, username, degree_program)
VALUES(3, 'blanot', 'BSCS');
INSERT INTO MEMBER_DEGREE_PROGRAM(member_id, username, degree_program)
VALUES(4, 'ttralala', 'BSA');
INSERT INTO MEMBER_DEGREE_PROGRAM(member_id, username, degree_program)
VALUES(5, 'aalde', 'BSA');

-- ADD: organization
INSERT INTO ORGANIZATION(organization_id, name, password, number_of_members)
VALUES(1, 'UPLB GDS', '1234', 39); 
INSERT INTO ORGANIZATION(organization_id, name, password, number_of_members)
VALUES(2, 'YCSS', '1234', 21); 
INSERT INTO ORGANIZATION(organization_id, name, password, number_of_members)
VALUES(3, 'BAKA', '1234', 25); 

-- ADD: financial obligation
INSERT INTO FINANCIAL_OBLIGATION(record_id, semester, academic_year, name, total_due, due_date, organization_id)
VALUES(1, '1st semester', 2025, 'Membership Fee', 500, '2025-06-15', 1); 
INSERT INTO FINANCIAL_OBLIGATION(record_id, semester, academic_year, name, total_due, due_date, organization_id)
VALUES(2, '1st semester', 2025, 'FRA Fee', 1000, '2025-10-15', 2); 
INSERT INTO FINANCIAL_OBLIGATION(record_id, semester, academic_year, name, total_due, due_date, organization_id)
VALUES(3, '1st semester', 2025, 'Orientation Fee', 1000, '2025-10-15', 2); 

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
VALUES(1, 'jalonzo', 1, 'Secretary', '2024-2025', 'Pub', '2nd semester');
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(2, 'jpmonreal', 1, 'Member', '2024-2025', 'Member', '1st semester');
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(2, 'jpmonreal', 3, 'Member', '2024-2025', 'Pub', '1st semester');
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(3, 'blanot', 2, 'President', '2024-2025', 'Executive', '2nd semester');
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(4, 'ttralala', 2, 'Member', '2022-2023', 'Pub', '2nd semester');
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(4, 'ttralala', 2, 'President', '2024-2025', 'Pub', '2nd semester');
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(5, 'aalde', 2, 'Member', '2022-2023', 'Finance', '2nd semester');
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(5, 'aalde', 2, 'President', '2023-2024', 'Finance', '2nd semester');

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



--SEARCH MEMBER
SELECT * FROM MEMBER
WHERE member_id = 1 OR username = 'jalonzo';

-- SELECT: track member current roles
SELECT ranked.member_id, ranked.username, ranked.role, ranked.committee, ranked.semester
FROM (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY school_year DESC, FIELD(semester, '1st semester', '2nd semester', 'Mid semester') DESC) AS rn
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
GROUP BY member_id, record_id, organization_id;


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
        SERVES s
    LEFT JOIN 
        MEMBER m
    ON m.member_id = s.member_id
    LEFT JOIN
        MEMBER_DEGREE_PROGRAM md
    ON m.member_id = md.member_id
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
GROUP BY member_id, record_id, organization_id;

--View a member’s unpaid membership fees or dues for all their organizations (Member’s POV).
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
HAVING total_amount_paid < total_due AND osmfp.mem_id = 4;  -- Can replace with member id

--View all executive committee members of a given organization for a given academic year.
SELECT 
    m.member_id,
    m.username,
    m.name,
    s.role,
    s.committee,
    s.school_year,
    s.organization_id
FROM 
    MEMBER m
JOIN 
    SERVES s ON m.member_id = s.member_id AND m.username = s.username
WHERE 
    s.organization_id = 2 AND -- Can replace with the actual organization ID
    s.school_year = '2024-2025' AND -- Can replace with the desired academic year
    s.role != 'Member'; 

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
) osmfp;

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

-- View the percentage of active vs inactive members of a given organization for the last n semesters
-- Note: n = 5 (change as needed)

SELECT 
    s.organization_id,
    SUM(CASE WHEN m.status = 'Active' THEN 1 ELSE 0 END) AS active_members,
    SUM(CASE WHEN m.status = 'Inactive' OR m.status = 'Graduated' THEN 1 ELSE 0 END) AS inactive_members,
    COUNT(*) AS total_members,
    ROUND((SUM(CASE WHEN m.status = 'Active' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS active_percentage,
    ROUND((SUM(CASE WHEN m.status = 'Inactive' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS inactive_percentage
FROM 
    MEMBER m
JOIN 
    SERVES s ON m.member_id = s.member_id AND m.username = s.username
WHERE 
    s.organization_id = 1 -- Replace with desired org ID
    AND CAST(LEFT(s.school_year, 4) AS UNSIGNED) >= (YEAR(CURDATE()) - FLOOR(5 / 2)) -- Adjust based on n semesters
    AND s.semester IN ('1st semester', '2nd semester', 'Mid semester')
GROUP BY 
    s.organization_id



-- View all alumni members of a given organization as of a given date.
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
    MEMBER_DEGREE_PROGRAM md ON m.member_id = md.member_id
JOIN 
    SERVES s ON m.member_id = s.member_id
WHERE 
    s.organization_id = 1 -- replace with the actual organization_id
    AND m.status = 'alumni'
    AND m.batch <= YEAR('2025-04-29') -- replace with the given date
ORDER BY 
    m.name;


-- View amount paid
SELECT s.member_id, m.username, o.name, f.record_id, f.name as `obligation_name`, f.semester, f.academic_year, f.total_due, f.due_date, 
COALESCE(p.total_amount_paid, 0) as `total_amount_paid`
FROM SERVES s
LEFT JOIN MEMBER m
ON s.member_id=m.member_id
LEFT JOIN ORGANIZATION o
ON o.organization_id=s.organization_id
LEFT JOIN FINANCIAL_OBLIGATION f
ON o.organization_id=f.organization_id
LEFT JOIN (
    SELECT record_id, member_id, SUM(amount_paid) `total_amount_paid`
    FROM PAYMENT p
    GROUP BY record_id, member_id
) p
ON f.record_id=p.record_id AND s.member_id=p.member_id
WHERE f.record_id IS NOT NULL
ORDER BY s.member_id, o.name, f.name;


--View payment history
SELECT 
    p.payment_id, 
    m.username,
    SUM(p.amount_paid), 
    p.payment_date
FROM PAYMENT p 
LEFT JOIN FINANCIAL_OBLIGATION f
    ON f.record_id = p.record_id
LEFT JOIN ORGANIZATION o
    ON f.organization_id = o.organization_id
LEFT JOIN MEMBER m
    ON m.member_id = p.member_id
WHERE f.record_id = {insert here}
GROUP BY
    m.username
ORDER BY 
    p.member_id, 
    o.name, 
    f.name, 
    p.payment_date DESC;



--View members for a given organization with unpaid membership fees or dues for a given semester and academic year.
SELECT DISTINCT r.username, r.obligation_name, r.unpaid_amount  FROM (
    SELECT s.member_id, m.username, o.organization_id, o.name, f.record_id, f.name as `obligation_name`, f.semester, f.academic_year, f.total_due, f.due_date, 
    COALESCE(p.total_amount_paid, 0) as `total_amount_paid`,
    (f.total_due - COALESCE(p.total_amount_paid, 0)) AS `unpaid_amount`
    FROM SERVES s
    LEFT JOIN MEMBER m
    ON s.member_id=m.member_id
    LEFT JOIN ORGANIZATION o
    ON o.organization_id=s.organization_id
    LEFT JOIN FINANCIAL_OBLIGATION f
    ON o.organization_id=f.organization_id
    LEFT JOIN (
        SELECT record_id, member_id, SUM(amount_paid) `total_amount_paid`
        FROM PAYMENT p
        GROUP BY record_id, member_id
    ) p
    ON f.record_id=p.record_id AND s.member_id=p.member_id
    WHERE f.record_id IS NOT NULL AND o.organization_id = 2 AND (f.total_due - COALESCE(p.total_amount_paid, 0)) > 0
    ORDER BY s.member_id, o.name, f.name
) r
ORDER BY r.name, `unpaid_amount` DESC;



SELECT 
    SUM(sub.total_amount_paid) AS total_paid,
    SUM(sub.total_due - sub.total_amount_paid) AS total_unpaid
FROM (
    SELECT 
        s.member_id, 
        m.username, 
        o.name AS organization_name, 
        f.record_id, 
        f.name AS obligation_name, 
        f.semester, 
        f.academic_year, 
        f.total_due, 
        f.due_date, 
        COALESCE(p.total_amount_paid, 0) AS total_amount_paid,
        o.organization_id
    FROM SERVES s
    LEFT JOIN MEMBER m ON s.member_id = m.member_id
    LEFT JOIN ORGANIZATION o ON o.organization_id = s.organization_id
    LEFT JOIN FINANCIAL_OBLIGATION f ON o.organization_id = f.organization_id
    LEFT JOIN (
        SELECT record_id, member_id, SUM(amount_paid) AS total_amount_paid
        FROM PAYMENT
        GROUP BY record_id, member_id
    ) p ON f.record_id = p.record_id AND s.member_id = p.member_id
    WHERE f.record_id IS NOT NULL AND o.organization_id = 2               -- ← your target organization_id
) AS sub;
