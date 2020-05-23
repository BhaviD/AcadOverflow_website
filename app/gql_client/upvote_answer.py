from graphql_client import gql, client

def upvote_answer(aId):
    upvote = gql('''
        mutation {
            update_Answers(
                where: {
                    Id: { _eq: ''' + str(aId) + ''' }
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
    aId = 2
    upvote_answer(aId)