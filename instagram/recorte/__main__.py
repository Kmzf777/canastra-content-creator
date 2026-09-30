"""Ponto de entrada de `python -m instagram.recorte` -- delega para `cli.main`."""

from .cli import main

raise SystemExit(main())
