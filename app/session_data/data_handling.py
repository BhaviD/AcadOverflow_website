import pandas as pd
import datetime

questions_df = pd.read_csv("./app/session_data/csv_files/Preprocessed_questions.csv")
answers_df = pd.read_csv("./app/session_data/csv_files/Preprocessed_answers.csv")
users_df = pd.read_csv("./app/session_data/csv_files/Preprocessed_users.csv")

def get_preprocessed_data():
    global questions_df
    return questions_df

def csv_register_user(emailId, firstName, lastName, password):
    global users_df
    id = users_df.shape[0]
    curr_timestamp = str(datetime.datetime.now())
    new_user = {
        'EmailId': emailId,
        'FirstName': firstName,
        'LastName': lastName,
        'Password': password,
        'Id': id,
        'created_at': curr_timestamp
    }
    users_df = users_df.append(new_user, ignore_index=True)

def csv_user_exists(emailId):
    global users_df
    user = users_df.loc[users_df['EmailId'] == emailId]
    return True if user.shape[0] else False

def csv_get_login_details(emailId):
    global users_df
    user_index = (users_df.loc[users_df['EmailId'] == emailId]).index
    if len(user_index) == 0:
        return None
    user = users_df.iloc[user_index[0]]
    login_details = {
        'EmailId': user.EmailId,
        'FirstName': user.FirstName,
        'LastName': user.LastName,
        'Password': user.Password,
        'Id': user.Id
    }
    return login_details

def csv_query_question_for_list(Id):
    global questions_df
    Id = int(Id)
    question = questions_df.iloc[Id]
    question_details = {
        'Id': Id,
        'Title': question.original_title,
        'Body': question.question_content,
        'VoteCount': question.VoteCount
    }
    return question_details

def csv_post_question(qtitle, qbody, tags_list, userId):
    global questions_df
    curr_timestamp = str(datetime.datetime.now())
    new_question = {
        'original_title': qtitle,
        'post_corpus': "-",
        'question_content': qbody,
        'question_url': "-",
        'tags': "",
        'overall_scores': 0.0,
        'answers_content': "-",
        'sentiment_polarity': 0.0,
        'sentiment_subjectivity': 0.0,
        'processed_title': "-",
        'UserId': userId,
        'created_at': curr_timestamp
    }
    questions_df = questions_df.append(new_question, ignore_index=True)


def csv_query_user_questions(userId):
    global questions_df
    userId = int(userId)
    question_ids = questions_df.loc[questions_df['UserId'] == userId].index
    if len(question_ids) == 0:
        return None
    User_Questions = []
    for q_id in question_ids:
        question = questions_df.iloc[q_id]
        question_details = {
            'Id': q_id,
            'Title': question.original_title,
        }
        User_Questions.append(question_details)
    return User_Questions


def csv_query_question_for_page(Id):
    global questions_df
    global answers_df
    global users_df
    Id = int(Id)
    question = questions_df.iloc[Id]
    # print ("1", type(question))
    # print ("2", question)
    question_details = {
        'Id': Id,
        'Title': question.original_title,
        'Body': question.question_content,
        'VoteCount': question.VoteCount,
        'created_at': question.created_at
    }
    # print ("3", question_details)

    Question_Answers = []
    answer_ids = answers_df.loc[answers_df['QuestionId'] == Id].index
    # print ("4", answer_ids)
    for a_id in answer_ids:
        answer = answers_df.iloc[a_id]
        # print ("5", answer)
        answer_dict = {
            'Body': answer.answers_content,
            'VoteCount': answer.VoteCount,
            'created_at': answer.created_at
        }
        # print ("6", answer_dict)
        ans_userId = answer.UserId
        ans_user = users_df.iloc[ans_userId]
        # print ("7", ans_user)
        answer_dict['Answer_User'] = {
            'Id': ans_user.Id,
            'EmailId': ans_user.EmailId,
            'FirstName': ans_user.FirstName,
            'LastName': ans_user.LastName
        }
        # print ("8", answer_dict)
        Question_Answers.append(answer_dict)
    question_details['Question_Answers'] = Question_Answers

    ques_user = users_df.iloc[question.UserId]
    # print ("9", ques_user)
    question_details['Question_User'] = {
        'Id': ques_user.Id,
        'EmailId': ques_user.EmailId,
        'FirstName': ques_user.FirstName,
        'LastName': ques_user.LastName
    }
    return question_details

        
def csv_post_answer(qId, aBody, userId):
    global answers_df
    qId = int(qId)
    userId = int(userId)
    curr_timestamp = str(datetime.datetime.now())
    new_answer = {
        'answers_content': aBody,
        'UserId': userId,
        'QuestionId': qId,
        'VoteCount': 0,
        'created_at': curr_timestamp
    }
    answers_df = answers_df.append(new_answer, ignore_index=True)
    print (new_answer)


def csv_downvote_answer(aId):
    aId = int(aId)
    answers_df.at[aId, 'VoteCount'] -= 1

def csv_downvote_question(qId):
    qId = int(qId)
    questions_df.at[qId, 'VoteCount'] -= 1

def csv_upvote_answer(aId):
    aId = int(aId)
    answers_df.at[aId, 'VoteCount'] += 1

def csv_upvote_question(qId):
    qId = int(qId)
    questions_df.at[qId, 'VoteCount'] += 1
