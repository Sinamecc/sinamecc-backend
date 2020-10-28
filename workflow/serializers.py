from rest_framework import serializers
from workflow.models import Comment, ReviewStatus

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'comment', 'form_section', 'status','fsm_state', 'review_number', 'user')

class ReviewStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewStatus
        fields = ('id', 'status')
