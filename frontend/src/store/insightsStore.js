import { makeAutoObservable } from "mobx";

class InsightsStore {
  loading = false;
  error = null;
  prediction = null;         // { predictedIncome, lowerBound, upperBound, confidence }
  featureImportances = [];   // [{ name, value }]
  textExplanation = "";
  offers = [];               // список продуктов

  constructor() {
    makeAutoObservable(this, {}, { autoBind: true });
  }

  async fetchInsights(clientId) {
    if (!clientId) return;

    this.loading = true;
    this.error = null;

    try {
      const resp = await fetch(`/api/clients/${clientId}/insights`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}), // или передайте нужные данные
      });
      
      if (!resp.ok) {
        throw new Error("Ошибка загрузки прогноза");
      }
      
      const data = await resp.json();
      // ... обработка данных
    } catch (err) {
      // ... обработка ошибок
    } finally {
      this.loading = false;
    }
  }

  /*async fetchInsights(clientId) {
    if (!clientId) return;

    this.loading = true;
    this.error = null;

    try {
      const resp = await fetch(`/api/clients/${clientId}/insights`);
      if (!resp.ok) {
        throw new Error("Ошибка загрузки прогноза");
      }
      const data = await resp.json();

      this.prediction = data.prediction || null;
      this.featureImportances = data.featureImportances || [];
      this.textExplanation = data.textExplanation || "";
      this.offers = data.offers || [];
    } catch (err) {
      this.error = err.message || "Ошибка загрузки прогноза";
      this.prediction = null;
      this.featureImportances = [];
      this.textExplanation = "";
      this.offers = [];
    } finally {
      this.loading = false;
    }
  } */

  clear() {
    this.loading = false;
    this.error = null;
    this.prediction = null;
    this.featureImportances = [];
    this.textExplanation = "";
    this.offers = [];
  }
}

export const insightsStore = new InsightsStore();