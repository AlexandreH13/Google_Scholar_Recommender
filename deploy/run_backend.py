from get_data import *
from ml_utils import *
import json
import time

queries = ["machine+learning", "algoritmos+geneticos"]

def update_db():
    with open("novos_links.json", 'w+') as output:
        for query in queries:
            
            for page in range(1,4):
                search_page = download_search_page(page, query)
                link_list = parse_search_page(search_page)

                for link in link_list:
                    if link['titulo']=="":
                        return 0
                        
                    p = compute_prediction(link)

                    link_id = link['link']
                    data_front = {"titulo": link['titulo'], "score": float(p), "link_id": link_id}
                    data_front['update_time'] = time.time_ns()

                    print(link_id, json.dumps(data_front))
                    output.write("{}\n".format(json.dumps(data_front)))
    return True