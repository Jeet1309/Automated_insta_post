import json

def parse_script_to_json(script_path, output_path):
    with open(script_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    script_json = []
    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        if ':' in line:
            speaker, text = line.split(':', 1)
            script_json.append({
                "speaker": speaker.strip(),
                "text": text.strip()
            })

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(script_json, f, ensure_ascii=False, indent=4)

    print(f"✅ Script saved to {output_path}")


# Example usage
parse_script_to_json("script.txt", "script.json")

