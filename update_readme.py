import os
from collections import defaultdict


def generate_til_readme():
    til_dict = defaultdict(list)

    # Iterate through all the .md files in the folders
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".md"):
                category = os.path.basename(root)
                file_path = os.path.join(root, file)

                with open(file_path, "r") as f:
                    content = f.read()
                    title = content.split("\n")[0].replace("#", "").strip()

                relative_path = os.path.relpath(file_path, ".")
                til_dict[category].append((title, relative_path))

    # Generate README content
    readme_content = "# Today I Learned\n\n"

    for category, items in sorted(til_dict.items()):
        if category != ".":  # Exclude root directory
            readme_content += f"## {category}\n\n"
            for title, path in sorted(items):
                readme_content += f"- [{title}]({path})\n"
            readme_content += "\n"

    # Write README.md file
    with open("README.md", "w") as readme_file:
        readme_file.write(readme_content)

    print("README.md has been generated successfully.")


if __name__ == "__main__":
    generate_til_readme()
