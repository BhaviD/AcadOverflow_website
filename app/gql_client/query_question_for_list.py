from graphql_client import gql, client

def query_question_for_list(Id):
    query_question = gql('''
        query {
            Questions_by_pk(Id: ''' + str(Id) + ''') {
                Id
                Title
                Body
                VoteCount
            }
        }
    ''')
    question = client.execute(query_question)
    question = question['Questions_by_pk']  # "by_pk" means to query an entry by the private key
    return question
    # print ("Title:", question['Title'])
    # print ("Body:", question['Body'])
    # print ("VoteCount:", question['VoteCount'])

# if __name__ == "__main__":
    # for id in id_list:
    #     query_question_for_list(id)