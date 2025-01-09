from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .services.main import my_service_logic  # Import the service layer function
#from .services.version2.main import execute_query  # Import the service layer function
import json
import spacy
from textblob import TextBlob
import rdflib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Define the view (controller) that uses the service layer
# @csrf_exempt
# def my_view(request):
#     result = my_service_logic()  # Call the service layer function
#     return JsonResponse(result)  # Return the result in the response

# @csrf_exempt
# def sparqview(request):

#     if request.method == 'POST':
#         try:
#             # Parse the incoming JSON data from the request body
#             data = json.loads(request.body)
#             query = data.get("string", "")
            
#             if not query:
#                 return JsonResponse({"status": "error", "message": "No query string provided."}, status=400)

#             # Call the service layer function to execute the SPARQL query
#             result = execute_query(query)
            
#             # Return the result in the response
            
#             return JsonResponse({"status": "success", "result": result})

#         except json.JSONDecodeError:
#             return JsonResponse({"status": "error", "message": "Invalid JSON in request body."}, status=400)
#     else:
#         # Handle methods that are not POST
#         return JsonResponse({"status": "error", "message": "Method Not Allowed."}, status=405)
    
# @csrf_exempt
# def sparqview1(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         query = data.get("string", data)
#         return JsonResponse({"status": "true", "message": query }, status=200)



# Charger le modèle spaCy pour la reconnaissance d'entités nommées (NER)
nlp = spacy.load("en_core_web_sm")
@csrf_exempt
def analyze_text(request):
    if request.method == 'POST':
        try:
            # Récupérer le texte envoyé dans la requête
            body = json.loads(request.body)
            text = body.get('text', '')
            
            if not text:
                return JsonResponse({'error': 'Text field is required'}, status=400)
            
            # Exécution de l'analyse NLP avec spaCy
            doc = nlp(text)
            
            # Extraction des entités nommées
            entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
            
            # Utilisation de TextBlob pour l'analyse de texte
            blob = TextBlob(text)
            keywords = list(blob.noun_phrases)
            sentiment = {
                'polarity': blob.sentiment.polarity,
                'subjectivity': blob.sentiment.subjectivity
            }
            
            # Création d'un graphe RDF et sérialisation
            rdf_graph = rdflib.Graph()
            rdf_graph.parse("http://dbpedia.org/resource/Albert_Camus", format="xml")
            rdf_data = rdf_graph.serialize(format='turtle')  # Suppression de .decode('utf-8')
            
            # Préparer les données pour la réponse JSON
            result = {
                'entities': entities,
                'keywords': keywords,
                'sentiment': sentiment,
                'rdf_data': rdf_data
            }
            
            return JsonResponse(result, safe=False, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
