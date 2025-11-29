import React, { useState } from "react";
import '../static/recommendation.css';

export const RecommendationsBlock = ({ offers }) => {
  // offers: массив объектов вида:
  // {
  //   id: string | number,
  //   name: string,
  //   productType: "credit" | "deposit" | "investment" | "card" | "other",
  //   shortDescription: string,
  //   reason: string, // почему рекомендовано
  //   approvalProbability?: number, // 0..1
  //   incomeSegment?: string, // "до 60k", "60-120k", "120k+"
  //   riskLevel?: "low" | "medium" | "high"
  // }

  const [activeFilter, setActiveFilter] = useState("all");

  const filterButtons = [
    { id: "all", label: "Все" },
    { id: "credit", label: "Кредиты" },
    { id: "card", label: "Карты" },
    { id: "deposit", label: "Вклады" },
    { id: "investment", label: "Инвестиции" },
  ];

  const filteredOffers =
    activeFilter === "all"
      ? offers
      : offers.filter((offer) => offer.productType === activeFilter);

  const formatProbability = (p) => {
    if (p === null || p === undefined) return null;
    return Math.round(p * 100);
  };

  const getRiskLabel = (risk) => {
    if (!risk) return null;
    if (risk === "low") return "Низкий риск";
    if (risk === "medium") return "Средний риск";
    if (risk === "high") return "Высокий риск";
    return risk;
  };

  return (
    <aside className="recommendations-block">
      <section className="card recommendations-card">
        <div className="recommendations-header">
          <h2 className="card-title">Персональные предложения</h2>
          <p className="card-subtitle">
            Продукты, подобранные на основе прогноза дохода и профиля клиента.
          </p>
        </div>

        {/* Фильтры по типу продукта */}
        <div className="recommendations-filters">
          {filterButtons.map((btn) => (
            <button
              key={btn.id}
              className={`rec-filter-btn ${activeFilter === btn.id ? "rec-filter-btn--active" : ""}`}
              onClick={() => setActiveFilter(btn.id)}
            >
              {btn.label}
            </button>
          ))}
        </div>

        {/* Список предложений */}
        <div className="offers-list">
          {!filteredOffers || filteredOffers.length === 0 ? (
            <div className="empty-state">
              Нет подходящих предложений для выбранного фильтра.
            </div>
          ) : (
            filteredOffers.map((offer) => {
              const prob = formatProbability(offer.approvalProbability);
              const riskLabel = getRiskLabel(offer.riskLevel);

              return (
                <article key={offer.id} className="offer-card">
                  <div className="offer-header">
                    <h3 className="offer-title">{offer.name}</h3>
                    {offer.incomeSegment && (
                      <span className="offer-chip">
                        Доход: {offer.incomeSegment}
                      </span>
                    )}
                  </div>

                  <p className="offer-description">
                    {offer.shortDescription}
                  </p>

                  <div className="offer-meta">
                    {prob !== null && (
                      <div className="offer-meta-item">
                        <span className="offer-meta-label">
                          Вероятность одобрения:
                        </span>
                        <span className="offer-meta-value">
                          {prob}%
                        </span>
                      </div>
                    )}

                    {riskLabel && (
                      <div className="offer-meta-item">
                        <span className="offer-meta-label">Риск:</span>
                        <span
                          className={`offer-meta-value offer-meta-risk offer-meta-risk--${
                            offer.riskLevel || "unknown"
                          }`}
                        >
                          {riskLabel}
                        </span>
                      </div>
                    )}
                  </div>

                  <div className="offer-reason-block">
                    <div className="offer-reason-label">
                      Почему рекомендовано:
                    </div>
                    <p className="offer-reason-text">{offer.reason}</p>
                  </div>

                  <div className="offer-actions">
                    <button className="offer-btn offer-btn--primary">
                      Добавить в предложение клиенту
                    </button>
                    <button className="offer-btn offer-btn--ghost">
                      Подробнее
                    </button>
                  </div>
                </article>
              );
            })
          )}
        </div>
      </section>
    </aside>
  );
};