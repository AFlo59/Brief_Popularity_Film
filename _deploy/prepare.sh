echo "copy modelisation/score_datasets to scrap/modelisation/score_datasets"
cp -r ../modelisation/score_datasets ../scrap/modelisation/score_datasets

echo "copy modelisation/functions.py & modelisation/converter.py to scrap/modelisation/functions.py & scrap/modelisation/converter.py"
cp ../modelisation/functions.py ../scrap/modelisation/functions.py
cp ../modelisation/converter.py ../scrap/modelisation/converter.py

echo "copy modelisation/model.pkl & modelisation/pipe_transform.pkl to scrap/_data_prediction/model.pkl & scrap/_data_prediction/pipe_transform.pkl"
cp ../modelisation/model.pkl ../scrap/_data_prediction/model.pkl
cp ../modelisation/pipe_transform.pkl ../scrap/_data_prediction/pipe_transform.pkl