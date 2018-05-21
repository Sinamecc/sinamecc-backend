from workflow.models import Comment, ReviewStatus
from workflow.serializers import CommentSerializer, ReviewStatusSerializer
from rest_framework.parsers import JSONParser

class WorkflowService():
    def __init__(self):
        self.COMMENT_DOES_NOT_EXIST = "Comment does not exist."
        self.REVIEW_STATUS_DOES_NOT_EXIST = "Review status does not exist."

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
