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
    """Generate a random ID for the resolver filename or spawn pool ID."""
    return ''.join(random.choices(string.digits, k=length))


def get_input_with_default(prompt, default):
    """Get user input with a default value if the user just presses Enter."""
    user_input = input(f"{prompt} (default: {default}): ").strip()
    return user_input if user_input else default


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
    spawn_pool_dir = "output/data/cobblemon/spawn_pool_world"

    create_directory(species_features_dir)
    create_directory(assignments_dir)
    create_directory(resolvers_base_dir)
    create_directory(textures_base_dir)
    create_directory(spawn_pool_dir)

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
            print(f"\nCopied texture: {source_texture_path} -> {target_texture_path}")
        else:
            print(f"Warning: Texture file not found for {pokemon['name']}: {source_texture_path}")

        print(f"Enter spawn settings for {pokemon['name']} (press Enter for default values):")

        default_weight = "5"
        default_biome = "#cobblemon:is_sandy"
        default_bucket = "common"
        default_context = "grounded"
        default_level = "5-31"
        default_min_skylight = "8"
        default_max_skylight = "15"

        spawn_weight = get_input_with_default("Enter spawn weight", default_weight)

        biome_name = get_input_with_default("Enter biome name", default_biome)

        valid_buckets = ["common", "uncommon", "rare", "ultra-rare"]
        while True:
            bucket = get_input_with_default(f"Choose a bucket for {pokemon['name']} (common/uncommon/rare/ultra-rare)", default_bucket)
            if bucket in valid_buckets:
                break
            print(f"Invalid choice. Please choose from: {', '.join(valid_buckets)}")

        valid_contexts = ["grounded", "submerged", "surface", "fishing"]
        while True:
            context = get_input_with_default(f"Choose a context for {pokemon['name']} (grounded/submerged/surface/fishing)", default_context)
            if context in valid_contexts:
                break
            print(f"Invalid choice. Please choose from: {', '.join(valid_contexts)}")

        while True:
            level = get_input_with_default(f"Enter level range for {pokemon['name']} (format: XX-YY, e.g. 30-50)", default_level)
            if re.match(r'^\d+-\d+$', level):
                break
            print("Invalid format. Please use the format XX-YY (e.g. 30-50)")

        min_skylight = get_input_with_default(f"Enter minSkyLight for {pokemon['name']}", default_min_skylight)

        while True:
            max_skylight = get_input_with_default(f"Enter maxSkyLight for {pokemon['name']}", default_max_skylight)
            if int(max_skylight) >= int(min_skylight):
                break
            print(f"maxSkyLight must be greater than or equal to minSkyLight ({min_skylight})")

        spawn_id = generate_random_id(6)
        spawn_pool_file = {
            "id": f"{pokemon['name']}-{sanitized_aspect}-{spawn_id}",
            "pokemon": f"{pokemon['name']} {aspect_name}=true",
            "presets": [
                "natural"
            ],
            "type": "pokemon",
            "context": context,
            "bucket": bucket,
            "level": level,
            "weight": spawn_weight,
            "condition": {
                "minSkyLight": min_skylight,
                "maxSkyLight": max_skylight,
                "biomes": [
                    biome_name
                ]
            }
        }

        spawn_pool_file_path = f"{spawn_pool_dir}/{pokemon['id']}_{pokemon['sanitized_name']}.json"
        with open(spawn_pool_file_path, 'w') as f:
            json.dump(spawn_pool_file, f, indent=2)

    print(f"\nFiles generated successfully in the following directories:")
    print(f"- Species features: {species_features_dir}/{sanitized_aspect}.json")
    print(f"- Feature assignments: {assignments_dir}/{sanitized_aspect}_assignment.json")
    print("- Resolvers:")
    for pokemon in pokemon_data:
        resolver_dir = f"{resolvers_base_dir}/{pokemon['id']}_{pokemon['sanitized_name']}"
        print(f"  - {resolver_dir}/<RANDOM>_{pokemon['sanitized_name']}_{sanitized_aspect}.json")
    print("- Textures copied to respective pokemon directories")
    print("- Spawn pool files:")
    for pokemon in pokemon_data:
        spawn_pool_file_path = f"{spawn_pool_dir}/{pokemon['id']}_{pokemon['sanitized_name']}.json"
        print(f"  - {spawn_pool_file_path}")


if __name__ == "__main__":
    generate_files()
