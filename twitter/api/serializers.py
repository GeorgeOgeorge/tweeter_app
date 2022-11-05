from rest_framework import serializers

from twitter.models import Tweet, TwitterUser
from twitter.service import TweetService, TwitterUserService


class TwitterUserSerializer(serializers.ModelSerializer):

    tweets = serializers.SerializerMethodField()
    follows = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = TwitterUser
        fields = [
            'id',
            'username',
            'password',
            'bio',
            'tweets',
            'follows',
            'followers',
            'email',
            'location',
            'website',
            'phone',
            'birth_date',
            'date_joined',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
            'tweets':{'read_only': True},
            'date_joined': {'read_only': True}
        }

    def get_tweets(self, obj):
        user_tweets = []
        tweets_results = TweetService.find_tweets_by_user_id(obj.id)
        if tweets_results:
            for tweet in tweets_results:
                user_tweets.append(f'https://b2-twitter.herokuapp.com/twitter_api/tweets/{tweet.id}/')
        return user_tweets

    def get_follows(self, obj):
        follows = TwitterUserService.find_user_by_id(obj.id).get().follows.all()
        return [
            {
                "id": user.id,
                "name": user.username
            } for user in follows
        ]

    def get_followers(self, obj):
        followers = TwitterUserService.find_user_by_id(obj.id).get().followers.all()
        return [
            {
                "id": user.id,
                "name": user.username
            } for user in followers
        ]


class TweetSerializer(serializers.ModelSerializer):

    tweet_op = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    retweets = serializers.SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id',
            'text',
            'location',
            'tweet_op',
            'likes',
            'retweets'
        ]

    def get_tweet_op(self, obj):
        return obj.tweet_op.username

    def get_likes(self, obj):
        tweet_likes = []
        likes_result = TweetService.find_tweet_likes_by_id(obj.id)
        for like in likes_result:
            tweet_likes.append(like.id)
        return tweet_likes

    def get_retweets(self, obj):
        tweet_retweets = []
        retweets_results = TweetService.find_tweet_retweets_by_id(obj.id)
        for retweet in retweets_results:
            tweet_retweets.append(retweet.id)
        return tweet_retweets

