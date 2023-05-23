let t =
  let loc = Astlib.Location.none in
  let (module Ast_builder) = Ppxlib.Ast_builder.make loc in
  let open Ast_builder in
  ppat_constraint
    (ppat_var {txt= "hello"; loc})
    (ptyp_package ({txt= Lident "S"; loc}, []))

let () = Pprintast.pattern Format.std_formatter t
