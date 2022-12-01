module type Day = sig
  val part1 : unit -> unit

  val part2 : unit -> unit
end

let run_simple f =
  let open Cmdliner.Term in
  const f $ const ()

let make_group s (module Day : Day) =
  let open Cmdliner.Cmd in
  group (info s)
    [v (info "1") @@ run_simple Day.part1; v (info "2") @@ run_simple Day.part2]

let cmd =
  let open Cmdliner.Cmd in
  group (info "ks-aoc")
    [ group (info "2015")
        (let open Year2015 in
        [ make_group "01" (module Day01)
        ; make_group "02" (module Day02)
        ; make_group "03" (module Day03)
        ; make_group "04" (module Day04)
        ; make_group "05" (module Day05)
        ; make_group "06" (module Day06)
        ; make_group "07" (module Day07)
        ; make_group "08" (module Day08)
        ; make_group "09" (module Day09)
        ; make_group "10" (module Day10) ] )
    ; group (info "2016") [] ]

let () =
  let open Cmdliner.Cmd in
  exit @@ eval @@ cmd
