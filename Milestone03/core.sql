-- ADD: new member
INSERT INTO MEMBER(member_id, username, name, password, batch, status, gender, is_admin)
VALUES(1, 'jalonzo', 'Joejean Alonzo', '123456789', 2022, 'Active', 'F', FALSE);

-- ADD: member's degree program
INSERT INTO MEMBER_DEGREE_PROGRAM(member_id, username, degree_program)
VALUES(1, 'jalonzo', 'BSCS');

-- ADD: financial obligation
INSERT INTO FINANCIAL_OBLIGATION(record_id, semester, academic_year, name, total_due, due_date, amount_paid, organization_id)
VALUES(1, '2nd semester', 2025, 'Membership Fee', 500, '2025-06-15', 0.00, 1);

-- ADD: payment
INSERT INTO PAYMENT(amount_paid, payment_date, record_id, member_id, username)
VALUES(150.00, '2025-04-25', 1, 1, 'jalonzo');

-- ADD: organization
INSERT INTO ORGANIZATION(organization_id, name, number_of_members)
VALUES(1, 'UPLB GDS', 39);

-- ADD: member role (SERVES)
INSERT INTO SERVES(member_id, username, organization_id, role, school_year, committee, semester)
VALUES(1, 'jalonzo', 1, 'Member', '2024-2025', 'Member', '2nd Semester');

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
SET total_due = 600, amount_paid = 150.00
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
