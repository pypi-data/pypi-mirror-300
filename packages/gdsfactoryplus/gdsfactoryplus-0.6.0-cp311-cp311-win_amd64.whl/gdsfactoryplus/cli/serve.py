import os
import pathlib
import sys
import threading
from typing import Literal

import gdsfactory as gf
import kfactory
import typer
import uvicorn
from fastapi import Body, HTTPException, Request
from fastapi.responses import HTMLResponse, PlainTextResponse

from ..pdk import PDK_CELL_NAMES
from ..settings import SETTINGS as s
from ..shared import import_pdk, maybe_find_docode_project_dir
from .app import app as cli
from .patch_netlist import changed as _changed
from .patch_netlist import modify_body as _modify_body
from .patch_netlist import patch_netlist_post as _patch_netlist_post
from .tree import _tree
from .watch import watch as _watch

try:
    from doweb.api.viewer import FileView, file_view_static
    from doweb.browser import get_app
except ImportError:
    from kweb.api.viewer import FileView, file_view_static
    from kweb.browser import get_app

PDK: str = s.pdk.name
PROJECT_DIR: str = maybe_find_docode_project_dir() or os.getcwd()


app = get_app(fileslocation=PROJECT_DIR, editable=False)


def needs_to_be_removed(path):
    if path.startswith("/file"):
        return True
    elif path.startswith("/gds"):
        return True


app.router.routes = [r for r in app.routes if not needs_to_be_removed(r.path)]  # type: ignore


def start_watcher(pdk, pre_build):
    path = os.path.join(PROJECT_DIR, s.name)
    try:
        return _watch(path, pdk, pre_build)
    except typer.Exit:
        return


@cli.command()
def serve(
    pdk: str = PDK,
    port: int = 8787,
    host: str = "0.0.0.0",
):
    kfactory.conf.config.cell_layout_cache = False

    os.chdir(PROJECT_DIR)

    global PDK

    if not pdk:
        pdk = PDK

    PDK = str(pdk).lower().strip()

    import_pdk(PDK).activate()
    for name in gf.get_active_pdk().cells:
        PDK_CELL_NAMES.add(name)

    print(f"{pdk=}\nproject_dir={PROJECT_DIR}\n{port=}\n{host=}", file=sys.stderr)

    uvicorn.run(
        "gdsfactoryplus.cli.serve:app",
        host=host,
        port=int(port),
        proxy_headers=True,
        reload=True,
    )


@app.post("/patch-netlist")
def patch_netlist_post(path: str, body: str = Body(...), schemapath: str = ""):
    content = _patch_netlist_post(path, body, schemapath, PDK)
    return PlainTextResponse(content)


@app.get("/patch-netlist")
def patch_netlist_get(path: str, schemapath: str = ""):
    content = _patch_netlist_post(path, "", schemapath, PDK)
    return PlainTextResponse(content)


@app.get("/pdk")
def pdk():
    return PlainTextResponse(PDK)


@app.get("/dir")
def project_dir():
    return PlainTextResponse(PROJECT_DIR)


@app.get("/tree")
def tree(
    path: str,
    by: Literal["cell", "file"] = "cell",
    key: str = "",
    none_str: str = "None",
):
    return PlainTextResponse(
        _tree(
            path,
            PDK,
            by,
            key,
            none_str,
            PDK_CELL_NAMES,
        )
    )


@app.get("/view2")
async def view2(
    request: Request,
    file: str,
    pdk: str = PDK,
    cell: str = "",
    rdb: str = "",
    theme: Literal["light", "dark"] = "dark",
):
    if pdk:
        assert PROJECT_DIR is not None
        layer_props = os.path.join(PROJECT_DIR, "build", "lyp", f"{pdk}.lyp")
        _pdk = import_pdk(pdk)
        layer_views = _pdk.layer_views
        assert layer_views is not None
        layer_views.to_lyp(filepath=layer_props)
    else:
        layer_props = None

    try:
        fv = FileView(
            file=pathlib.Path(file),
            cell=cell or None,
            layer_props=layer_props,
            rdb=rdb or None,
        )
        resp = await file_view_static(request, fv)  # type: ignore
    except HTTPException as e:
        print(e, file=sys.stderr)
        color = "#f5f5f5" if theme == "light" else "#121317"
        return HTMLResponse(f'<body style="background-color: {color}"></body>')
    body = resp.body.decode()
    body = _modify_body(resp.body.decode(), theme, file)
    return HTMLResponse(body)


@app.get("/changed")
async def changed(path: str):
    assert PROJECT_DIR is not None
    return _changed(PROJECT_DIR, path)
