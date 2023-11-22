{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      ocamlPkgs = pkgs.ocamlPackages;
      pyPkgs = p: with p; [
        z3
        sympy
        numpy
        requests
        beautifulsoup4
      ];
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        nativeBuildInputs = (with ocamlPkgs; [ ocaml findlib dune_3 ocaml-lsp ]);

        buildInputs =
          (with pkgs; [
            pup
            #(python311.withPackages pyPkgs)
          ])
          ++ (with ocamlPkgs; [
            containers
            alcotest
            angstrom
            iter
            yojson
            re
            re2
            fmt
            ppx_deriving
            ppx_derivers
            qcheck
            qcheck-alcotest
          ])
        ;
      };
    };
}
