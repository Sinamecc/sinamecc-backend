from workflow.models import Comment, ReviewStatus
from workflow.serializers import CommentSerializer, ReviewStatusSerializer
from rest_framework.parsers import JSONParser
from general.helpers.services import ServiceHelper

class WorkflowService():
    def __init__(self):
        self.COMMENT_DOES_NOT_EXIST = "Comment does not exist."
        self.REVIEW_STATUS_DOES_NOT_EXIST = "Review status does not exist."
        self.SUBMITTED_STATUS = 'submitted'
        self.IN_REVIEW_STATUS = 'in-review'
        self.ON_CHANGE_STATUS = 'on-change'
        self.APPROVED_STATUS = 'approved'
        self.REJECTED_STATUS = 'rejected'
        self._service_helper = ServiceHelper()

    def get_review_status_id(self, review_status):
        try:
            rs_id = ReviewStatus.objects.filter(status=review_status)[0].id
            result = (True, rs_id)
        except:
            result = (False, self.REVIEW_STATUS_DOES_NOT_EXIST)
        return result

    def _get_serialized_comment(self, data , comment=False, many=False):

        serializer = self._service_helper.get_serialized_record(CommentSerializer, data, many=many, record=comment, partial=True)

        return serializer

    def get_serialized_comment(self, request):
        comment_data = {
            'comment': request.data.get('comment')
        }
        serializer = CommentSerializer(data=comment_data)
        return serializer
    
    def create_comment(self, request):
        serialized_comment = self.get_serialized_comment(request)
        if serialized_comment.is_valid():
            new_comment = serialized_comment.save()
            return (True, new_comment)
        return (False, serialized_comment.errors)


    def create_comment_list(self, comment_list):

        serialized_comment_list = self._get_serialized_comment(comment_list, many=True)
        if serialized_comment_list.is_valid():
            comments = serialized_comment_list.save()
            result = (True, comments)
        else:
            result = (False, serialized_comment_list.errors)

        return result


    def get_status_data(self):
        try:
            review_status_list = [
                {
                    'id': r.id,
                    'status': r.status
                } for r in ReviewStatus.objects.all()
            ]
            result = (True, review_status_list)
        except ReviewStatus.DoesNotExist:
            result = (False, {'error': self.REVIEW_STATUS_DOES_NOT_EXIST})
        return result
