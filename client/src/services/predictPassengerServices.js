import axios from "axios";

// aqui ira nuestros servicios en donde haremos peticiones a la API 

const BASE_URL = "http://localhost:8000";

export const getPredictPassenger = async (data) => {
    const response = await axios.post(`${BASE_URL}/predict`, data);
    return response.data;
};