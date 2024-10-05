import argparse
from .repo import GitHubRepoExtractor

# Define available project choices
PROJECT_CHOICES = [
    'deno', 'lambda', 'llm-stream', 'azure', 'speedybot-starter',
    'standard-server', 'worker', 'voiceflow', 'voiceflow-kb'
]

def setup(project: str, boot: bool, install: bool, token: str, debug: bool):
    print(f"Setting up project: {project}")
    if boot:
        print("Booting up the project...")
    if install:
        print("Installing dependencies...")
    print(f"Using token: {token}")

    # Instantiate the extractor with the debug flag
    extractor = GitHubRepoExtractor(
        repo_url='https://github.com/valgaze/speedybot',
        branch='v2',
        debug=debug
    )
    
    # Extract the project based on its subdirectory
    extractor.extract_to_directory(
        subdir_name=f'examples/{project}',
        target_dir=project
    )

def main():
    parser = argparse.ArgumentParser(description="SpeedyBot CLI")
    
    subparsers = parser.add_subparsers(dest="command")

    # Create the setup command
    setup_parser = subparsers.add_parser('setup', help='Setup a new project')
    setup_parser.add_argument('--project', required=True, choices=PROJECT_CHOICES, help='Name of the project')
    setup_parser.add_argument('--boot', action='store_true', help='Boot up the project')
    setup_parser.add_argument('--install', action='store_true', help='Install dependencies')
    setup_parser.add_argument('--token', required=True, help='API token')
    setup_parser.add_argument('--debug', action='store_true', help='Enable debug logging')

    args = parser.parse_args()

    if args.command == 'setup':
        setup(args.project, args.boot, args.install, args.token, args.debug)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
