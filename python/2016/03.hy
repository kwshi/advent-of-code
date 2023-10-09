(import itertools :as it)

(defn parse [stdin]
  (gfor line stdin (map int (.split (line.strip)))))

(defn valid [a b c]
  (and
    (> (+ a b) c)
    (> (+ b c) a)
    (> (+ c a) b)))

(defn batched [i n]
  (let [i (iter i)]
    (while (setx batch (tuple (it.islice i n))) (yield batch))))

(defn wrap [f]
  (fn [stdin]
    (sum (it.starmap valid (f (parse stdin))))))

(defn [wrap] part1 [trs] trs)
(defn [wrap] part2 [trs]
  (it.chain #* (gfor chunk (batched trs 3) (zip #* chunk))))
