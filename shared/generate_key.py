# Security Keys
import secrets
import os

def generate_env_file():
    # Master Path
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(root_dir, '.env.keys')

    # Key Generate
    api_key = secrets.token_urlsafe(32)
    
    # .env content | You can write triple quotes (""" """) and specify other keys there.
    env_content = f"SERVICE_API_KEY={api_key}\n"
    
    # Write to .env
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    #print(f"Generated API key: {api_key}")
    #return api_key

if __name__ == "__main__":
    generate_env_file()
