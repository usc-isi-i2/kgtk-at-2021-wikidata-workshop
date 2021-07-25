import sys
import time
from SPARQLWrapper import SPARQLWrapper, JSON


endpoint_url = "https://dsbox02.isi.edu:8888/bigdata/namespace/wdq/sparql"
#endpoint_url = "https://query.wikidata.org/sparql"

test_query = """
select ?p ?o where {
?a wdt:P31 wd:Q5 .
?a ?p ?o
}limit 10
"""

query_common_names = """
SELECT distinct ?given_name (count(?given_name) as ?count) ?given_name_label
WHERE
{
  ?person wdt:P31 wd:Q5.
  ?person wdt:P735 ?given_name.
  ?given_name rdfs:label ?given_name_label .
  filter(lang(?given_name_label) = 'en')

}group by ?given_name ?given_name_label
order by desc (?count)
"""

query_instances = """
SELECT distinct ?superclass (count(?entity) as ?count)
WHERE
{
  ?entity wdt:P31 ?class.
  ?class wdt:P279* ?superclass

}group by ?superclass
order by desc (?count)
"""

query_film_instances = """
select distinct ?class ?class_label (count(?instance) as ?instance_count) where{
 ?instance wdt:P31 ?class.
 ?class wdt:P279* wd:Q11424 .
 ?class rdfs:label ?class_label .
  filter(lang(?class_label) = 'en')
 }
group by ?class ?class_label
order by desc (?instance_count)
"""

query_author_network = """
select distinct ?author1 ?author2 (count(?pub) as ?count) where{
 ?pub wdt:P31 ?class.
 ?class wdt:P279* wd:Q591041 .
 ?pub wdt:P577 ?date .
 ?pub wdt:P50 ?author1.
 ?pub wdt:P50 ?author2.
  filter (?author1 != ?author2)
 }
group by ?author1 ?author2
order by desc (?count)
"""

query_author_network_cancer = """
select distinct ?author1 ?author2 (count(?pub) as ?count) where{
 ?pub wdt:P31 ?class.
 ?class wdt:P279* wd:Q591041 .
 ?pub wdt:P577 ?date .
 ?pub wdt:P50 ?author1.
 ?pub wdt:P50 ?author2.
 ?pub wdt:P921 ?cancer_type.
 ?cancer_type wdt:P279* wd:Q12078 .
  filter (?author1 != ?author2)
 }
group by ?author1 ?author2
order by desc (?count)
"""

#with open('ulan_query.txt', 'r') as file:
#    query_ulan_ids = file.read()
#    print ("ulan query read successfully")

def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def measure_time_for_query(endpoint_url,query):
    start = time.time()
    print("performing query...")
    results = get_results(endpoint_url, query)
    end = time.time()
    print("TOTAL TIME for query (in ms)")
    print(end - start)
    return results

print("Executing test query")
measure_time_for_query(endpoint_url, test_query)


# silly way but there are only 6 queries
print("Executing common names query")
measure_time_for_query(endpoint_url, query_common_names)

print("Executing instances query (count elements of all classes)")
measure_time_for_query(endpoint_url, query_instances)

print("Executing film instances query (same as above, but restricted to film)")
measure_time_for_query(endpoint_url, query_film_instances)

print("Executing author network query")
measure_time_for_query(endpoint_url, query_author_network)

print("Executing author network query, with topic cancer")
measure_time_for_query(endpoint_url, query_author_network_cancer)

#Can't do this query this way because it's too long
#print("Executing ulan_id query with all ids (27.000) as part of the values")
#measure_time_for_query(endpoint_url, query_ulan_ids)

#for result in results["results"]["bindings"]:
#    print(result)
