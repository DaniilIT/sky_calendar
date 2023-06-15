# from django.test import TestCase

# test_goals


# from django.urls import reverse
# from django.utils import timezone
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from src.core.models import User
# from src.goals.models import Goal, GoalCategory
#
# class TestCreateGoal(APITestCase):
#     def test_auth_required(self):
#         response = self.client.post(reverse('create-goal'))
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_not_category_owner(self):
#         user = User.objects.create(username='username', password='password')
#         category = GoalCategory.objects.create(title='cat', user=user)
#
#         self.client.force_login(user=User.objects.create(username='test_user', password='password'))
#         response = self.client.post(
#             path=reverse('create-goal'),
#             data={
#                 'title': 'new goal',
#                 'category': category.id,
#                 'due_date': timezone.now(),
#             }
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_success(self):
#         user = User.objects.create(username='username', password='password')
#         category = GoalCategory.objects.create(title='cat', user=user)
#
#         self.client.force_login(user=user)
#         now = timezone.now()
#         response = self.client.post(
#             path=reverse('create-goal'),
#             data={
#                 'title': 'new goal',
#                 'category': category.id,
#                 'due_date': now,
#             }
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         new_goal = Goal.objects.last()
#         self.assertDictEqual(
#             response.json(),
#             {
#                 'id': new_goal.id,
#                 'category': new_goal.category,
#                 'created': timezone.localtime(new_goal.created).isoformat(),
#                 'updated': timezone.localtime(new_goal.created).isoformat(),
#                 'title': 'new goal',
#                 'description': None,
#                 'status': Goal.status.to_do.value,
#                 'priority': Goal.Priority.medium.value,
#                 'due_date': timezone.localtime(now).isoformat(),
#             }
#         )
#
#     class TestGoalsList(APITestCase):
#
#         def setUp(self) -> None:
#             self.user = User.objects.create(username='username', password='password')
