from graphql_client import gql, client

def upvote_question(qId):
    upvote = gql('''
        mutation {
            update_Questions(
                where: {
                    Id: { _eq: ''' + str(qId) + ''' }
                }, 
                _inc: { VoteCount: 1 }
            ) {
                returning { VoteCount }
            }
        }
    ''')

    try:
        mutation_result = client.execute(upvote)
        print (mutation_result)
    except Exception as e:
        print (e)

if __name__ == "__main__":
    qId = 2
    upvote_question(qId)