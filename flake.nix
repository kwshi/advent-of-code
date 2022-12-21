{
  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = inputs:
    let
      system = "x86_64-linux";
      pkgs = inputs.nixpkgs.legacyPackages.${system};
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
        buildInputs = with pkgs; [ pup (python311.withPackages pyPkgs) ];
      };
    };
}
