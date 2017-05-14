""" app start"""

import phrase_corrector
import topic_modeling

if __name__ == '__main__':

    from flask import Flask, request
    from flask_restful import Resource, Api

    APP = Flask(__name__)
    API = Api(APP)

    class PharseCorrector(Resource):
        """ phrase corrector """
        def get(self):
            """ get the corrected phrase for misspelled phrase """
            phrase = request.args.get('phrase')
            cleaned_query, prob = phrase_corrector.cleanQuery(phrase)
            return {"query": phrase, "cleaned_query": cleaned_query, "prob": prob}

    class PharseSimilarity(Resource):
        """ topic modeling """
        def get(self):
            """ get similar phrase for a phrase """
            phrase = request.args.get('phrase')
            simliar_queries = topic_modeling.get_similar_queries(phrase)
            return simliar_queries

    API.add_resource(PharseCorrector, '/corrector')
    API.add_resource(PharseSimilarity, '/similar')

    # app.run(debug=True)
    APP.run(port=int("5001"), threaded=True)
    