import axios from 'axios';

export const apiRequest = async (endpoint, payload) => {
  try {
    const response = await axios.post(`http://localhost:5000/${endpoint}`, payload);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Server error');
  }
};
