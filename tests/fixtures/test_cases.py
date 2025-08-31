import pytest
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.orm import selectinload
from src.models import User
from tests.unit.conftest import RegisterTestSchema, UserResponse, UserResponseWithQuestions, QuestionResponseTest, \
    QuestionWithAnswersResponseTest, AnswerResponseTest
from src.core.jwt import create_access_token
from src.schemas import RegistrationPayload, AuthResponse, AnswerBase, QuestionBase
from uuid import UUID
from contextlib import nullcontext


PARAMS_TEST_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE = [
    (
        {'username': '11'},
        UserResponse(
            id=UUID('3d3e784f-646a-4ad4-979c-dca5dcea2a28'),
            username='11',
            hashed_password='$2b$12$6jdyx4G4dwZs9wOTJ/4tauQE7vtQdaTVa9CWI6.iqWm4f50AwSBmW'
        ),
        nullcontext()
    ),
    (
        {'username': '12'},
        None,
        nullcontext()
    ),
    (
        {'hashed_password': '$2b$12$6jdyx4G4dwZs9wOTJ/4tauQE7vtQdaTVa9CWI6.iqWm4f50AwSBmW'},
        None,
        pytest.raises(MultipleResultsFound)
    )
]



PARAMS_TEST_REPOSITORY_GET_FILTER_BY_WITH_OPTIONS_OR_NONE = [
    (
        [selectinload(User.questions)],
        {'username': '22'},
        UserResponseWithQuestions(
            id=UUID('bb929d29-a8ef-4a8e-b998-9998984d8fd6'),
            username='22',
            hashed_password='$2b$12$6jdyx4G4dwZs9wOTJ/4tauQE7vtQdaTVa9CWI6.iqWm4f50AwSBmW',
            questions=[
                QuestionResponseTest(
                    id=UUID('b1f0b8f2-3c7b-4f2f-a4d7-9a08dbde0c80'),
                    user_id=UUID('bb929d29-a8ef-4a8e-b998-9998984d8fd6'),
                    text='textt'
                )
            ]
        ),
        nullcontext()
    ),
    (
        [],
        {'username': '12'},
        None,
        nullcontext()
    ),
    (
        [],
        {'hashed_password': '$2b$12$6jdyx4G4dwZs9wOTJ/4tauQE7vtQdaTVa9CWI6.iqWm4f50AwSBmW'},
        None,
        pytest.raises(MultipleResultsFound)
    )
]


PARAMS_USER_ROUTE_REGISTRATION = [
    (
        RegistrationPayload(
            username='12',
            password='password'
        ),
        RegisterTestSchema(
            username='12',
        ),
        201,
        None,
    ),
    (
        RegistrationPayload(
            username='11',
            password='password'
        ),
        None,
        409,
        'Username already registered'
    ),
]

PARAMS_USER_ROUTE_AUTH = [
    (
        OAuth2PasswordRequestForm(
            username='11',
            password='password',
            grant_type='password'
        ),
        AuthResponse,
        200,
        None
    ),
    (
        OAuth2PasswordRequestForm(
            username='12',
            password='password',
            grant_type='password'
        ),
        None,
        404,
        'No such user'
    ),
    (
        OAuth2PasswordRequestForm(
            username='11',
            password='password1',
            grant_type='password'
        ),
        None,
        401,
        'Incorrect password'
    )
]

token_data = {'user_id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28'}
access_token = create_access_token(token_data)


PARAMS_QUESTION_ROUTE_CREATE_QUESTION = [
    (
        {"Authorization": f'Bearer {access_token}'},
        QuestionBase(
            text=token_data['user_id'],
        ),
        QuestionResponseTest(
            id=UUID('d61a9530-123f-4620-a6a9-5c3e67220c4a'),
            text='texxt',
            user_id='3d3e784f-646a-4ad4-979c-dca5dcea2a28'
        ),
        201

    ),
]

