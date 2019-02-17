#!/usr/bin/env python3
import os
import csv
import json
from flask import Flask, Response

app = Flask(__name__)


@app.route("/get-cases")
def get_cases():
    casefile_path = "casefiles/"
    csv_files = [os.path.abspath("{0}{1}".format(casefile_path, f)) for f in os.listdir(casefile_path) if f.endswith("csv")]
    datas = []
    for f in csv_files:
        data = {}
        with open(f) as fin:
            reader = csv.reader(fin, skipinitialspace=True, quotechar="'")
            ks = []
            for idx, row in enumerate(reader):
                if idx == 0:
                    for k in row:
                        data[k] = []
                        ks.append(k)
                else:
                    for i, val in enumerate(row):
                        data[ks[i]].append(val)
        datas.append(data)
    return Response(json.dumps(datas), mimetype="application/json")


@app.after_request
def allow_cross_domain(response: Response):
    """Hook to set up response headers."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'content-type'
    return response


if __name__ == "__main__":
    app.run("localhost", 8001)
