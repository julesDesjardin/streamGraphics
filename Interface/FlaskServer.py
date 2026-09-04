import flask
import threading


class FlaskServer:
    def __init__(self, port, queueGroupsInput, queueGroupsOutput, queueButtons, queueReload, queueReloadDone):
        self.port = port
        self.queueGroupsInput = queueGroupsInput
        self.queueGroupsOutput = queueGroupsOutput
        self.queueButtons = queueButtons
        self.queueReload = queueReload
        self.queueReloadDone = queueReloadDone
        self.app = flask.Flask(__name__)

        self.app.add_url_rule(
            "/groups",
            "groups",
            self.groupsCallback,
            methods=["GET"],
        )

        self.app.add_url_rule(
            "/button",
            "button",
            self.buttonCallback,
            methods=["POST"],
        )

        self.app.add_url_rule(
            "/reload",
            "reload",
            self.reloadCallback,
            methods=["POST"],
        )

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    def run(self):
        self.app.run(
            port=self.port
        )

    def groupsCallback(self):
        venues = flask.request.args.getlist("venue")
        rooms = flask.request.args.getlist("room")
        events = flask.request.args.getlist("event")
        rounds = flask.request.args.getlist("round")
        groups = flask.request.args.getlist("group")

        data = []
        for i in range(min(len(venues), len(rooms), len(events), len(rounds), len(groups))):
            data.append((venues[i], rooms[i], events[i], rounds[i], groups[i]))

        self.queueGroupsInput.put(data)
        while self.queueGroupsOutput.empty():
            pass

        result = self.queueGroupsOutput.get()
        return flask.jsonify({"status": "ok", "result": result})

    def buttonCallback(self):
        payload = flask.request.get_json(force=True)

        camera = payload["camera"]
        buttonId = payload["buttonId"]

        print(f"{camera=}, {buttonId=}")
        self.queueButtons.put({"camera": camera, "buttonId": buttonId})

        return flask.jsonify({"status": "ok"})

    def reloadCallback(self):
        self.queueReload.put('')

        while self.queueReloadDone.empty():
            pass

        _ = self.queueReloadDone.get()
        return flask.jsonify({"status": "ok"})
