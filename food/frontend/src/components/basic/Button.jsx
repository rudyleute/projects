const Button = ({ children, className, type, onSubmit, onClick }) => {
				const buttonClassName = ["", className].join(" ");

				return (
								<button
												className={buttonClassName}
												type={type}
												onClick={onClick}
												onSubmit={onSubmit}
								>
												{children}
								</button>
				)
}

export default Button;