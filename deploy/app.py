import os.path
from flask import Flask
import os
import json
import run_backend

import time

app = Flask(__name__)

def get_predictions():
    count_id = 0
    links = []
    
    novos_links_json = "novos_links.json"
    ## Se o json não existir, buscamos novos links com a função update_db()
    if not os.path.exists(novos_links_json):
        run_backend.update_db()
    
    last_update = os.path.getmtime(novos_links_json) * 1e9

    with open("novos_links.json", 'r') as data_file:
        for line in data_file:
            line_json = json.loads(line)
            links.append(line_json)

    predictions = []
    for link in links:
        predictions.append((link['link_id'], link['titulo'], float(link['score'])))
    
    #Ordena do mais interessante ao menos interessante, apresentando apenas 30
    predictions = sorted(predictions, key=lambda x: x[2], reverse=True)[:30]


    predictions_formatted = []
    for e in predictions:
        count_id+=1
        predictions_formatted.append("""
            <tr><th>{title}</th><th>{score}</th><th><a href=\"{link}\"><svg class="bi bi-arrow-right-square-fill" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2zm5.646 10.646a.5.5 0 0 0 .708.708l3-3a.5.5 0 0 0 0-.708l-3-3a.5.5 0 1 0-.708.708L9.793 7.5H5a.5.5 0 0 0 0 1h4.793l-2.147 2.146z"/>
            </svg></a></th></tr>
            """.format(title=e[1], link=e[0], score=e[2]))
  
    return '\n'.join(predictions_formatted), last_update

#Decorato python onde passamos a requiseção. Neste caso para raiz
@app.route('/')
def main_page():
    preds, last_update = get_predictions()
    return """
    <head>
        <div class="card border-secondary mb-3"">

            <div class="card-header"><h1><center>Recomendador de Links do Google Scholar <svg class="bi bi-book-half" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
              <path fill-rule="evenodd" d="M12.786 1.072C11.188.752 9.084.71 7.646 2.146A.5.5 0 0 0 7.5 2.5v11a.5.5 0 0 0 .854.354c.843-.844 2.115-1.059 3.47-.92 1.344.14 2.66.617 3.452 1.013A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.276-.447L15.5 2.5l.224-.447-.002-.001-.004-.002-.013-.006-.047-.023a12.582 12.582 0 0 0-.799-.34 12.96 12.96 0 0 0-2.073-.609zM15 2.82v9.908c-.846-.343-1.944-.672-3.074-.788-1.143-.118-2.387-.023-3.426.56V2.718c1.063-.929 2.631-.956 4.09-.664A11.956 11.956 0 0 1 15 2.82z"/>
              <path fill-rule="evenodd" d="M3.214 1.072C4.813.752 6.916.71 8.354 2.146A.5.5 0 0 1 8.5 2.5v11a.5.5 0 0 1-.854.354c-.843-.844-2.115-1.059-3.47-.92-1.344.14-2.66.617-3.452 1.013A.5.5 0 0 1 0 13.5v-11a.5.5 0 0 1 .276-.447L.5 2.5l-.224-.447.002-.001.004-.002.013-.006a5.017 5.017 0 0 1 .22-.103 12.958 12.958 0 0 1 2.7-.869z"/>
            </svg></center></h1>
            </div>

            <div class="card-body text-secondary">
            <h5 class="card-title">Segundos antes da última atualização: {}</h5>
            </div>

        </div>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
    </head>

    <body>
    <table class="table">
        <thead class="thead-dark">
        <tr>
          <th scope="col">Título</th>
          <th scope="col">Score</th>
          <th scope="col">Link</th>
        </tr>
      </thead>
      <tbody>
             {}
      </tbody>
    </table>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
    </body>""".format((time.time_ns() - last_update) / 1e9, preds)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')