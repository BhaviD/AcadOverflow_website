from graphql_client import gql, client
import sys

def user_exists(emailId):
    query_user = gql('''
        query {
            Users (where: {EmailId: { _like: "''' + emailId + '''"}}) {
                EmailId
            }
        }
    ''')
    user = client.execute(query_user)
    if len(user["Users"]) == 0:
        return False
    if emailId != user["Users"][0]["EmailId"]:
        return False
    return True

if __name__ == "__main__":
    emailId = "bhavi.dhingra@students.iiit.ac.in"
    if user_exists(emailId):
        print ("User already has an account!!")
    else:
        print ("New Registration!!")