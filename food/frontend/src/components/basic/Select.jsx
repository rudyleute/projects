const Select = ({data, placeholder, value, onChange}) => {
				const options = data.map((item) => {
								return <option key={item.id} title={item?.title ?? ''} value={item.value}>{item.value}</option>
				})

				const handleChange = (event) => {
								const selectedValue = event.target.value;
								const newOption = data.find(option => option.value === selectedValue);
								if (newOption) {
												onChange({id: newOption.id, value: newOption.value})
								}
				};

				return (
								<div className={"select-wrapper"}>
												<select value={value?.value ?? ""} onChange={handleChange}>
																<option value={""}>{placeholder ?? "Choose the option"}</option>
																{options}
												</select>
								</div>
				)
}

export default Select;