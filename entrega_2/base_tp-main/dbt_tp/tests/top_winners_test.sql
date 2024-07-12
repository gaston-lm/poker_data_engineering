SELECT *
FROM {{ ref('top_winners') }}
WHERE total_ganado <= 0