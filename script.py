import requests

# Function to get blocked users and save to a file
def get_blocked_users(token):
    headers = {
        'Authorization': token,
    }
    response = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers)
    
    if response.status_code == 200:
        blocked_users = [user for user in response.json() if user['type'] == 2]  # Type 2 is blocked
        
        # Save the blocked users (IDs only) to a notepad file
        with open('blocked_users.txt', 'w') as f:
            for user in blocked_users:
                user_id = user.get('id', 'Unknown ID')
                f.write(f"{user_id}\n")
        
        print(f"Blocked users' IDs saved to 'blocked_users.txt'.")
        return blocked_users
    else:
        print(f"Failed to retrieve blocked users: {response.status_code}")
        return []

# Function to block users on a new account using their IDs
def block_users_on_new_account(token, blocked_users):
    headers = {
        'Authorization': token,
    }
    for user in blocked_users:
        user_id = user['id']
        block_url = f'https://discord.com/api/v9/users/@me/relationships/{user_id}'
        response = requests.put(block_url, headers=headers, json={"type": 2})  # Type 2 is block
        if response.status_code == 204:
            print(f"Blocked user ID: {user_id}")
        else:
            print(f"Failed to block user ID: {user_id}, Status code: {response.status_code}")

# Main function
def main():
    print("Option 1: Save blocked users")
    print("Option 2: Block users on new account")
    option = input("Choose an option: ")

    if option == '1':
        token = input("Enter your Discord token: ")
        blocked_users = get_blocked_users(token)
    
    elif option == '2':
        with open('blocked_users.txt', 'r') as f:
            blocked_users = [{"id": line.strip()} for line in f]  # Load user IDs from the file

        new_token = input("Enter the new Discord token: ")
        block_users_on_new_account(new_token, blocked_users)

if __name__ == "__main__":
    main()
