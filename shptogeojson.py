import shapefile
import json
import os

current_path = os.path.dirname(os.path.abspath(__file__))

def make_geo_json(path, output):
    sf = shapefile.Reader(path)

    fields = sf.fields[1:]
    field_names = [field[0] for field in fields]

    buffer = []
    for sr in sf.shapeRecords():
        atr = dict(zip(field_names, sr.record))

        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))

    geojson = open("{}".format(output), "w")
    geojson.write(json.dumps({"type": "FeatureCollection", "features": buffer}, indent=2, ensure_ascii=False))
    geojson.close()


if __name__ == "__main__":

    print("[Shp Converter] Find shp from {}\n".format(current_path))

    for (path, dir, files) in os.walk(current_path):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.shp':
                p = "{}/{}".format(path, filename)
                output = "{}/json/{}".format(current_path, "{}.json".format(filename.split(".shp")[0]))
                print("[Shp Converter] Read shp from {}".format(p))
                make_geo_json(p, output)
                print("[Shp Converter] Write to {}\n".format(output))