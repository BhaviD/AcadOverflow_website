from graphql_client import gql, client
import sys

def get_login_details(emailId):
    query_user = gql('''
        query {
            Users (where: {EmailId: { _like: "''' + emailId + '''"}}) {
                EmailId,
                FirstName,
                LastName,
                Password,
                Id
            }
        }
    ''')
    user = client.execute(query_user)
    if len(user["Users"]) == 0:
        return None
    return user["Users"][0]

if __name__ == "__main__":
    emailId = "bhavi.dhingra@students.iiit.ac.in"
    user = get_login_details(emailId)
    print (user)