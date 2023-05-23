open Containers
open Fun.Infix

let find_modules =
  let entry_regexp =
    let open Re in
    compile @@ seq [bos; str "day"; group @@ seq [digit; digit]; str ".ml"; eos]
  in
  let get_module =
    Re.exec_opt entry_regexp %> Option.map (fun group -> Re.Group.get group 1)
  in
  Sys.readdir %> Array.to_list %> List.filter_map get_module

let extractor =
  let open Ppxlib.Ast_pattern in
  single_expr_payload @@ pexp_loc __
  @@ pexp_apply __ ((nolabel ** estring __') ^:: nil)

let expander :
       ctxt:Ppxlib.Expansion_context.Extension.t
    -> Ppxlib.Location.t
    -> Parsetree.expression
    -> string Astlib.Location.loc
    -> Parsetree.expression =
 fun ~ctxt apply_loc fn year ->
  let root_loc = Ppxlib.Expansion_context.Extension.extension_point_loc ctxt in
  let root_loc' = {root_loc with loc_ghost= true} in
  let year_loc' = {year.loc with loc_ghost= true} in
  let open Ppxlib.Ast_builder.Default in
  match find_modules year.txt with
  | exception err ->
      pexp_extension ~loc:root_loc'
      @@ Ppxlib.Location.error_extensionf ~loc:year.loc "%s"
      @@ Printexc.to_string err
  | modules ->
      elist ~loc:root_loc'
      @@ List.map
           (fun day ->
             eapply ~loc:apply_loc fn
               [ estring ~loc:year.loc year.txt
               ; pexp_pack ~loc:year_loc'
                 @@ pmod_ident ~loc:year_loc'
                      { loc= year_loc'
                      ; txt= Ldot (Lident ("Year" ^ year.txt), "Day" ^ day) } ]
             )
           modules

let extension =
  Ppxlib.Extension.V3.declare "generate_days"
    Ppxlib.Extension.Context.expression extractor expander

let () =
  Ppxlib.Driver.register_transformation
    ~rules:[Ppxlib.Context_free.Rule.extension extension]
    "ks-aoc:generate_days"
