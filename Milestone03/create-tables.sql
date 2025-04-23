-- create: MEMBER table
CREATE TABLE MEMBER(
    member_id INT NOT NULL,
    username VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    batch INT,
    status VARCHAR(50),
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

-- create: FINANCIAL_OBLIGATION(Org_id) table 



-- create: PAYMENT table



-- create: ORGANIZATION table



-- create: SERVES table

