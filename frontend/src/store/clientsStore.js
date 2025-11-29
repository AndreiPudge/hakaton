import { makeAutoObservable } from "mobx"
import { api } from "../api/api";

class ClientStore {
    list = []
    searchQuery = "";
    loading = false;
    error = null;
    selectedClient = null;
    page = 1;
    totalCount = 0;
    limit = 10;

    constructor() {
        makeAutoObservable(this, {}, { autoBind: true });
    }

    setSearchQuery(value) {
        this.searchQuery = value;
    }

    setPage(newPage) {
        this.page = newPage;
    }

    setLimit(newLimit) {
        this.limit = newLimit;
    }

    // Загрузка всех клиентов (для таблицы при загрузке)
    async fetchAllClients() {
        this.loading = true;
        this.error = null;

        try {
            const data = await api.clients.getAll(this.page, this.limit);
            this.list = data.clients || data.items || data;
            this.totalCount = data.totalCount || data.total || data.length;
        } catch (err) {
            this.error = err.message || "Ошибка загрузки клиентов";
            this.list = [];
            this.totalCount = 0;
        } finally {
            this.loading = false;
        }
    }

    // Поиск клиентов
    async fetchClients() {
        if (!this.searchQuery || this.searchQuery.trim() === "") {
            // Если поиск пустой - загружаем всех клиентов
            await this.fetchAllClients();
            return;
        }

        this.loading = true;
        this.error = null;

        try {
            const data = await api.clients.search(this.searchQuery);
            this.list = data.clients || data;
            this.totalCount = data.totalCount || data.length;
        } catch (err) {
            this.error = err.message || "Ошибка загрузки клиентов";
            this.list = [];
            this.totalCount = 0;
        } finally {
            this.loading = false;
        }
    }

    // Получить клиента по ID
    async fetchClientById(clientId) {
        this.loading = true;
        this.error = null;

        try {
            const client = await api.clients.getById(clientId);
            return client;
        } catch (err) {
            this.error = err.message || "Ошибка загрузки клиента";
            return null;
        } finally {
            this.loading = false;
        }
    }

    selectClient(client) {
        this.selectedClient = client;
    }

    clear() {
        this.list = [];
        this.selectedClient = null;
        this.searchQuery = "";
        this.error = null;
        this.page = 1;
        this.totalCount = 0;
    }

    // Пагинация
    nextPage() {
        if (this.page < Math.ceil(this.totalCount / this.limit)) {
            this.page++;
            this.fetchAllClients();
        }
    }

    prevPage() {
        if (this.page > 1) {
            this.page--;
            this.fetchAllClients();
        }
    }

    goToPage(pageNumber) {
        if (pageNumber >= 1 && pageNumber <= Math.ceil(this.totalCount / this.limit)) {
            this.page = pageNumber;
            this.fetchAllClients();
        }
    }
}

export const clientStore = new ClientStore();