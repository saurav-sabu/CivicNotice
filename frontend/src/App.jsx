import { useEffect, useState } from "react";
import "./App.css";
import NoticeGenerator from "./components/NoticeGenerator";

function App() {
	const [serverConnected, setServerConnected] = useState(false);

	useEffect(() => {
		const checkServerConnection = async () => {
			try {
				setServerConnected(false);
				const response = await fetch("https://civicnotice.onrender.com");
				if (response.ok) {
					setServerConnected(true);
				} else {
					console.error("Server responded, but with an error.");
				}
			} catch (error) {
				console.error("Error connecting to server:", error);
				setServerConnected(false);
			}
		};

		checkServerConnection();
	}, []);

	return (
		<>
			{serverConnected ? (
				<NoticeGenerator />
			) : (
				<div className="loading-preview">
					<div className="loader"></div>Booting up the servers... Almost there!
				</div>
			)}
		</>
	);
}

export default App;
