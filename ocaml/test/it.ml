open Containers
open Alcotest

let format_int_list l =
  "[" ^ (String.concat " " @@ List.map Int.to_string l) ^ "]"

let test_slinky () =
  [ ([], [([], [])])
  ; ([1], [([], [1]); ([1], [])])
  ; ([3; 5], [([], [3; 5]); ([3], [5]); ([5; 3], [])])
  ; ([2; 3; 4], [([], [2; 3; 4]); ([2], [3; 4]); ([3; 2], [4]); ([4; 3; 2], [])])
  ]
  |> List.iter
     @@ fun (input, output) ->
     check (list @@ pair (list int) (list int)) (format_int_list input) output
     @@ Iter.to_list @@ Ks.It.slinky input

let test_slinky1 () =
  [([], []); ([3], [([], 3, [])])]
  |> List.iter
     @@ fun (input, output) ->
     check
       (list @@ triple (list int) int (list int))
       (format_int_list input) output
     @@ Iter.to_list @@ Ks.It.slinky1 input

let test_perms () =
  [ ([], [[]])
  ; ([3], [[3]])
  ; ([2; 1], [[2; 1]; [1; 2]])
  ; ( [1; 2; 3]
    , [[1; 2; 3]; [1; 3; 2]; [2; 1; 3]; [2; 3; 1]; [3; 1; 2]; [3; 2; 1]] ) ]
  |> List.iter
     @@ fun (input, output) ->
     check (list @@ list int) (format_int_list input) output
     @@ Iter.to_list @@ Ks.It.perms input

let tests =
  [ test_case "slinky" `Quick test_slinky
  ; test_case "slinky1" `Quick test_slinky1
  ; test_case "perms" `Quick test_perms ]
