(import ..ks.point.p2 [P2])

(defn solve [stdin grid init]
  (defn grid-get [p] (get grid p.x p.y))
  (defn update [p move]
    (let
      [q (match move
            "U" p.west
            "D" p.east
            "L" p.south
            "R" p.north)]
      (if (and (chainc 0 <= q.x < (len grid))
               (chainc 0 <= q.y < (len (get grid 0)))
               (!= (grid-get q) " "))
        q p)))

  (setv pos (P2 init))
  (for [line stdin]
    (for [move (line.strip)]
      (setv pos (update pos move)))
    (yield (grid-get pos))))

(defn make [init grid]
  (fn [stdin]
    (.join "" (solve stdin grid init))))

(setv
  part1 (make #(1 1) ["123" "456" "789"])
  part2 (make #(2 2) ["  1  " " 234 " "56789" " ABC " "  D  "]))
