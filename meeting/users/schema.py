from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

"""
This creates a user.
It takes three arguments username, password,email,first_name, last_name
"""
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    def mutate(self, info, username, password, email, first_name, last_name):
        user = get_user_model()(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()
        return CreateUser(user=user)

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    self_user = graphene.Field(UserType)

# It takes one argument id and returns user object
    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

# It returns logged in user object
    def resolve_self_user(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("User must login first")

        return user

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()