{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = inputs: let
    system = "x86_64-linux";
    pkgs = inputs.nixpkgs.legacyPackages.${system};

    python = pkgs.python312;
    ocamlPackages = pkgs.ocamlPackages;

    ocamlLibs = p:
      with p; [
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
      ];

    ocamlCore = p:
      with p; [
        ocaml
        findlib
        dune_3
        ocaml-lsp
      ];

    pythonLibs = p:
      with p; [
        #hy
        z3
        #sympy
        #numpy
        pytest
        hypothesis
      ];

    extraPackages = p:
      with p; [
        pup
      ];
  in {
    devShells.${system} = {
      ocaml = pkgs.mkShell {
        nativeBuildInputs = ocamlCore ocamlPackages;
        buildInputs = ocamlLibs ocamlPackages;
      };

      python = python.env;

      python-full = (python.withPackages pythonLibs).env;

      gleam = pkgs.mkShell {packages = with pkgs; [beamPackages.erlang gleam];};

      default = pkgs.mkShell {
        nativeBuildInputs =
          (ocamlCore ocamlPackages)
          ++ [(python.withPackages pythonLibs)];

        packages =
          extraPackages pkgs
          ++ ocamlLibs ocamlPackages
          ++ (with pkgs; [gleam]);
      };
    };
  };
}
