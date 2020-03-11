import jsonlines
import json

with open('tracker.json', 'r') as f:
    json_data = json.load(f)

with jsonlines.open('tracker_lines.jsonl', 'w') as writer:
    
    for keys,values in json_data.items():
        writer.write_all(values)