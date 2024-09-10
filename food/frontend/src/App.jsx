import {BrowserRouter, Routes, Route} from "react-router-dom";
import Consumption from "./pages/Consumption.jsx";
import Layout from "./pages/Layout.jsx";
import NoPage from "./pages/NoPage.jsx";

function App() {
				return (
								<BrowserRouter>
												<Routes>
																<Route path="/">
																				<Route index element={<Layout />} />
																				<Route path="consumption" element={<Consumption />} />
																				<Route path="*" element={<NoPage />} />
																</Route>
												</Routes>
								</BrowserRouter>
				)
}

export default App
