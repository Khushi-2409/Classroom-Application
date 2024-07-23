-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
SELECT teacher_id, COUNT(*) AS count_grade_A
FROM assignments
WHERE grade = 'A'
GROUP BY teacher_id
ORDER BY count_grade_A DESC
LIMIT 1;