PARAMS_QUESTION_ROUTE_GET_QUESTION_BY_ID = [
    (
        UUID('d61a9530-123f-4620-a6a9-5c3e67220c4a'),
        QuestionWithAnswersResponseTest(
            id=UUID('d61a9530-123f-4620-a6a9-5c3e67220c4a'),
            text='textt',
            user_id=UUID('4289fdd9-9fd3-4f39-a10b-a703a4fd23f0'),
            answers=[]
        ),
        200
    ),

    (
        UUID('b1f0b8f2-3c7b-4f2f-a4d7-9a08dbde0c80'),
        QuestionWithAnswersResponseTest(
            id=UUID('b1f0b8f2-3c7b-4f2f-a4d7-9a08dbde0c80'),
            text='textt',
            user_id=UUID('bb929d29-a8ef-4a8e-b998-9998984d8fd6'),
            answers=[
                AnswerResponseTest(
                    id=UUID('a7951f41-f3d6-49a3-a726-c46a9875b590'),
                    text='text',
                    user_id=UUID('bb929d29-a8ef-4a8e-b998-9998984d8fd6'),
                    question_id=UUID('b1f0b8f2-3c7b-4f2f-a4d7-9a08dbde0c80')
                )
            ]
        ),
        200
    ),
    (
        UUID('d61a9530-123f-4620-a6a9-5c3e67220c41'),
        None,
        404
    )
]

token_data2 = {'user_id': '4289fdd9-9fd3-4f39-a10b-a703a4fd23f0'}
access_token2 = create_access_token(token_data2)

PARAMS_QUESTION_ROUTE_DELETE_QUESTION_BY_ID = [
    (
        {"Authorization": f'Bearer {access_token2}'},
        UUID('d61a9530-123f-4620-a6a9-5c3e67220c4a'),
        True,
        200
    ),

    (
        {"Authorization": f'Bearer {access_token2}'},
        UUID('d61a9530-123f-4620-a6a9-5c3e67220c4b'),
        True,
        404
    ),
    (
        {"Authorization": f'Bearer {access_token2}'},
        UUID('b1f0b8f2-3c7b-4f2f-a4d7-9a08dbde0c80'),
        None,
        403
    )
]
PARAMS_ANSWER_ROUTE_CREATE_ANSWER = [
    (
        {"Authorization": f'Bearer {access_token}'},
        UUID('d61a9530-123f-4620-a6a9-5c3e67220c4a'),
        True,
        AnswerBase(
            text=token_data['user_id']
        ),
        201
    ),
    (
        {"Authorization": f'Bearer {access_token}'},
        UUID('d61a9530-123f-4620-a6a9-5c3e67220c4b'),
        False,
        AnswerBase(
            text=token_data['user_id']
        ),
        404
    )
]

PARAMS_ANSWER_ROUTE_GET_ANSWER_BY_ID = [
    (
        UUID('b1648a37-90d7-42d4-b81b-4c18580dfc3f'),
        AnswerResponseTest(
            id=UUID('b1648a37-90d7-42d4-b81b-4c18580dfc3f'),
            text='text',
            user_id=UUID('4289fdd9-9fd3-4f39-a10b-a703a4fd23f0'),
            question_id=UUID('0a59c625-e148-4e35-b8c9-a27110ca2869')
        ),
        200
    ),
    (
        UUID('b1648a37-90d7-42d4-b81b-4c18580dfc3d'),
        None,
        404
    )
]

PARAMS_ANSWER_ROUTE_DELETE_ANSWER_BY_ID = [
    (
        {"Authorization": f'Bearer {access_token2}'},
        UUID('b1648a37-90d7-42d4-b81b-4c18580dfc3f'),
        True,
        200
    ),
    (
        {"Authorization": f'Bearer {access_token2}'},
        UUID('a7951f41-f3d6-49a3-a726-c46a9875b590'),
        False,
        403
    ),
    (
        {"Authorization": f'Bearer {access_token2}'},
        UUID('a7951f41-f3d6-49a3-a726-c46a9875b591'),
        False,
        404
    ),

]