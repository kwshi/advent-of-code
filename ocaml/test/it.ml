open Containers
open Alcotest

let format_int_list l =
  "[" ^ (String.concat " " @@ List.map Int.to_string l) ^ "]"

let test_slinky =
  let open List.Infix in
  let+ input, output =
    [ ([], [([], [])])
    ; ([1], [([], [1]); ([1], [])])
    ; ([3; 5], [([], [3; 5]); ([3], [5]); ([5; 3], [])])
    ; ( [2; 3; 4]
      , [([], [2; 3; 4]); ([2], [3; 4]); ([3; 2], [4]); ([4; 3; 2], [])] ) ]
  in
  test_case (format_int_list input) `Quick
  @@ fun () ->
  check (list @@ pair (list int) (list int)) "expected output" output
  @@ Iter.to_list @@ Ks.It.slinky input

let test_slinky1 =
  let open List.Infix in
  let+ input, output = [([], []); ([3], [([], 3, [])])] in
  test_case (format_int_list input) `Quick
  @@ fun () ->
  check (list @@ triple (list int) int (list int)) "expected output" output
  @@ Iter.to_list @@ Ks.It.slinky1 input

let test_perms =
  let open List.Infix in
  let+ input, output =
    [ ([], [[]])
    ; ([3], [[3]])
    ; ([2; 1], [[2; 1]; [1; 2]])
    ; ( [1; 2; 3]
      , [[1; 2; 3]; [1; 3; 2]; [2; 1; 3]; [2; 3; 1]; [3; 1; 2]; [3; 2; 1]] ) ]
  in
  test_case (format_int_list input) `Quick
  @@ fun () ->
  check (list @@ list int) ("perms " ^ format_int_list input) output
  @@ Iter.to_list @@ Ks.It.perms input

let () =
  run "it"
    [("slinky", test_slinky); ("slinky1", test_slinky1); ("perms", test_perms)]
