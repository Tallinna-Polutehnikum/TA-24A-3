SELECT s.id,
       s.filmi_id,
       m.pealkiri,
       s.saali_id,
       h.name,
       h.ekraani_tüüp,
       h.kino_id,
       c.kino_nimi,
       s.algus_aeg,
       s.lopu_aeg,
       s.keel,
       s.subtiitrid,
       s.alghind
FROM seansid AS s
JOIN filmid AS m ON m.id = s.filmi_id
JOIN kinosaalid AS h ON h.id = s.saali_id
JOIN kino AS c ON c.id = h.kino_id
ORDER BY s.algus_aeg, s.id;
