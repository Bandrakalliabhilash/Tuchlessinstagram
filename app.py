from flask import Flask
from config import Config
from flask_cors import CORS
# Extensions
from extensions import db, jwt, cors

# Routes
from routes.auth import auth
from routes.post import post
from routes.profile import profile
from routes.like import like
from routes.comment import comment
from routes.follow import follow
from routes.user import user
from routes.notification import notification
from routes.message import message
from routes.story import story
from routes.saved_post import saved_post
from routes.explore import explore
from routes.reel import reel
from routes.reel_like import reel_like
from routes.reel_comment import reel_comment
from routes.saved_reel import saved_reel
from routes.reel_share import reel_share
from routes.reel_view import reel_view
from routes.trending import trending
from routes.search import search
from routes.hashtag import hashtag
from routes.location import location
from routes.mention import mention
from routes.report import report
from routes.story_view import story_view
from routes.story_like import story_like
from routes.story_reply import story_reply
from routes.highlight import highlight
from routes.recommendation import recommendation
from routes.feed import feed
from routes.ai_caption import ai_caption
from routes.ai_hashtag import ai_hashtag
from routes.ai_moderation import ai_moderation
from routes.gesture import gesture
from routes.video import video_bp
from routes.speech import speech_bp



# Models (Import so SQLAlchemy creates tables)
from models.user import User
from models.post import Post
from models.comment import Comment
from models.like import Like
from models.follow import Follow
from models.notification import Notification
from models.message import Message
from models.story import Story
from models.saved_post import SavedPost
from models.reel import Reel
from models.reel_like import ReelLike
from models.reel_comment import ReelComment
from models.saved_reel import SavedReel
from models.reel_share import ReelShare
from models.reel_view import ReelView
from models.search_history import SearchHistory

from models.hashtag import Hashtag
from models.post_hashtag import PostHashtag
from models.reel_hashtag import ReelHashtag

from models.location import Location
from models.post_location import PostLocation
from models.reel_location import ReelLocation

from models.mention import Mention
from models.post_mention import PostMention
from models.reel_mention import ReelMention

from models.report import Report
from models.reported_post import ReportedPost
from models.reported_reel import ReportedReel
from models.reported_story import ReportedStory
from models.reported_comment import ReportedComment
from models.reported_user import ReportedUser

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(post)
    app.register_blueprint(profile)
    app.register_blueprint(like)
    app.register_blueprint(comment)
    app.register_blueprint(follow)
    app.register_blueprint(user)
    app.register_blueprint(notification)
    app.register_blueprint(message)
    app.register_blueprint(story)
    app.register_blueprint(saved_post)
    app.register_blueprint(explore)
    app.register_blueprint(reel)
    app.register_blueprint(reel_like)
    app.register_blueprint(reel_comment)
    app.register_blueprint(saved_reel)
    app.register_blueprint(reel_share)
    app.register_blueprint(reel_view)
    app.register_blueprint(trending)
    app.register_blueprint(search)
    app.register_blueprint(hashtag)
    app.register_blueprint(location)
    app.register_blueprint(mention)
    app.register_blueprint(report)
    app.register_blueprint(story_view)
    app.register_blueprint(story_like)
    app.register_blueprint(story_reply)
    app.register_blueprint(highlight)
    app.register_blueprint(recommendation)
    app.register_blueprint(feed)
    app.register_blueprint(ai_caption)
    app.register_blueprint(ai_hashtag)
    app.register_blueprint(ai_moderation)
    app.register_blueprint(gesture)
    app.register_blueprint(video_bp)
    app.register_blueprint(speech_bp)

    @app.route("/")
    def home():
        return {
            "success": True,
            "message": "Welcome to TouchGram AI API"
        }

    with app.app_context():
        try:
            db.create_all()
        except Exception as db_err:
            print(f"Database initialization notice: {db_err}")

    return app


app = create_app()

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 TouchGram AI Backend Server Starting...")
    print("📡 Base URL: http://127.0.0.1:5000")
    print("🗄️ Database Connected: MySQL (touchgram)")
    print("✨ Available Services:")
    print("   • Gestures:         /api/gesture/send, /api/gesture/get")
    print("   • Comments:         /api/comments/create, /api/comments/<id>")
    print("   • Speech-to-Text:   /api/speech/transcribe (en-IN, kn-IN)")
    print("   • Posts & Feed:     /api/posts, /api/feed")
    print("   • Reels:            /api/reels, /api/reel-comments")
    print("   • AI Caption:       /api/ai/caption (Lazy loaded)")
    print("   • AI Hashtags:      /api/ai/hashtag")
    print("=" * 60)
    app.run(host="0.0.0.0", port=5000, debug=True)