import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import re
import joblib as jb
from scipy.sparse import hstack

mdl_rf = jb.load("random_forest.pkl.z")
mdl_lgbm = jb.load("lgbm.pkl.z")
vectorizer = jb.load("vectorizer.pkl.z")

##Limpa caracteres desnecessários
def clean_data(cols_list, char_list, data):
	for col in cols_list:
		for char in char_list:
			data[col] = data[col].replace(char, '')
	return data

##Converte tipo das colunas
def cols_to_convert(cols, data):
	for col in cols:
		data[col] = data[col].astype('int32')


##Limpa coluna ano
def limpa_coluna_ano(data):
	coluna_ano = data['ano'].copy()

	for i in range(len(coluna_ano)):
	    if(len(coluna_ano[i])>4):
	        res = re.findall(r'\d{4}', coluna_ano[i])
	        if(len(res)>1):
	            coluna_ano[i] = res[len(res)-1]
	        else:
	            coluna_ano[i] = res[0]
	coluna_ano = coluna_ano.astype('int32')
	return coluna_ano

##Codifica coluna 'tipo_arquivo'
def encode_tipo_arquivo(data):
	data['CITAÇÃO'] = 0.0
	data['DOC'] = 0.0
	data['HTML'] = 0.0
	data['LIVRO'] = 0.0
	data['PDF'] = 0.0
	tipo_str = str(data['tipo_arquivo'])
	tipo = tipo_str[tipo_str.find('[')+len('['):tipo_str.rfind(']')]
	data[tipo] = [1.0]
	return data

## Transforma a coluna 'titulo'
def transforma_titulo(col):
	titulo_vec = vectorizer.transform([str(col)])
	df_titulo = pd.DataFrame(titulo_vec.toarray(), columns=vectorizer.get_feature_names())
	return df_titulo

##Define o array de features
def create_features(data):
	cols_to_clean = ['citacoes', 'ano', 'tipo_arquivo', 'versao']
	spec_chars = ["[", "]", "'", ".", ",", " "]

	##Limpa colunas
	cleaned_data = clean_data(cols_to_clean, spec_chars, data)

	##Converte colunas
	int_columns = ['citacoes', 'versao']
	cols_to_convert(int_columns, cleaned_data)

	##Limpa coluna 'ano'
	cleaned_data['ano'] = limpa_coluna_ano(cleaned_data)

	##Codifica coluna 'tipo_arquivo'
	data = encode_tipo_arquivo(cleaned_data)

	##Transforma a coluna 'titulo'
	titulo = transforma_titulo(data['titulo'])
	
	##array de features
	data = data[['citacoes', 'ano', 'versao', 'CITAÇÃO', 'DOC', 'HTML', 'LIVRO', 'PDF']]
	feature_array = data.join(titulo)

	return feature_array

##Calcula a previsão
def compute_prediction(data):
	if(len(data['ano'])>1):
		return 0
	else:
		df = pd.DataFrame.from_dict(data)
		features = create_features(df)

		predict_rf = mdl_rf.predict_proba(features)[0][1]

		predict_lgbm = mdl_lgbm.predict_proba(features)[0][1]

		predict_ensemble = 0.5*predict_rf + 0.5*predict_lgbm
		
		formated_result = round((predict_ensemble*100), 2)

	return formated_result

##Para monitoramento das previsões
def log_data(data, feature_array, p):
    link_id = data.get('titulo', '')
    data['prediction'] = p
    data['feature_array'] = feature_array.todense().tolist()
    #print(video_id, json.dumps(data))

