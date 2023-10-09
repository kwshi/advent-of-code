(defn traverse [stdin]
  (setv steps (.split (.strip (stdin.read)) ", "))
  (setv [dx dy] [1 0] [x y] [0 0])
  (yield #(x y))
  (for [step steps]
    (setv [dx dy]
      (match (get step 0)
        "L" [dy (- dx)]
        "R" [(- dy) dx]))
    (for [_ (range (int (cut step 1 None)))]
      (+= x dx) (+= y dy)
      (yield #(x y)))))

(defn wrap [f]
  (fn [stdin]
    (sum (map abs (f (traverse stdin))))))

(defn [wrap] part1 [ps]
  (get (list ps) -1))

(defn [wrap] part2 [ps]
  (setv seen #{})
  (for [p ps]
    (when (in p seen) (return p))
    (seen.add p)))
