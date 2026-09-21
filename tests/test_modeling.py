import numpy as np
import pandas as pd
from alveolar_pheno.modeling import fit_interpretable_model, rank_features
from alveolar_pheno.evaluation import evaluate


def test_model_train_evaluate_and_rank_features():
    rng = np.random.default_rng(2)
    rows=[]
    for cls,mu in [("a",0.0),("b",2.0),("c",4.0)]:
        for _ in range(20):
            rows.append({"phenotype":cls,"batch":"batch_1","f1":rng.normal(mu,0.4),"f2":rng.normal(mu,0.5)})
    df=pd.DataFrame(rows)
    bundle=fit_interpretable_model(df)
    metrics=evaluate(bundle,df)
    ranking=rank_features(bundle)
    assert metrics["macro_f1"] > 0.8
    assert set(ranking["feature"]) == {"f1","f2"}
