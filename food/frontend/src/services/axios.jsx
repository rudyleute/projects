import axios from "axios";
import errorsParser from "./errorsParser.jsx";

const instance = axios.create({
				headers: {
								'Content-Type': 'application/json',
				}
})

const axiosRequest = async (method, endpoint, id = null, data = {}) => {
				const uri = `/api/${endpoint}/${id ?? ''}`
				const requestConfig = { method, url: uri, data }
				const result = {}

				try {
								const {data} = await instance(requestConfig);
								result.data = data;
				} catch (error) {
								result.error = errorsParser(error);
				}

				return result;
}

export default axiosRequest;