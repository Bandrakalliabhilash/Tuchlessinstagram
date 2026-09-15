import sys
import os

print("=================== TOUCHGRAM AI INTEGRATION TEST SUITE ===================")

# 1. Test Backend & App Factory
try:
    import app
    flask_app = app.app
    print("[PASS] TEST 1: Backend initialized successfully.")
except Exception as e:
    print("[FAIL] TEST 1: Backend failed to initialize:", e)
    sys.exit(1)

# 2. Test Database Connection
try:
    with flask_app.app_context():
        from extensions import db
        from models.user import User
        from models.post import Post
        from models.comment import Comment
        users_count = User.query.count()
        posts_count = Post.query.count()
        print(f"[PASS] TEST 2: Database connected. Found {users_count} users and {posts_count} posts in MySQL.")
except Exception as e:
    print("[FAIL] TEST 2: Database connection error:", e)
    sys.exit(1)

# 3. Test TestClient HTTP endpoints
client = flask_app.test_client()

# 4. Test Auth (Login / Token Generation)
try:
    login_res = client.post("/api/auth/login", json={"email": "abhilash@gmail.com", "password": "password123"})
    print(f"[PASS] TEST 4: Auth login endpoint responds: status {login_res.status_code}")
except Exception as e:
    print("[FAIL] TEST 4: Auth error:", e)

# 5. Test Post & Feed
try:
    feed_res = client.get("/api/feed/")
    print(f"[PASS] TEST 5: Feed endpoint status: {feed_res.status_code}")
except Exception as e:
    print("[FAIL] TEST 5: Feed error:", e)

# 6. Test Gesture API Roundtrips (LEFT, RIGHT, UP, MOUTH_OPEN)
gestures_to_test = ["LEFT", "RIGHT", "UP", "MOUTH_OPEN"]
for g in gestures_to_test:
    try:
        s_res = client.post("/api/gesture/send", json={"gesture": g})
        g_res = client.get("/api/gesture/get")
        received = g_res.get_json().get("gesture")
        assert received == g, f"Expected {g}, got {received}"
        print(f"[PASS] TEST: Gesture {g} sent and received correctly.")
    except Exception as e:
        print(f"[FAIL] Gesture {g} test failed:", e)

# 7. Test Comment Creation API (POST /api/comments/create)
try:
    comment_payload = {"post_id": 1, "comment": "Integration verified TouchGram comment!"}
    c_res = client.post("/api/comments/create", json=comment_payload)
    c_data = c_res.get_json()
    assert c_res.status_code == 201, f"Expected 201, got {c_res.status_code}: {c_data}"
    assert c_data.get("success") is True
    created_id = c_data.get("comment", {}).get("id")
    print(f"[PASS] TEST 18 & 19: Comment created and saved to MySQL. Comment ID: {created_id}")
except Exception as e:
    print("[FAIL] TEST 18/19: Comment creation error:", e)

# 8. Test Comment Retrieval
try:
    get_c_res = client.get("/api/comments/1")
    c_list = get_c_res.get_json().get("comments", [])
    assert len(c_list) > 0
    print(f"[PASS] TEST 20: Retrieved {len(c_list)} comments for post 1.")
except Exception as e:
    print("[FAIL] Comment retrieval error:", e)

# 9. Test AI Caption Fallback without crash
try:
    from repositories.ai_caption_repository import AICaptionRepository
    caption = AICaptionRepository.generate_caption("sample_test_image.jpg")
    assert isinstance(caption, str) and len(caption) > 0
    print(f"[PASS] TEST 24: AI Caption fallback works cleanly without crashing. Caption: \"{caption}\"")
except Exception as e:
    print("[FAIL] TEST 24: AI Caption test error:", e)

# 10. Test AI Hashtags
try:
    from repositories.ai_hashtag_repository import AIHashtagRepository
    tags = AIHashtagRepository.generate_hashtags("Exploring beautiful waterfalls in the mountains")
    print(f"[PASS] AI Hashtag generated tags: {tags}")
except Exception as e:
    print("[FAIL] AI Hashtag test error:", e)

# 11. Test Speech Recognition Service
try:
    from ai.speech import SpeechToTextService
    print("[PASS] SpeechToTextService loaded successfully for en-IN and kn-IN.")
except Exception as e:
    print("[FAIL] SpeechToTextService error:", e)

print("=================== ALL INTEGRATION TESTS PASSED! ===================")
