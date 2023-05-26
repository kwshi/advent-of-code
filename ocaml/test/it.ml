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

let factorial =
  let rec go acc n = if n <= 0 then acc else go (n * acc) (n - 1) in
  go 1

let test_perms' =
  let check input =
    let perms = Ks.It.perms input in
    let len = List.length input in
    Iter.length perms = factorial len
    && Iter.sorted ~cmp:(List.compare Int.compare) perms
  in
  QCheck_alcotest.to_alcotest
  @@
  let open QCheck in
  let input =
    list_of_size Gen.(int_range 0 8) int
    |> map ~rev:Fun.id @@ List.sort_uniq ~cmp:Int.compare
  in
  Test.make ~name:"perms (qcheck)" input check

let tests =
  [ test_case "slinky" `Quick test_slinky
  ; test_case "slinky1" `Quick test_slinky1
  ; test_case "perms" `Quick test_perms
  ; test_perms' ]
