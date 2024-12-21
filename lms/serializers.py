from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Course, Lesson, SubscriptionOnCourse
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):

    video_url = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionOnCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionOnCourse
        fields = ['user', 'course']
