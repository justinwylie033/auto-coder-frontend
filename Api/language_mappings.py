LANGUAGE_MAPPINGS = {

  'python': {
    'image': 'python:3.8',  
    'command': 'python',
    'packages': 'pip install {}'
  },
  
  'javascript': {
    'image': 'node:latest',
    'command': 'node', 
    'packages': 'npm install {}'
  },
  
  'java': {
    'image': 'openjdk:11',
    'command': 'java',
    'packages': 'apt-get install {}'
  },

  'c#': {
    'image': 'mcr.microsoft.com/dotnet/sdk:6.0', 
    'command': 'dotnet run',
    'packages': 'dotnet add package {}'
  },

  'php': {
    'image': 'php:8.0',
    'command': 'php',
    'packages': 'composer require {}'
  },

  'ruby': {
    'image': 'ruby:3.0',
    'command': 'ruby',
    'packages': 'gem install {}'
  },

  'go': {
    'image': 'golang:1.18',
    'command': 'go run',
    'packages': 'go get {}'
  },

  'rust': {
    'image': 'rust:latest',
    'command': 'rustc',
    'packages': 'cargo add {}'
  },

  'swift': {
    'image': 'swift:5.5',
    'command': 'swift run',
    'packages': 'swift package install {}'    
  },

  'kotlin': {
    'image': 'kotlin:latest',
    'command': 'kotlinc',
    'packages': 'apt-get install {}'
  },

  'scala': {
    'image': 'scala:2.13',
    'command': 'scala',
    'packages': 'apt-get install {}'
  },

  'clojure':{
    'image': 'clojure:latest',
    'command': 'clj',
    'packages': 'clj -Sdeps "{}" {}'
  },

  'haskell': {
    'image': 'haskell:latest',
    'command': 'runhaskell',
    'packages': 'cabal install {}'
  },

  'perl': {
    'image': 'perl:latest', 
    'command': 'perl',
    'packages': 'cpan {}'
  },

  'r': {
    'image': 'r-base:latest',
    'command': 'Rscript',
    'packages': 'install.packages("{}")'
  },

  'julia': {
    'image': 'julia:latest',
    'command': 'julia',
    'packages': 'using Pkg; Pkg.add("{}")'
  },

  'lua': {
    'image': 'lua:latest',
    'command': 'lua', 
    'packages': 'luarocks install {}'
  },

  'ocaml': {
    'image': 'ocaml/opam:latest',
    'command': 'ocaml',
    'packages': 'opam install {}'
  },

  'fortran': {
    'image': 'fortran:latest',
    'command': 'gfortran',
    'packages': 'apt install {}'
  },
}