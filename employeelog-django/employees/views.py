from rest_framework import viewsets

from .models import Employee, DeletedEmployee

from .serializers import (
    EmployeeSerializer,
    DeletedEmployeeSerializer
)


class EmployeeView(viewsets.ModelViewSet):

    queryset = Employee.objects.all()

    serializer_class = EmployeeSerializer

    def perform_destroy(self, instance):

        DeletedEmployee.objects.create(
            name=instance.name,
            email=instance.email,
            designation=instance.designation,
            salary=instance.salary,
            phone=instance.phone
        )

        instance.delete()


class DeletedEmployeeView(viewsets.ModelViewSet):

    queryset = DeletedEmployee.objects.all()

    serializer_class = DeletedEmployeeSerializer