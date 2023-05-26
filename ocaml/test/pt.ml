open Containers
open Fun.Infix
open Ks.Pt

let test_compare_p2 =
  QCheck_alcotest.to_alcotest
  @@
  let open QCheck in
  Test.make ~name:"P2.compare" (pair (pair int int) (pair int int))
  @@ fun (a, b) ->
  let a' = P2.from_tuple a in
  let b' = P2.from_tuple b in
  let cmp = Pair.compare Int.compare Int.compare a b in
  cmp = P2.compare a' b'

let test_compare_p3 =
  QCheck_alcotest.to_alcotest
  @@
  let open QCheck in
  Test.make ~name:"P3.compare" (pair (triple int int int) (triple int int int))
  @@ fun (a, b) ->
  let a' = P3.from_tuple a in
  let b' = P3.from_tuple b in
  let a'' = (a'.x, (a'.y, a'.z)) in
  let b'' = (b'.x, (b'.y, b'.z)) in
  let cmp =
    Pair.compare Int.compare (Pair.compare Int.compare Int.compare) a'' b''
  in
  cmp = P3.compare a' b'

let tests = [test_compare_p2; test_compare_p3]
