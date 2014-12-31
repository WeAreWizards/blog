with import <nixpkgs> {};

pythonPackages.buildPythonPackage rec {
  name = "color-similarity";

  propagatedBuildInputs = with pythonPackages; [
    ipython
    matplotlib
    numpy
    pandas
    pillow
    scikitlearn
    scipy
  ];

  src = ./.;
}
