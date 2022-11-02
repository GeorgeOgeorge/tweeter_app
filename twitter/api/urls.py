from django.urls import path
from rest_framework.routers import DefaultRouter

from twitter.api.views import (
    TweetViewSet, TwitterUserViewSet,
    get_tweet_comments, get_user_tweets, follow_user
)


router = DefaultRouter()
router.register(r'twitterusers', TwitterUserViewSet, basename='twitterusers')
router.register(r'tweets', TweetViewSet, basename='tweets')

urlpatterns = [
    path('tweets/<int:pk>/get_tweet_comments', get_tweet_comments),
    path('tweets/<int:pk>/get_user_tweets', get_user_tweets),
    path('twitterusers/<int:user_pk>/<int:follow_pk>/follow_user', follow_user)
]

urlpatterns += router.urls