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
    [ group (info "2015") [%generate_days make_group "2015"]
    ; group (info "2016") [] ]

let () =
  let open Cmdliner.Cmd in
  exit @@ eval @@ cmd
