import graphene
from graphene_django import DjangoObjectType
from .models import *
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id


class CityNode(DjangoObjectType):
    class Meta:
        model = City
        filter_fields = ['name']
        interfaces = (graphene.relay.Node,)


class TitleNode(DjangoObjectType):
    class Meta:
        model = Title
        filter_fields = ['name']
        interfaces = (graphene.relay.Node,)


class EmployeeNode(DjangoObjectType):
    class Meta:
        model = Employee
        filter_fields = [
              'name',
              'city__name',
              'title__name'
               ]
        interfaces = (graphene.relay.Node,)


class Query(object):
    city = graphene.relay.Node.Field(CityNode)
    all_cities = DjangoFilterConnectionField(CityNode)

    title = graphene.relay.Node.Field(TitleNode)
    all_titles = DjangoFilterConnectionField(TitleNode)

    employee = graphene.relay.Node.Field(EmployeeNode)
    all_employees = DjangoFilterConnectionField(EmployeeNode)


class CreateTitle(graphene.relay.ClientIDMutation):
    title = graphene.Field(TitleNode)

    class Input:
        title_name = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        title = Title(name=input.get('name'))
        title.save()

        return CreateTitle(title=title)


class CreateEmployee(graphene.relay.ClientIDMutation):
    book = graphene.Field(EmployeeNode)

    class Input:
        name = graphene.String()
        city = graphene.String()
        title = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        employee = Employee(name=input.get('name'),
                            city=City.objects.get(name=input.get('city')),
                            title=Title.objects.get(name=input.get('title')))
        employee.save()
        return CreateEmployee(employee=employee)


class UpdateEmployee(graphene.relay.ClientIDMutation):
    employee = graphene.Field(EmployeeNode)

    class Input:
        id = graphene.String()
        name = graphene.String()
        city = graphene.String()
        title = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        employee = Employee.objects.get(pk=from_global_id(input.get('id'))[1])
        employee.employee_name = input.get('name')
        employee.employee_city = City.objects.get(name=input.get('city'))
        employee.employee_title = Title.objects.get(name=input.get('title'))
        employee.save()
        return UpdateEmployee(employee=employee)


class DeleteEmployee(graphene.relay.ClientIDMutation):
    employee = graphene.Field(EmployeeNode)

    class Input:
        id = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        employee = Employee.objects.get(pk=from_global_id(input.get('id'))[1])
        employee.delete()
        return DeleteEmployee(employee=employee)


class Mutation(graphene.AbstractType):
    create_title = CreateTitle.Field()
    create_employee = CreateEmployee.Field()
    update_employee = UpdateEmployee.Field()
    delete_employee = DeleteEmployee.Field()
