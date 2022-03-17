
"""
This file contains the Converter methods
"""
from werkzeug.routing import BaseConverter
from project.models.models import User, Menu
from project.utils import create_error_message


class UserConverter(BaseConverter):
    """
    Converter for user entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to a user object
        """
        role = User.query.filter_by(id=value).first()
        if role is None:
            return create_error_message(
                404, "Not found",
                "User not found"
            )
        return role

    def to_url(self, value):
        """
        return user id
        """
        return str(value.id)

class MenuConverter(BaseConverter):
    """
    Converter for Menu entity in URL parameter
    """

    def to_python(self, value):
        """
        convert to a menu object
        """
        menu = Menu.query.filter_by(id=value).first()
        if menu is None:
            return create_error_message(
                404, "Not found",
                "Menu not found"
            )
        return menu

    def to_url(self, value):
        """
        return menu id
        """
        return str(value.id)


# class DepartmentConverter(BaseConverter):
#     """
#     Converter for Department entity in URL parameter
#     """
#
#     def to_python(self, value):
#         """
#         convert to a department object
#         """
#         department = Department.query.filter_by(department_id=value).first()
#         if department is None:
#             return create_error_message(
#                 404, "Not found",
#                 "Department not found"
#             )
#         return department
#
#     def to_url(self, value):
#         """
#         return department id
#         """
#         return str(value.department_id)
#
#
# class OrganizationConverter(BaseConverter):
#     """
#     Converter for Organization entity in URL parameter
#     """
#
#     def to_python(self, value):
#         """
#         convert to a organization object
#         """
#         organization = Organization.query.filter_by(
#             organization_id=value).first()
#         if organization is None:
#             return create_error_message(
#                 404, "Not found",
#                 "Organization not found"
#             )
#         return organization
#
#     def to_url(self, value):
#         """
#         return organization id
#         """
#         return str(value.organization_id)
#
#
# class LeavePlanConverter(BaseConverter):
#     """
#     Converter for leave plan entity in URL parameter
#     """
#
#     def to_python(self, value):
#         """
#         convert to a leave plan object
#         """
#         leaveplan = LeavePlan.query.filter_by(id=value).first()
#
#         if leaveplan is None:
#             return create_error_message(
#                 404, "Not found",
#                 "leave plan not found"
#             )
#         return leaveplan
#
#     def to_url(self, value):
#         """
#         return leave plan id
#         """
#         return str(value.id)
#
#
# class EmployeeConverter(BaseConverter):
#     """
#     Converter for employee entity in URL parameter
#     """
#
#     def to_python(self, value):
#         """
#         convert to a employee object
#         """
#         employee = Employee.query.filter_by(employee_id=value).first()
#         if employee is None:
#             return create_error_message(
#                 404, "Not found",
#                 "employee not found"
#             )
#         return employee
#
#     def to_url(self, value):
#         """
#         return employee id
#         """
#         return str(value.employee_id)
