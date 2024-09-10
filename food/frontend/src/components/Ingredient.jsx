import {useEffect, useState} from "react";
import axiosRequest from "../services/axios.jsx";
import Select from "../components/basic/Select.jsx";

const Ingredient = () => {
				const [list, setList] = useState([]);
				useEffect(() => {
								const retrieveElements = async () => {
												const {data, error} = await axiosRequest('get', 'brand');
												if (!error) setList(data);
								}

								retrieveElements().catch((error) => {alert(error)});
				}, [])

				return (
								<>
												<Select data={list} handleSelectChange={(aux) => console.log(aux)}/>
								</>
				)
}

export default Ingredient;