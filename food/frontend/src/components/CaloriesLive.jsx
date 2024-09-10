import {useEffect, useState} from "react";
import axiosRequest from "../services/axios.jsx";
import Input from "./basic/Input.jsx";
import Select from "./basic/Select.jsx";
import Button from "./basic/Button.jsx";

const CaloriesLive = () => {
	const [showCalculations, setShowCalculations] = useState(false);
	const [activities, setActivities] = useState([]);
	const [formValues, setFormValues] = useState({
		age: 0, weight: 0, height: 0, activity: {},
	});

	useEffect(() => {
		const retrieveElements = async () => {
			const {data, error} = await axiosRequest('get', 'activity_level');
			if (!error) setActivities(data.map(({id, name, description, multiplier}) => {
				return {id, value: name, title: description, multiplier};
			}));
		}

		retrieveElements().catch((error) => {
			alert(error)
		});
	}, [])

	const onFormSubmit = (e) => {
		e.preventDefault()
		setShowCalculations(!showCalculations)
	}

	const onInputChange = (name, value) => {
		setFormValues({...formValues, [name]: parseInt(value)});
	}

	const onActivityChange = (value) => {
		setFormValues({...formValues, "activity": activities.find(option => option.id === value.id)});
	}

	return (
		<>
			{
				showCalculations &&
				<div className={"calories"}>
					<span className={"calories-goal"}>
						{Math.round(0.8 * (5 + 10 * formValues.weight + 6.25 * formValues.height - 5 * formValues.age) * formValues.activity.multiplier)}
					</span><br/>
					<span className={"calories-overall"}>
						{Math.round((5 + 10 * formValues.weight + 6.25 * formValues.height - 5 * formValues.age) * formValues.activity.multiplier)}
					</span>
				</div>
			}
			<form className={"form"} onSubmit={onFormSubmit}>
				<Input
					type={"number"}
					value={formValues.age || ''}
					name={"age"}
					min={18}
					max={80}
					onChange={onInputChange}
					label={"Age"}
				/>
				<Input
					type={"number"}
					value={formValues.height || ''}
					name={"height"}
					min={130}
					max={240}
					onChange={onInputChange}
					label={'Height'}
				/>
				<Input
					type={"number"}
					value={formValues.weight || ''}
					name={"weight"}
					min={30}
					max={250}
					onChange={onInputChange}
					label={"Weight"}
				/>
				<Select data={activities} value={formValues.activity} onChange={onActivityChange}/>
				<Button onSubmit={onFormSubmit} type={"submit"}>{showCalculations ? "Edit" : "Calculate"}</Button>
			</form>
		</>)
}

export default CaloriesLive;