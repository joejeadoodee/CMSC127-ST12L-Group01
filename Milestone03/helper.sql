SELECT osmfp.mem_id, osmfp.full_name, osmfp.record_id, osmfp.name as 'obligation_name', osmfp.org_id, osmfp.org_name, osmfp.academic_year, osmfp.semester, SUM(osmfp.amount_paid) total_amount_paid, osmfp.total_due 
FROM (
    SELECT *
    FROM (
        SELECT DISTINCT organization_id as 'org_id', name as 'org_name', member_id as 'mem_id', full_name FROM (
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
GROUP BY member_id, record_id, organization_id 
HAVING total_amount_paid < total_due;