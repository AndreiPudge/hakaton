import {makeAutoObservable} from "mobx"

class ClientStore{
    list=[]
    searchQuery = "";
    loading = false;
    error = null;
    selectedClient = null; // объект выбранного клиента

    constructor() {
        makeAutoObservable(this, {}, { autoBind: true });
    }

    setSearchQuery(value){
        this.searchQuery = value;
    }

    async fetchClients(){
        if (!this.searchQuery || this.searchQuery.trim() === "") {
            this.list = [];
            return;
        }

        this.loading = true;
        this.error = null;

        try {
            const resp = await fetch(`/api/clients?search=${encodeURIComponent(this.searchQuery)}`)
            if (!resp.ok) {
                throw new Error("Ошибка загрузки клиентов");
            }
            const data = await resp.json();
            this.list = data;
        }catch(err){
            this.error = err.message || "Ошибка загрузки клиентов";
            this.list = [];
        }finally{
            this.loading = false;
        }
    }

  selectClient(client){
    this.selectedClient = client;
  }

  clear() {
    this.list = [];
    this.selectedClient = null;
    this.searchQuery = "";
    this.error = null;
  }
}
export const clientStore = new ClientStore()