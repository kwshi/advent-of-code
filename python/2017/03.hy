(import itertools :as it)

(defn part1 [stdin]
  (setv n (int (stdin.read)))
  (for [i (it.count 1 2)]
    (when (>= (* i i) n) (break)))
  (setv l (% (- (* i i) n) (- i 1)))
  (setv d (abs (- l (// i 2))))
  (+ d (// i 2)))
