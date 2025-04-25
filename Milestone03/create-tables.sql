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

-- create: FINANCIAL_OBLIGATION table 
CREATE TABLE FINANCIAL_OBLIGATION(
    record_id INT NOT NULL,
    semester VARCHAR(50) NOT NULL,
    academic_year INT(4) NOT NULL,
    name VARCHAR(100) NOT NULL,
    total_due INT NOT NULL,
    due_date DATE NOT NULL,
    amount_paid DATE NOT NULL,
    organization_id INT NOT NULL,
    PRIMARY KEY(record_id),
    FOREIGN KEY(organization_id) REFERENCES ORGANIZATION(organization_id)
);

-- create: PAYMENT table
CREATE TABLE PAYMENT(
    payment_id INT NOT NULL,
    amount_paid VARCHAR(50) NOT NULL,
    payment_date INT(4) NOT NULL,
    record_id INT NOT NULL,
    member_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    PRIMARY KEY(payment_id),
    FOREIGN KEY(record_id) REFERENCES FINANCIAL_OBLIGATION(record_id),
    FOREIGN KEY(member_id, username) REFERENCES MEMBER(member_id, username)
);

-- create: ORGANIZATION table
CREATE TABLE ORGANIZATION (
    organization_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    number_of_members INT NOT NULL,
    PRIMARY KEY (organization_id)
);

-- create: SERVES table
CREATE TABLE SERVES (
    member_id INT NOT NULL,
    username VARCHAR(100) NOT NULL,
    organization_id INT NOT NULL,
    role VARCHAR(100) NOT NULL,
    school_year VARCHAR(10) NOT NULL,
    committee VARCHAR(100) NOT NULL,
    semester VARCHAR(10) NOT NULL,
    PRIMARY KEY (member_id, username, organization_id, role, school_year, committee, semester),
    FOREIGN KEY (organization_id) REFERENCES ORGANIZATION(organization_id),
    FOREIGN KEY (member_id, username) REFERENCES MEMBER(member_id, username)
);
