from routpost_sdk import Plugin

plugin = Plugin("org.routpost.example-transformer", "0.1.0", ["transformer"])


@plugin.method("transform.run")
def transform(params):
    post = dict(params["post"])
    post["text"] = post.get("text", "") + params.get("settings", {}).get("suffix", "")
    return {"post": post}


if __name__ == "__main__":
    plugin.serve()
