import argparse
import json

import yaml


def convert(world: str, key: str, label: str):
    with open("markers.yml") as markers_yml:
        dynmap_markers = yaml.load(markers_yml.read(), yaml.Loader)

    dynmap_set = dynmap_markers["sets"][key]

    result = {
        "key": key,
        "label": label,
        "defaultHidden": dynmap_set["hide"],
        "markers": [],
    }

    for marker_key, data in dynmap_set["markers"].items():
        if data["world"] != world:
            continue

        result["markers"].append(
            {
                "type": "icon",
                "data": {
                    "key": marker_key,
                    "point": {
                        "x": data["x"],
                        "z": data["z"],
                    },
                    "image": f"dynmap_{data["icon"]}",
                    "anchor": {
                        "x": 8,
                        "z": 8,
                    },
                },
                "options": {
                    "tooltip": {
                        "content": data["label"],
                        "direction": 2,
                        "sticky": True,
                    }
                },
            }
        )

    for marker_key, data in dynmap_set["lines"].items():
        if data["world"] != world:
            continue

        result["markers"].append(
            {
                "type": "line",
                "data": {
                    "key": marker_key,
                    "points": [
                        {
                            "x": x,
                            "z": z,
                        }
                        for x, z in zip(
                            data["x"],
                            data["z"],
                        )
                    ],
                },
                "options": {
                    "stroke": {
                        "weight": data["strokeWeight"],
                        "color": (
                            (round(data["strokeOpacity"] * 0xFF) << 24)
                            + data["strokeColor"]
                        ),
                    },
                    "tooltip": {
                        "content": data["label"],
                        "direction": 2,
                        "sticky": True,
                    },
                },
            }
        )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("world", type=str)
    parser.add_argument("key", type=str)
    parser.add_argument("label", type=str)

    args = parser.parse_args()

    convert(args.world, args.key, args.label)
