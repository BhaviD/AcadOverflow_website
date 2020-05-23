from graphql_client import gql, client
import pprint

def questions_by_user(UserId):

    #select Title, Id from Questions where UserId = str(id)
    query_question = gql('''
    #     query {
    #         Questions(_like: ''' + str(UserId) + ''') {
    #             Id
    #             Title
    #         }
    #     }

    query {
        Questions(where: {UserId: { _eq: ''' + str(UserId) + '''}}) {
            Id
            Title
        }
    }


    ''')

    questions = client.execute(query_question)
    questions = questions['Questions']
    # pprint.pprint(questions)
    return questions

if __name__ == "__main__":
    result = questions_by_user(41)