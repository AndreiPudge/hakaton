import React from "react";
import { observer } from "mobx-react-lite";
import  CentralBlock  from "./CentralBlock";
import { RecommendationsBlock } from "./recommendation";
import { insightsStore } from "../store/insightsStore";
import  Table  from "./table";

export const MainPage = observer(() => {
  const {
    prediction,
    featureImportances,
    textExplanation,
    offers,
    loading,
    error,
  } = insightsStore

  return (
   <main className='main'>
      <Table />
      <div>
        {loading && (
          <div className="card">
            <p>Загрузка прогноза...</p>
          </div>
        )}
        {error && !loading && (
          <div className="card">
            <p style={{ color: "red" }}>{error}</p>
          </div>
        )}
        {!prediction && !loading && !error && (
          <div className="card">
            <p style={{ fontSize: 13, color: "#9ca3af" }}>
              Выберите клиента слева, чтобы увидеть прогноз дохода.
            </p>
          </div>
        )}
        {prediction && !loading && (
          <CentralBlock
            predictedIncome={prediction.predictedIncome}
            lowerBound={prediction.lowerBound}
            upperBound={prediction.upperBound}
            confidence={prediction.confidence}
            featureImportances={featureImportances}
            textExplanation={textExplanation}
          />
        )}
      </div>
      <div>
        <RecommendationsBlock offers={offers || []} />
      </div>
    </main>
  );
});