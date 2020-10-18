from django.urls import reverse

from tests.testapp import workflows


class TestTaskViewMixin:

    def test_create_task(self, db, admin_client, admin_user):
        url = reverse('simpleworkflow:start_view')
        response = admin_client.post(url)
        assert response.status_code == 302

        wf = workflows.SimpleWorkflow.objects.get()

        assert wf.task_set.count() == 2
        new_task = wf.task_set.get(name='save_the_princess')
        assert new_task.name == 'save_the_princess'
        assert new_task.type == 'human'
        assert not new_task.assignees.all()

    def test_custom_create_task(self, db, admin_client, admin_user):
        url = reverse('assigneeworkflow:start_view')
        response = admin_client.post(url)
        assert response.status_code == 302

        wf = workflows.AssigneeWorkflow.objects.get()

        assert wf.task_set.count() == 2
        new_task = wf.task_set.get(name='save_the_princess')
        assert admin_user in new_task.assignees.all()
