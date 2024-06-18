{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.05";
    systems.url = "github:nix-systems/default";
  };

  outputs = {
    self,
    nixpkgs,
    systems,
    ...
  }: let
    forAllSystems = f: nixpkgs.lib.genAttrs (import systems) (s: f nixpkgs.legacyPackages.${s});
  in {
    packages = forAllSystems (pkgs: {
      default = pkgs.stdenv.mkDerivation {
        pname = "redes-projeto";
        version = self.lastModifiedDate;
        src = ./.;
        buildInputs = [pkgs.texliveFull pkgs.pandoc];
        buildPhase = ''
          latexmk
        '';
        installPhase = ''
          mkdir -p $out
          cp build/*.pdf $out/
        '';
      };
    });
  };
}
