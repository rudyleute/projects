const errorParser = ({request, response, message}) => {
				console.log(request, response, message);
				let error;
				if (request?.statusText) error = request.statusText;
				else if (message) error = message

				return error;
}

export default errorParser;

