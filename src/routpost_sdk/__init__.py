"""Small synchronous JSON-RPC 2.0 stdio SDK for Routpost protocol v1."""
import json
import sys


class PluginError(Exception):
    def __init__(self, kind, message, retryable=False, retry_after_seconds=None):
        super().__init__(message)
        self.kind = kind
        self.retryable = retryable
        self.retry_after_seconds = retry_after_seconds


class Plugin:
    def __init__(self, plugin_id, version, capabilities):
        self.plugin_id = plugin_id
        self.version = version
        self.capabilities = capabilities
        self.handlers = {}

    def method(self, name):
        def register(handler):
            self.handlers[name] = handler
            return handler
        return register

    def serve(self):
        for line in sys.stdin:
            request = None
            try:
                request = json.loads(line)
                if request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
                    raise PluginError("validation_failed", "Invalid JSON-RPC request")
                method = request["method"]
                if method == "plugin.initialize":
                    if request.get("params", {}).get("protocol_version") != 1:
                        raise PluginError("validation_failed", "Incompatible protocol")
                    result = {"protocol_version": 1, "plugin_id": self.plugin_id,
                              "plugin_version": self.version, "capabilities": self.capabilities}
                elif method == "plugin.describe":
                    result = {"plugin_id": self.plugin_id, "capabilities": self.capabilities}
                elif method == "plugin.health":
                    result = {"status": "ok"}
                elif method == "plugin.shutdown":
                    result = {"ok": True}
                elif method in self.handlers:
                    result = self.handlers[method](request.get("params", {}))
                else:
                    response = {"jsonrpc": "2.0", "id": request.get("id"),
                                "error": {"code": -32601, "message": "Method not found"}}
                    print(json.dumps(response, ensure_ascii=False), flush=True)
                    continue
                response = {"jsonrpc": "2.0", "id": request.get("id"), "result": result}
            except PluginError as error:
                response = {"jsonrpc": "2.0", "id": request.get("id") if isinstance(request, dict) else None,
                            "error": {"code": 1000, "message": "Plugin operation failed",
                                      "data": {"kind": error.kind, "retryable": error.retryable,
                                               "retry_after_seconds": error.retry_after_seconds,
                                               "safe_message": str(error)}}}
            except Exception as error:
                print(f"plugin error: {type(error).__name__}", file=sys.stderr)
                response = {"jsonrpc": "2.0", "id": request.get("id") if isinstance(request, dict) else None,
                            "error": {"code": 1000, "message": "Plugin operation failed",
                                      "data": {"kind": "temporary_failure", "retryable": True,
                                               "safe_message": "Plugin operation failed"}}}
            print(json.dumps(response, ensure_ascii=False), flush=True)
            if isinstance(request, dict) and request.get("method") == "plugin.shutdown":
                break
