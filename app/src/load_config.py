import yaml

def get_variable(filepath, variable_name):
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
        if variable_name not in data:
            raise KeyError(f"Variable '{variable_name}' not found in '{filepath}'")
    return data.get(variable_name)

def main():
    api_key = get_variable('app/config/.credentials.yaml', 'API_KEY')
    zone_id = get_variable('app/config/.credentials.yaml', 'ZONE_ID')

    print(api_key)
    print(zone_id)

if __name__ == "__main__":
    main()