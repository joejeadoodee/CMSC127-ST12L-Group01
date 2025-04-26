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
    payment_id INT NOT NULL AUTO_INCREMENT,
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
VALUES(4, 'ttralala', 'Tralero Tralal', '123456789', 2023, 'Active', 'M', FALSE); 

-- ADD: member's degree program
INSERT INTO MEMBER_DEGREE_PROGRAM(member_id, username, degree_program)
VALUES(1, 'jalonzo', 'BSCS');

-- ADD: organization
INSERT INTO ORGANIZATION(organization_id, name, number_of_members)
VALUES(1, 'UPLB GDS', 39); 

-- ADD: financial obligation
INSERT INTO FINANCIAL_OBLIGATION(record_id, semester, academic_year, name, total_due, due_date, organization_id)
VALUES(3, '1st semester', 2025, 'Membership Fee', 500, '2025-06-15', 2); 

-- ADD: payment
INSERT INTO PAYMENT(payment_id, amount_paid, payment_date, record_id, member_id, username)
VALUES(6, 500.00, '2025-10-25', 3, 1, 'jalonzo'); 

-- ADD: member role (SERVES)
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(1, 'jalonzo', 1, 'Member', '2024-2025', 'Member', '2nd semester');

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
SET total_due = 600,
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

-- SELECT: track member current roles
SELECT ranked.member_id, ranked.username, ranked.role
FROM (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY member_id ORDER BY school_year DESC, FIELD(semester, 'First semester', 'Second semester', 'Mid semester') DESC) AS rn
  FROM SERVES
) ranked
WHERE rn = 1;

-- SELECT: track member status
SELECT member_id, username, status FROM MEMBER;

-- View members payment given semester and academic year


-- View members for a given organization with unpaid membership fees or dues for a given semester and academic year
SELECT osmfp.mem_id as 'member_id', osmfp.full_name, osmfp.record_id, osmfp.name as 'obligation_name', osmfp.org_id as 'organization_id', osmfp.org_name, osmfp.academic_year, osmfp.semester, SUM(osmfp.amount_paid) total_amount_paid, osmfp.total_due 
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
        FROM FINANCIAL_OBLIGATION f
        LEFT JOIN (SELECT payment_id, amount_paid, payment_date, record_id as 'p_record_id', member_id FROM PAYMENT) p
        ON f.record_id=p.p_record_id
    ) fp
    ON osm.mem_id=fp.member_id
) osmfp 
WHERE org_id = 1
GROUP BY member_id, record_id, organization_id 
HAVING total_amount_paid < total_due or osmfp.record_id is NULL;


-- View all late payments made by all members of a given organization for a given semester and academic year
SELECT osmfp.mem_id as 'member_id', osmfp.full_name, osmfp.record_id, osmfp.name as 'obligation_name', osmfp.org_id as 'organization_id', osmfp.org_name, osmfp.academic_year, osmfp.semester, osmfp.total_due, osmfp.payment_date, osmfp.due_date 
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
        FROM FINANCIAL_OBLIGATION f
        LEFT JOIN (SELECT payment_id, amount_paid, payment_date, record_id as 'p_record_id', member_id FROM PAYMENT) p
        ON f.record_id=p.p_record_id
    ) fp
    ON osm.mem_id=fp.member_id
    WHERE payment_date > due_date
) osmfp 


