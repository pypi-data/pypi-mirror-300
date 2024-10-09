import argparse
import requests
from rich.console import Console
from rich.table import Table


def fetch_github_repositories(query=None):
    search_query = "topic:beepy-app"
    if query:
        search_query += f" {query}"
    
    response = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": search_query},
        headers={"Accept": "application/vnd.github.v3+json"},
    )
    if response.status_code == 200:
        return response.json().get("items", [])
    else:
        print("Failed to fetch data from GitHub")
        return []


def display_repositories(repositories):
    if not repositories:
        print("No packages found matching your search criteria.")
        return

    console = Console()
    table = Table(title="Available Packages")

    table.add_column("Package Name", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    table.add_column("Stars", justify="right", style="green")

    for repo in repositories:
        package_name = f"{repo['owner']['login']}/{repo['name']}"
        description = repo["description"] or "No description"
        stars = str(repo["stargazers_count"])
        table.add_row(package_name, description, stars)

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="bapp-store Command Line Interface")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Help command
    help_parser = subparsers.add_parser("help", help="Show help message")
    search_parser = subparsers.add_parser("search", help="Search for a package")
    search_parser.add_argument(
        "package_name", type=str, help="Name of the package to search"
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all available packages")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install a package")
    install_parser.add_argument(
        "package_name", type=str, help="Name of the package to install"
    )

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove a package")
    remove_parser.add_argument(
        "package_name", type=str, help="Name of the package to remove"
    )

    # List-installed command
    list_installed_parser = subparsers.add_parser(
        "list-installed", help="List all installed packages"
    )

    args = parser.parse_args()

    if args.command == "search":
        print(f"Searching for package: {args.package_name}")
        repositories = fetch_github_repositories(args.package_name)
        display_repositories(repositories)
    elif args.command == "list":
        print("Listing all available packages from GitHub with topic 'beepy-app':")
        repositories = fetch_github_repositories()
        display_repositories(repositories)
    elif args.command == "install":
        print(f"Installing package: {args.package_name}")
    elif args.command == "remove":
        print(f"Removing package: {args.package_name}")
    elif args.command == "list-installed":
        print("Listing all installed packages")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
