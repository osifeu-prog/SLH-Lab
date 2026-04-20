"""
SLH Control Panel — unified dashboard server.

Serves control_panel.html and proxies API calls to:
  - control_api   (127.0.0.1:5050)  — system status, restart services
  - esp_bridge    (127.0.0.1:5002)  — ESP heartbeat + commands
  - system_bridge (127.0.0.1:5003)  — optional, for live system stats

Zero modifications to existing files. Safe to delete anytime.

Run:  cd D:\\AISITE && python panel.py
Open: http://127.0.0.1:8001/
"""
from flask import Flask, send_from_directory, request, Response, jsonify
from pathlib import Path
import urllib.request
import urllib.error
import json

BASE = Path(r"D:\AISITE")
SECURE = BASE / "secure"

app = Flask(__name__)

CONTROL_API = "http://127.0.0.1:5050"
ESP_BRIDGE  = "http://127.0.0.1:5002"
SYS_BRIDGE  = "http://127.0.0.1:5003"


def proxy_get(url: str, timeout: float = 2.0):
    """GET <url> and return (body_bytes, status_code)."""
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), r.status
    except urllib.error.HTTPError as e:
        return e.read(), e.code
    except Exception as e:
        err = json.dumps({"ok": False, "proxy_error": str(e)}).encode("utf-8")
        return err, 503


def proxy_post(url: str, payload: dict | None, timeout: float = 5.0):
    """POST json <payload> to <url> and return (body_bytes, status_code)."""
    try:
        data = json.dumps(payload or {}).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(), r.status
    except urllib.error.HTTPError as e:
        return e.read(), e.code
    except Exception as e:
        err = json.dumps({"ok": False, "proxy_error": str(e)}).encode("utf-8")
        return err, 503


# -------- Static files --------
@app.get("/")
def root():
    return send_from_directory(BASE, "control_panel.html")


@app.get("/secure/<path:fname>")
def secure_file(fname):
    return send_from_directory(SECURE, fname)


# -------- Health of proxy itself --------
@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "panel", "port": 8001})


# -------- Proxy: control_api (5050) --------
@app.get("/api/system/status")
def sys_status():
    body, code = proxy_get(f"{CONTROL_API}/api/system/status")
    return Response(body, code, content_type="application/json")


@app.post("/api/system/recover")
def sys_recover():
    body, code = proxy_post(f"{CONTROL_API}/api/system/recover", None, timeout=15)
    return Response(body, code, content_type="application/json")


@app.post("/api/system/start")
def sys_start():
    body, code = proxy_post(f"{CONTROL_API}/api/system/start", None, timeout=15)
    return Response(body, code, content_type="application/json")


@app.post("/api/system/stop")
def sys_stop():
    body, code = proxy_post(f"{CONTROL_API}/api/system/stop", None, timeout=15)
    return Response(body, code, content_type="application/json")


# -------- Proxy: esp_bridge (5002) --------
@app.get("/api/esp/health")
def esp_health():
    body, code = proxy_get(f"{ESP_BRIDGE}/health")
    return Response(body, code, content_type="application/json")


@app.get("/api/esp/status")
def esp_status():
    """Read esp_status.json directly (no need to hit the bridge)."""
    try:
        path = SECURE / "esp_status.json"
        if not path.exists():
            return jsonify({"ok": False, "error": "no status file yet"}), 200
        return Response(path.read_bytes(), 200, content_type="application/json")
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.post("/api/esp/command")
def esp_command():
    payload = request.get_json(force=True, silent=True) or {}
    body, code = proxy_post(f"{ESP_BRIDGE}/api/esp/command", payload)
    return Response(body, code, content_type="application/json")


@app.post("/api/esp/command/clear")
def esp_command_clear():
    body, code = proxy_post(f"{ESP_BRIDGE}/api/esp/command/clear", None)
    return Response(body, code, content_type="application/json")


# -------- Proxy: system_bridge (5003) — optional --------
@app.get("/api/system/stats")
def system_stats():
    body, code = proxy_get(f"{SYS_BRIDGE}/api/stats")
    return Response(body, code, content_type="application/json")


# -------- Combined status for the dashboard's top-bar --------
@app.get("/api/panel/summary")
def panel_summary():
    """One call → status of all 3 services + ESP + runtime."""
    out = {"services": {}}

    for name, url in [
        ("control_api", f"{CONTROL_API}/health"),
        ("esp_bridge",  f"{ESP_BRIDGE}/health"),
        ("system_bridge", f"{SYS_BRIDGE}/health"),
    ]:
        body, code = proxy_get(url, timeout=1.0)
        try:
            parsed = json.loads(body)
            ok = bool(parsed.get("ok"))
        except Exception:
            ok = (code == 200)
        out["services"][name] = {"up": ok, "http": code}

    # ESP live state
    esp_path = SECURE / "esp_status.json"
    if esp_path.exists():
        try:
            out["esp"] = json.loads(esp_path.read_text(encoding="utf-8"))
        except Exception as e:
            out["esp"] = {"error": str(e)}
    else:
        out["esp"] = None

    # Runtime (master_controller services map)
    rt_path = SECURE / "runtime_status.json"
    if rt_path.exists():
        try:
            out["runtime"] = json.loads(rt_path.read_text(encoding="utf-8-sig"))
        except Exception as e:
            out["runtime"] = {"error": str(e)}
    else:
        out["runtime"] = None

    return jsonify(out)


if __name__ == "__main__":
    print("=" * 60)
    print("  SLH Control Panel")
    print("  URL: http://127.0.0.1:8001/")
    print("  Proxies:")
    print("    /api/system/*  -> 127.0.0.1:5050 (control_api)")
    print("    /api/esp/*     -> 127.0.0.1:5002 (esp_bridge)")
    print("    /api/panel/summary (all-in-one)")
    print("=" * 60)
    app.run(host="127.0.0.1", port=8001, debug=False)
