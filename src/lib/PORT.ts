export const API_URL = import.meta.env.VITE_APP_API_URL as string;

if (!API_URL) {
  throw new Error('API_URL environment variable is not defined');
}

export default API_URL;
