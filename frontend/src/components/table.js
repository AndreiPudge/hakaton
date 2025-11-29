import React, {useState, useEffect} from 'react';
import Pages from './pagintaion';
import '../static/table.css';
import {observer} from 'mobx-react-lite'
import { clientStore } from '../store/clientsStore';
import { insightsStore } from '../store/insightsStore';

const Table = observer(() => {
    const {list, searchQuery, loading, error, selectedClient, setSearchQuery, fetchClients, selectClient} = clientStore
    
    const handleSearchClick = () => {
        fetchClients()
    }
    
    const handleClientClick = (client) => {
        selectClient(client)
        insightsStore.fetchInsights(client.id)
    }

    const [users] = useState([
        {
            id: 1,
            name: "John Doe",
            userId: "#SPK1001",
            product: "Wrist Watch",
            orderedDate: "2024-10-05",
            orderedTime: "12:45PM",
            status: "Shipped",
            totalAmount: "$150.00",
            paymentMethod: "Credit Card",
            paymentDetails: "*******1111"
        },
        {
            id: 2,
            name: "Jane Smith",
            userId: "#SPK1002",
            product: "Teddy Bear",
            orderedDate: "2024-10-04",
            orderedTime: "10:30AM",
            status: "Pending",
            totalAmount: "$230.00",
            paymentMethod: "MasterCard",
            paymentDetails: "*******4444"
        },
        {
            id: 3,
            name: "Bob Lee",
            userId: "#SPK1003",
            product: "Shoes",
            orderedDate: "2024-10-03",
            orderedTime: "03:15PM",
            status: "Delivered",
            totalAmount: "$120.00",
            paymentMethod: "Bank Transfer",
            paymentDetails: "Direct Payment"
        },
        {
            id: 4,
            name: "Alice Johnson",
            userId: "#SPK1004",
            product: "Over Coat",
            orderedDate: "2024-10-02",
            orderedTime: "09:20AM",
            status: "Cancelled",
            totalAmount: "$85.00",
            paymentMethod: "American Express",
            paymentDetails: "*****10005"
        },
        {
            id: 5,
            name: "Michael Brown",
            userId: "#SPK1005",
            product: "Leather Watch",
            orderedDate: "2024-10-01",
            orderedTime: "05:40PM",
            status: "Shipped",
            totalAmount: "$500.00",
            paymentMethod: "PayPal",
            paymentDetails: "PayPal App"
        }
    ]);

    return (
        <div className="page">
            <div className="users-section">
                <div className="card">
                    <div className="card-header">
                        <div className="header-content">
                            <h2 className="table-title">Пользователи</h2>
                            <div className="search-section">
                                <div className="search-box">
                                    <input
                                        type="text"
                                        placeholder="Search..."
                                        value={searchQuery}
                                        onChange={(e) => setSearchQuery(e.target.value)}
                                        style={{flex: 1}}
                                        className="search-input"
                                    />
                                    <button 
                                        className="search-btn" 
                                        onClick={handleSearchClick} 
                                        disabled={loading}
                                    >
                                        {loading ? "Загрузка..." : "Поиск"}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    {loading && <p>Загрузка списка клиентов...</p>}
                    {error && <p style={{color: "red"}}>{error}</p>}
                    
                    <div className="card-body">
                        <div className="users-table-container">
                            <table className="users-table">
                                <thead>
                                    <tr>
                                        <th>ID</th>
                                        <th>Пол</th>
                                        <th>Город</th>
                                        <th>Траты за 90 дней</th>
                                        <th>Телефон</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {/*Здесь вместо users - list, но так как list пустой для примера пишу users */users.map((user) => {
                                        const isSelected = selectedClient && selectedClient.id === user.id
                                        return (
                                            <tr 
                                                key={user.id} 
                                                onClick={() => handleClientClick(user)}
                                                className={`user-row ${isSelected ? 'selected' : ''}`}
                                            >
                                                <td>
                                                    <div className="user-main-info">
                                                        <div className="user-name">{user.name}</div>
                                                        <div className="user-id">{user.userId}</div>
                                                    </div>
                                                    <div className="product-info">
                                                        <div className="product-name">{user.product}</div>
                                                    </div>
                                                </td>
                                                <td>
                                                    <div className="order-date">
                                                        <div className="date">{user.orderedDate}</div>
                                                        <div className="time">{user.orderedTime}</div>
                                                    </div>
                                                </td>
                                                <td>
                                                    {/* Город отсутствует в данных - нужно добавить поле city в user объект */}
                                                    <div className="city">{user.city || "Не указан"}</div>
                                                </td>
                                                <td className="amount-column">
                                                    <div className="amount">{user.totalAmount}</div>
                                                </td>
                                                <td>
                                                    <div className="payment-info">
                                                        <div className="payment-method">{user.paymentMethod}</div>
                                                        <div className="payment-details">{user.paymentDetails}</div>
                                                    </div>
                                                </td>
                                            </tr>
                                        )
                                    })}
                                </tbody>
                            </table>
                            
                            {/*list.length === 0 && !loading && (
                                <p style={{color: "#9ca3af", textAlign: "center", padding: "20px"}}>
                                    Нет клиентов. Введите запрос и нажмите "Поиск"
                                </p>
                            )*/}
                        </div>
                        <div className="table-footer">
                            <Pages />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
})

export default Table;