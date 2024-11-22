import json
import yaml


def main():
    with open("markers.yml") as markers_yml:
        dynmap_markers = yaml.load(markers_yml.read(), yaml.Loader)

    result = {
        "key": "markers",
        "label": "Markers",
        "markers": []
    }

    for key, data in dynmap_markers["sets"]["markers"]["markers"].items():
        if data['world'] != "oh_snap":
            continue

        result["markers"].append({
            "type": "icon",
            "data": {
                "key": key,
                "point": {
                    "x": data["x"],
                    "z": data["z"]
                },
                "image": f"dynmap_{data["icon"]}",
                "anchor": {
                    "x": 8,
                    "z": 8
                }
            },
            "options": {
                "tooltip": {
                    "content": data["label"],
                    "direction": 2,
                    "sticky": True
                }
            }
        })

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
