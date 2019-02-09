from config.bootstrap import app
from controllers import me_controller, activity_controller, follow_controller

me = me_controller.controller()
app.add_url_rule('/me', methods=['GET'], view_func=me.me)

activity = activity_controller.controller()
app.add_url_rule('/activity', methods=['POST'], view_func=activity.activity)

follow = follow_controller.controller()
app.add_url_rule('/follow', methods=['POST'], view_func=follow.follow)

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')
