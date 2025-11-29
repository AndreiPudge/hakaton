import React, { useState } from "react";
import '../static/centralblock.css';

const formatCurrency = (value) =>
  new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
    maximumFractionDigits: 0,
  }).format(value);

const CentralBlock = ({
  predictedIncome,
  lowerBound,
  upperBound,
  confidence,
  featureImportances,
  textExplanation,
}) => {
  const [activeTab, setActiveTab] = useState("chart");

  const confidencePercent =
    confidence !== undefined && confidence !== null
      ? Math.round(confidence * 100)
      : null;

  const maxAbsImportance =
    featureImportances && featureImportances.length > 0
      ? Math.max(...featureImportances.map((f) => Math.abs(f.value)))
      : 1;

  return (
    <div className="central-block">
      {/* ПРОГНОЗ ДОХОДА */}
      <section className="card prediction-card">
        <h2 className="card-title">Прогноз дохода клиента</h2>

        <div className="prediction-main">
          <div className="prediction-icon">₽</div>
          <div className="prediction-info">
            <div className="prediction-label">Прогнозируемый доход</div>
            <div className="prediction-value">
              {formatCurrency(predictedIncome)} / месяц
            </div>
          </div>
        </div>

        <div className="prediction-extra">
          {lowerBound !== undefined &&
            lowerBound !== null &&
            upperBound !== undefined &&
            upperBound !== null && (
              <div className="prediction-row">
                <span className="prediction-row-label">Диапазон (95%):</span>
                <span>
                  {formatCurrency(lowerBound)} — {formatCurrency(upperBound)}
                </span>
              </div>
            )}

          {confidencePercent !== null && (
            <div className="prediction-row">
              <span className="prediction-row-label">Уверенность модели:</span>
              <div className="confidence-wrapper">
                <div className="confidence-bar">
                  <div
                    className="confidence-fill"
                    style={{ width: `${confidencePercent}%` }}
                  />
                </div>
                <span className="confidence-label">
                  {confidencePercent}%
                </span>
              </div>
            </div>
          )}
        </div>

        <p className="prediction-note">
          Прогноз основан на данных о возрасте, типе занятости, транзакционной
          активности и кредитной нагрузке клиента.
        </p>
      </section>

      {/* ОБЪЯСНЕНИЕ ПРОГНОЗА */}
      <section className="card explanation-card">
        <h2 className="card-title">
          Почему доход = {formatCurrency(predictedIncome)}?
        </h2>

        {/* Табы */}
        <div className="tabs">
          <button 
            className={`tab ${activeTab === "chart" ? "active" : ""}`}
            onClick={() => setActiveTab("chart")}
          >
            График факторов
          </button>
          <button 
            className={`tab ${activeTab === "text" ? "active" : ""}`}
            onClick={() => setActiveTab("text")}
          >
            Текстовое объяснение
          </button>
        </div>

        {/* Содержимое табов */}
        {activeTab === "chart" ? (
          <div className="features-chart">
            {!featureImportances || featureImportances.length === 0 ? (
              <div className="empty-state">
                Нет данных о вкладах признаков для этого клиента.
              </div>
            ) : (
              <>
                <ul className="features-list">
                  {featureImportances.map((feature) => {
                    const widthPercent =
                      (Math.abs(feature.value) / maxAbsImportance) * 100 || 0;
                    const isPositive = feature.value >= 0;
                    return (
                      <li key={feature.name} className="feature-item">
                        <div className="feature-header">
                          <span className="feature-name">
                            {feature.name}
                          </span>
                          <span
                            className={`feature-value ${
                              isPositive
                                ? "feature-value--pos"
                                : "feature-value--neg"
                            }`}
                          >
                            {isPositive ? "+" : "−"}
                            {formatCurrency(Math.abs(feature.value))}
                          </span>
                        </div>
                        <div className="feature-bar">
                          <div
                            className={`feature-bar-fill ${
                              isPositive
                                ? "feature-bar-fill--pos"
                                : "feature-bar-fill--neg"
                            }`}
                            style={{ width: `${widthPercent}%` }}
                          />
                        </div>
                      </li>
                    );
                  })}
                </ul>
                <p className="chart-note">
                  Положительные значения увеличивают прогноз дохода, отрицательные —
                  снижают.
                </p>
              </>
            )}
          </div>
        ) : (
          <div className="text-explanation">
            {!textExplanation ? (
              <div className="empty-state">
                Текстовое объяснение для этого прогноза отсутствует.
              </div>
            ) : (
              <p>{textExplanation}</p>
            )}
          </div>
        )}
      </section>
    </div>
  );
};

export default CentralBlock;