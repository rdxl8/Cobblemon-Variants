import os
import json
import re
import random
import string
import shutil

def sanitize_name(name):
    """Sanitize the name to be used in filenames."""
    return re.sub(r'[^a-zA-Z0-9_]', '', name.lower())

def create_directory(path):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def generate_random_id(length=8):
    """Generate a random ID for the resolver filename."""
    return ''.join(random.choices(string.digits, k=length))

def generate_files():
    aspect_name = input("Enter the aspect name: ")
    sanitized_aspect = sanitize_name(aspect_name)

    pokemon_input = input("Enter pokemon IDs and names (format: id1_name1, id2_name2, ...): ")
    pokemon_entries = [entry.strip() for entry in pokemon_input.split(',')]

    pokemon_data = []
    for entry in pokemon_entries:
        if '_' not in entry:
            print(f"Warning: Skipping invalid entry '{entry}'. Format should be 'id_name'.")
            continue

        parts = entry.split('_', 1)
        pokemon_id = parts[0].strip()
        pokemon_name = parts[1].strip()

        pokemon_data.append({
            'name': pokemon_name,
            'id': pokemon_id,
            'sanitized_name': sanitize_name(pokemon_name)
        })

    species_features_dir = "output/data/cobblemon/species_features"
    assignments_dir = "output/data/cobblemon/species_feature_assignments"
    resolvers_base_dir = "output/assets/cobblemon/bedrock/pokemon/resolvers"
    textures_base_dir = "output/assets/cobblemon/textures/pokemon"

    create_directory(species_features_dir)
    create_directory(assignments_dir)
    create_directory(resolvers_base_dir)
    create_directory(textures_base_dir)

    feature_file = {
        "keys": [
            aspect_name
        ],
        "type": "flag",
        "isAspect": True,
        "default": False
    }

    feature_file_path = f'{species_features_dir}/{sanitized_aspect}.json'
    with open(feature_file_path, 'w') as f:
        json.dump(feature_file, f, indent=2)

    assignment_file = {
        "pokemon": [pokemon['name'] for pokemon in pokemon_data],
        "features": [aspect_name]
    }

    assignment_file_path = f'{assignments_dir}/{sanitized_aspect}_assignment.json'
    with open(assignment_file_path, 'w') as f:
        json.dump(assignment_file, f, indent=2)

    textures_source_dir = f"textures/{aspect_name}"
    if not os.path.exists(textures_source_dir):
        print(f"Warning: Textures directory '{textures_source_dir}' not found.")

    for pokemon in pokemon_data:
        resolver_dir = f"{resolvers_base_dir}/{pokemon['id']}_{pokemon['sanitized_name']}"
        create_directory(resolver_dir)

        random_id = generate_random_id()

        resolver_file = {
            "species": f"cobblemon:{pokemon['name']}",
            "order": random_id,
            "variations": [
                {
                    "aspects": [aspect_name],
                    "texture": f"cobblemon:textures/pokemon/{pokemon['id']}_{pokemon['sanitized_name']}/{pokemon['sanitized_name']}_{sanitized_aspect}.png"
                }
            ]
        }

        resolver_file_path = f"{resolver_dir}/{random_id}_{pokemon['sanitized_name']}_{sanitized_aspect}.json"
        with open(resolver_file_path, 'w') as f:
            json.dump(resolver_file, f, indent=2)

        source_texture_path = f"{textures_source_dir}/{pokemon['name']}.png"
        if os.path.exists(source_texture_path):
            pokemon_texture_dir = f"{textures_base_dir}/{pokemon['id']}_{pokemon['sanitized_name']}"
            create_directory(pokemon_texture_dir)

            target_texture_path = f"{pokemon_texture_dir}/{pokemon['sanitized_name']}_{sanitized_aspect}.png"
            shutil.copy2(source_texture_path, target_texture_path)
            print(f"Copied texture: {source_texture_path} -> {target_texture_path}")
        else:
            print(f"Warning: Texture file not found for {pokemon['name']}: {source_texture_path}")

    print(f"\nFiles generated successfully in the following directories:")
    print(f"- Species features: {species_features_dir}/{sanitized_aspect}.json")
    print(f"- Feature assignments: {assignments_dir}/{sanitized_aspect}_assignment.json")
    print("- Resolvers:")
    for pokemon in pokemon_data:
        resolver_dir = f"{resolvers_base_dir}/{pokemon['id']}_{pokemon['sanitized_name']}"
        print(f"  - {resolver_dir}/<RANDOM>_{pokemon['sanitized_name']}_{sanitized_aspect}.json")
    print("- Textures copied to respective pokemon directories")

if __name__ == "__main__":
    generate_files()
