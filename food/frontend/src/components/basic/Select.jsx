import {useState, useEffect} from "react";

const Select = ({data, placeholder, handleSelectChange}) => {
				const [options, setOptions] = useState([])
				const [selectedOption, setSelectedOption] = useState({})

				useEffect(() => {
								setOptions(data.map((item) => {
												return <option key={item.id} value={item.name}>{item.name}</option>
								}))
				}, [data])

				const handleChange = (event) => {
								const selectedValue = event.target.value;
								const newOption = options.find(option => option.props.value === selectedValue);
								if (newOption) {
												setSelectedOption(newOption)
												handleSelectChange(newOption)
								}
				};

				return (
								<select value={selectedOption.props?.value ?? ""} onChange={handleChange}>
												<option value={""}>{placeholder ?? "Choose the option"}</option>
												{options}
								</select>
				)
}

export default Select;