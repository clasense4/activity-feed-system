from config.bootstrap import app
from controllers import me_controller, activity_controller

me = me_controller.controller()
app.add_url_rule('/me', methods=['GET'], view_func=me.me)

activity = activity_controller.controller()
app.add_url_rule('/activity', methods=['POST'], view_func=activity.activity)

if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')
