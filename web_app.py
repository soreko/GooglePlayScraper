from flask import Flask, Response
from flask_restful import Api, reqparse
from flask_cors import CORS
from werkzeug import exceptions


class MyWebApp:
    """
    Web application that can be activate by its function run()
    """

    _app = None
    _queue = None
    _api = None
    _host = ""
    _port = 0

    def __init__(self, queue, host, port):

        self._queue = queue
        self._host = host
        self._port = port

        self._create_app()

    def _create_app(self):
        self._app = Flask(__name__)
        self._api = Api(self._app)
        CORS(self._app)

        @self._app.route('/ScrapApp', methods=['GET'])
        def get_app_details():
            """
            gets an id of a google store app, and applies the scraper for this id
            :return:
            """
            try:
                # parse query arguments
                args = self._argument_parser([['id', str, True]])

                self._queue.put(args['id'])

                response = Response(response="Done")

            except exceptions.HTTPException as e:
                self._app.logger.error("get_app_details() failed: {}".format(e))
                response = Response(response=str(e.data), status=e.code)

            except Exception as e:
                self._app.logger.error("get_app_details() failed: {}".format(e))
                response = Response(response="Internal Server Error", status=500)

            return response

    @staticmethod
    def _argument_parser(args, location='args'):
        """
        parse arguments from request
        :param args: list of [name, type, required]
        :param location: argument location (query, body, headres)
        :return: dictionary of {arg_name: arg_value}
        """
        parser = reqparse.RequestParser()
        for argument in args:
            parser.add_argument(argument[0], type=argument[1], location=location,
                                help='%s argument must contain %s, and located in %s' %
                                     (argument[0], argument[1], location),
                                required=argument[2])
        return parser.parse_args()

    def run(self):
        self._app.run(debug=False, host=self._host, port=self._port)
