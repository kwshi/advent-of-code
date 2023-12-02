(import re)
(import collections :as co)
(import dataclasses :as dc)

(defclass [dc.dataclass] Room []
  #^ str name
  #^ int sector
  #^ str checksum)

(setv re-room (re.compile r"(.*)-(\d+)\[(\w+)\]\s*"))

(defn parse-room [#^ str name]
  (let [m (re-room.fullmatch name)]
    (assert (is-not m None))
    (Room (get m 1) (int (get m 2)) (get m 3))))
  
(defn get-checksum [#^ Room room]
  (let [count (co.Counter room.name)]
    (del (get count "-"))
    (.join "" (cut (sorted (count.keys)
      :key (fn [c] #((- (get count c)) c))) 5))))

(defn validate [#^ Room room]
  (= room.checksum (get-checksum room)))

(defn decipher-char [#^ str c #^ int n]
  (if (= c "-") " "
    (chr (+ (ord "a") (% (+ n (- (ord c) (ord "a"))) 26)))))

(defn decipher [#^ str s #^ int n]
  (.join "" (gfor c s (decipher-char c n))))

(defn wrap [f] (fn [stdin] (f (map parse-room stdin))))

(defn [wrap] part1 [rooms]
  (sum (gfor room rooms (* (validate room) room.sector))))

(defn [wrap] part2 [rooms]
  (for [room rooms]
    (when (= "northpole object storage" (decipher room.name room.sector))
      (return room.sector))))
