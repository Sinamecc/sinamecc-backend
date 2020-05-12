from rest_framework import serializers
from workflow.models import Comment, ReviewStatus

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'comment')

class ReviewStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewStatus
        fields = ('id', 'status')
