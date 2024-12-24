from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Course, Lesson, SubscriptionOnCourse, CoursePayment
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):

    url = serializers.URLField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = SerializerMethodField()

    def get_lessons_count(self, course):
        return course.lessons.count()

    def get_subscription(self, course):
        current_user = self.context.get('request', None).user
        return course.course_subscription.filter(user=current_user).exists()

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionOnCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriptionOnCourse
        fields = ['user', 'course']


class CoursePaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoursePayment
        fields = '__all__'
