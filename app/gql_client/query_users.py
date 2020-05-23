from graphql_client import gql, client

def print_users():
    query_users = gql('''
        query {
            Users {
                Id
                FirstName
                LastName
                EmailId
            }
        }
    ''')
    users = client.execute(query_users)
    for user in users["Users"]:
        print (user)

if __name__ == "__main__":
    print_users()