# import tkinter as tk
# from tkinter import filedialog, messagebox
# import rdflib

# # Initialize the RDF graph
# graph = rdflib.Graph()

# # Function to upload the RDF file
# def upload_rdf():
#     graph.parse("djangoproject/myapp/services/version2/rdf-protege.rdf", format="xml")  

# # Function to execute SPARQL query
# def execute_query(query):

#     upload_rdf()
#     # Execute the SPARQL query on the RDF graph
#     results = graph.query(query)
#     data = [
#         {"LivreTitle": str(row.LivreTitle), "AuteurName": str(row.AuteurName)}
#         for row in results
#     ]
    
#     return data
   
import spacy
from textblob import TextBlob
import rdflib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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
