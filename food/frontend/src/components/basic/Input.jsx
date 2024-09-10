const Input = ({value, className, label, name, max, min, placeholder, type, onChange}) => {
				const inputClass = ["input-field", className].join(' ')
				return (
								<div className={"input-wrapper"}>
												{label && <label htmlFor={name}>{label}</label>}
												<input
																className={inputClass}
																type={type}
																value={value}
																name={name}
																max={max}
																min={min}
																placeholder={placeholder}
																onChange={(e) => onChange(name, e.target.value)}
												/>
								</div>
				)
}

export default Input;
