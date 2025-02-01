import os
import zipfile


def create_auth_proxy_extensions(name, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS):
    manifest_json = """
    {
    "version": "1.0.0",
    "manifest_version": 3,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "webRequest",
        "webRequestAuthProvider"
        ],
    "host_permissions": [
        "<all_urls>"
    ],
    "background": {
        "service_worker": "background.js"
    },
    "minimum_chrome_version":"22.0.0"
}
    """

    background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

    path = os.path.dirname(os.path.abspath(__file__))
    path = path + '\Chrome_extension'
    directory_path = path
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    manifest_file_path = os.path.join(directory_path, "manifest.json")
    with open(manifest_file_path, "w") as manifest_file:
        manifest_file.write(manifest_json)

    # Write background.js
    background_file_path = os.path.join(directory_path, "background.js")
    with open(background_file_path, "w") as background_file:
        background_file.write(background_js)