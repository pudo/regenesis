

SELECT c.name, s.title_de, STRING_AGG(CONCAT(d.title_de, ' (', d.name, ')'), '; ')
  FROM cube c
  LEFT JOIN reference r ON c.name = r.cube_name
  LEFT JOIN dimension d ON d.name = r.dimension_name
  LEFT JOIN statistic s ON s.name = c.statistic_name
  WHERE c.name IN 
    (SELECT DISTINCT ic.name FROM cube ic 
     LEFT JOIN reference ir ON ic.name = ir.cube_name 
     WHERE ir.dimension_name='kreise')
  GROUP BY c.name, s.title_de
  ORDER BY COUNT(r.id) DESC;



  SELECT DISTINCT ic.name FROM cube ic LEFT JOIN reference ir ON ic.name = ir.cube_name WHERE ir.dimension_name='kreise'
