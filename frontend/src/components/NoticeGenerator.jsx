import React, { useState, useRef, useMemo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { default as SimpleMDE } from "react-simplemde-editor";
import "easymde/dist/easymde.min.css";

import { useReactToPrint } from "react-to-print";

import {
	FileText,
	RotateCcw,
	Calendar,
	MapPin,
	Users,
	StickyNote,
	Lightbulb,
	Flashlight,
	Languages,
	ChartBarStacked,
	Contact,
	Hash,
	Mail,
	Info,
} from "lucide-react";
import "./NoticeGenerator.css";

export default function NoticeGenerator() {
	const [formData, setFormData] = useState({
		title: "",
		body: "",
		date: "",
		location: "",
		language: "",
		audience: "",
		category: "",
		department: "",
		contact_officer: "",
		contact_number: "",
		email: "",
		additional_notes: "",
		// promptTips: '',
	});
	// //debugging
	// const [formData, setFormData] = useState(dummyData);
	const [generatedNotice, setGeneratedNotice] = useState();

	const handleInputChange = (e) => {
		const { name, value } = e.target;
		setFormData((prev) => ({
			...prev,
			[name]: value,
		}));

		if (value.trim() !== "") {
			setInvalidFields((prev) => prev.filter((field) => field !== name));
		}
	};

	const handleReset = () => {
		setFormData({
			title: "",
			body: "",
			date: "",
			location: "",
			language: "",
			audience: "",
			category: "",
			department: "",
			contact_officer: "",
			contact_number: "",
			email: "",
			additional_notes: "",
			// promptTips: '',
		});
		setGenerating(false);
		setGeneratedNotice("");
	};

	//helper
	const [invalidFields, setInvalidFields] = useState([]);
	const checkEmpty = () => {
		const requiredFields = { ...formData };
		delete requiredFields.additional_notes;

		const emptyFields = Object.entries(requiredFields)
			.filter(([key, value]) => value.trim() === "")
			.map(([key]) => key);

		setInvalidFields(emptyFields);

		return emptyFields.length === 0;
	};
	const [generating, setGenerating] = useState(false);
	const [copied, setCopied] = useState(false);
	const handleCopy = () => {
		navigator.clipboard.writeText(generatedNotice).then(() => {
			setCopied(true);
			setTimeout(() => setCopied(false), 2000); // hide after 2s
		});
	};

	//api call
	const handleGenerateNotice = async () => {
		if (!checkEmpty()) {
			return;
		}

		try {
			setGenerating(true);
			console.log("Date: ", formData);
			const jsonData = JSON.stringify(formData);
			const response = await fetch(
				"https://civicnotice.onrender.com/generate_notice/",
				{
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: jsonData,
				}
			);
			const data = await response.json();
			console.log("Response Data:", data);

			if (response.ok) {
				//   setGeneratedNotice(data.message);
				setGeneratedNotice(data.message.trim().replace(/^```|```$/g, " "));
				setGenerating(false);
			} else {
				setGeneratedNotice(data.detail[0].msg);
				setGenerating(false);
			}
		} catch (error) {
			console.log(error);
			setGenerating(false);
			setGeneratedNotice("Error Fetching Data from Server");
		}
	};

	//simplemde options
	const simpleMDEOptions = useMemo(
		() => ({
			spellChecker: false,
			autofocus: true,
			toolbar: [
				"bold",
				"italic",
				"heading",
				"|",
				"quote",
				"unordered-list",
				"ordered-list",
				"|",
				"link",
				"image",
				"|",
				"preview",
				"side-by-side",
				"fullscreen",
				"|",
				"guide",
			],
			status: false,
			placeholder: "Edit your notice here...",
		}),
		[]
	);

	const previewRef = useRef(null);
	//For lazyloading
	const reactToPrintContent = () => {
		return previewRef.current;
	};

	const downloadAsPDF = useReactToPrint({
		documentTitle: "Notice",
	});

	return (
		<div className="container">
			<div className="main-card">
				<div className="header">
					<div className="header-title">
						<FileText size={48} color="#0d9488" />
						<h1 className="title">Civic Notice</h1>
					</div>
					<p className="subtitle">
						Create professional notices quickly and easily
					</p>
				</div>
				<div className="grid-container" ref={previewRef}>
					<div className="form-section">
						<h2 className="section-title">Notice Details</h2>

						<div className="input-group">
							<label className="label">
								<FileText size={16} className="label-icon" />
								Title
							</label>
							<input
								type="text"
								name="title"
								value={formData.title}
								onChange={handleInputChange}
								className={`input ${
									invalidFields.includes("title") ? "input-error" : ""
								}`}
								placeholder="Enter notice title"
							/>
						</div>

						<div className="input-group">
							<label className="label">
								<StickyNote size={16} className="label-icon" />
								Body
								<div className="info-icon-wrapper">
									<Info size={16} className="info-icon" />
									<span className="tooltip-text">
										Provide detailed and specific content you want to include in
										the notice. The more context you give, the better the AI can
										generate a professional and accurate notice.
									</span>
								</div>
							</label>

							<textarea
								name="body"
								value={formData.body}
								onChange={handleInputChange}
								className={`textarea ${
									invalidFields.includes("body") ? "input-error" : ""
								}`}
								placeholder="Enter notice body content"
								rows="4"
							/>
						</div>

						<div className="input-container-group">
							<div className="input-group">
								<label className="label">
									<Calendar size={16} className="label-icon" />
									Date
								</label>
								<input
									type="date"
									name="date"
									value={formData.date}
									onChange={handleInputChange}
									className={`input ${
										invalidFields.includes("date") ? "input-error" : ""
									}`}
								/>
							</div>

							<div className="input-group">
								<label className="label">
									<MapPin size={16} className="label-icon" />
									Location
								</label>
								<input
									type="text"
									name="location"
									value={formData.location}
									onChange={handleInputChange}
									className={`input ${
										invalidFields.includes("location") ? "input-error" : ""
									}`}
									placeholder="Enter location"
								/>
							</div>
						</div>

						<div className="input-group">
							<label className="label">
								<Users size={16} className="label-icon" />
								Audience
							</label>
							<input
								type="text"
								name="audience"
								value={formData.audience}
								onChange={handleInputChange}
								className={`input ${
									invalidFields.includes("audience") ? "input-error" : ""
								}`}
								placeholder="Enter target audience"
							/>
						</div>

						<div className="input-container-group">
							<div className="input-group">
								<label className="label">
									<ChartBarStacked size={16} className="label-icon" />
									Category
								</label>
								<input
									type="text"
									name="category"
									value={formData.category}
									onChange={handleInputChange}
									className={`input ${
										invalidFields.includes("category") ? "input-error" : ""
									}`}
									placeholder="Enter category"
								/>
							</div>
							<div className="input-group">
								<label className="label">
									<Languages size={16} className="label-icon" />
									Language
								</label>
								<select
									name="language"
									value={formData.language}
									onChange={handleInputChange}
									className={`input ${
										invalidFields.includes("language") ? "input-error" : ""
									}`}>
									{/* <option value="">Select Language</option> */}
									<option value="English">English</option>
									<option value="Hindi">Hindi</option>
									<option value="Marathi">Marathi</option>
									{/* <option value="Gujarati">Gujarati</option>
                  <option value="Tamil">Tamil</option>
                  <option value="Telugu">Telugu</option>
                  <option value="Bengali">Bengali</option> */}
									{/* Add more languages as needed */}
								</select>
							</div>
						</div>

						<div className="input-container-group">
							<div className="input-group">
								<label className="label">
									<FileText size={16} className="label-icon" />
									Department
								</label>
								<input
									type="text"
									name="department"
									value={formData.department}
									onChange={handleInputChange}
									className={`input ${
										invalidFields.includes("department") ? "input-error" : ""
									}`}
									placeholder="Enter department"
								/>
							</div>

							<div className="input-group">
								<label className="label">
									<Contact size={16} className="label-icon" />
									Contact Officer
								</label>
								<input
									type="text"
									name="contact_officer"
									value={formData.contact_officer}
									onChange={handleInputChange}
									className={`input ${
										invalidFields.includes("contact_officer")
											? "input-error"
											: ""
									}`}
									placeholder="Enter contact officer"
								/>
							</div>
						</div>

						<div className="input-container-group">
							<div className="input-group">
								<label className="label">
									<Hash size={16} className="label-icon" />
									Contact Number
								</label>
								<input
									type="text"
									name="contact_number"
									value={formData.contact_number}
									onChange={handleInputChange}
									className={`input ${
										invalidFields.includes("contact_number")
											? "input-error"
											: ""
									}`}
									placeholder="Enter contact number"
								/>
							</div>

							<div className="input-group">
								<label className="label">
									<Mail size={16} className="label-icon" />
									Email
								</label>
								<input
									type="text"
									name="email"
									value={formData.email}
									onChange={handleInputChange}
									className={`input ${
										invalidFields.includes("email") ? "input-error" : ""
									}`}
									placeholder="Enter email"
								/>
							</div>
						</div>

						<div className="input-group">
							<label className="label">
								<StickyNote size={16} className="label-icon" />
								Notes
								<div className="info-icon-wrapper">
									<Info size={16} className="info-icon" />
									<span className="tooltip-text">
										Include any extra instructions, tone preferences, or
										background information. This helps the AI tailor the notice
										more precisely to your needs.
									</span>
								</div>
							</label>
							<textarea
								name="additional_notes"
								value={formData.additional_notes}
								onChange={handleInputChange}
								className={`textarea ${
									invalidFields.includes("additional_notes")
										? "input-error"
										: ""
								}`}
								placeholder="Additional notes or instructions"
								rows="3"
							/>
						</div>

						{/* <div className="input-group">
              <label className="label">
                <Lightbulb size={16} className="label-icon" />
                Prompt Tips
              </label>
              <textarea
                name="promptTips"
                value={formData.promptTips}
                onChange={handleInputChange}
                className="textarea"
                placeholder="Tips for improving the notice"
                rows="3"
              />
            </div> */}

						<div className="button-container">
							<button
								onClick={handleGenerateNotice}
								className="button primary-button">
								<FileText size={20} />
								Generate Notice
							</button>
							<button onClick={handleReset} className="button secondary-button">
								<RotateCcw size={20} />
								Reset
							</button>
						</div>
					</div>

					<div className="preview-section">
						<h2 className="section-title">Generated Notice</h2>

						<div className="preview-container">
							{generating ? (
								<div className="load">
									<div className="loader-inside"></div>
									Loading
								</div>
							) : generatedNotice ? (
								<div className="preview-content">
									{/*                      
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
               
                    {generatedNotice}
                  </ReactMarkdown> */}
									{/* <div className="preview-content">{generatedNotice}</div> */}

									<SimpleMDE
										key="notice-editor"
										value={generatedNotice}
										onChange={(value) => setGeneratedNotice(value)}
										options={simpleMDEOptions}
									/>
								</div>
							) : (
								<div className="empty-preview">
									<div className="empty-preview-content">
										<FileText
											size={64}
											color="#ccc"
											style={{ marginBottom: "15px" }}
										/>
										<p style={{ fontSize: "1.2rem", margin: "0 0 5px 0" }}>
											Your generated notice will appear here
										</p>
										<p style={{ fontSize: "0.9rem", margin: "0" }}>
											Fill in the details and click "Generate Notice"
										</p>
									</div>
								</div>
							)}
						</div>

						{generatedNotice && (
							<div className="button-container">
								{copied && (
									<div className="copy-wrapper">
										<span className="copy-text">Copied</span>
									</div>
								)}

								<button onClick={handleCopy} className="copy-button">
									Copy to Clipboard
								</button>
								<button
									onClick={() => {
										console.log(previewRef.current);
										downloadAsPDF(reactToPrintContent);
									}}
									className="copy-button">
									Download as PDF
								</button>
							</div>
						)}
					</div>
				</div>
				{/* for PDF Generation offscreen-preview // final-preview */}

				<div ref={previewRef} className="offscreen-preview">
					<ReactMarkdown remarkPlugins={[remarkGfm]}>
						{generatedNotice}
					</ReactMarkdown>
				</div>
			</div>
		</div>
	);
}

const dummyData = {
	title: "Temporary Power Shortage Notice",
	body: "Residents are hereby informed that due to an unexpected load management issue from the local power grid, our CHS will experience intermittent power supply on 28th June 2025. The Maharashtra State Electricity Distribution Company Limited (MSEDCL) has assured us that normal supply will resume by evening.",
	date: "28/06/2025",
	location: "Sai Krupa CHS, Sector 17, Vashi, Navi Mumbai",
	language: "English",
	audience: "All Residents of Sai Krupa CHS",
	category: "Electricity Disruption",
	department: "Building Maintenance Committee",
	contact_officer: "Mr. Ramesh Patil (Secretary)",
	contact_number: "9819456723",
	email: "saikrupachs.vashi@gmail.com",
	additional_notes:
		"Residents are requested to conserve electricity and avoid using heavy appliances during peak hours. Generator backup will be available for elevators and essential services only.",
};

const dummyNotice = `
    **

**SAI KRUPA CO-OPERATIVE HOUSING SOCIETY LTD.**
Sector 17, Vashi, Navi Mumbai – 400703
(Maharashtra, India)

**PUBLIC NOTICE**

**Ref. No.:** SKCHS/MAINT/2025/06/001
**Date:** 28/06/2025

**Subject: Intimation Regarding Temporary Power Supply Disruption**

To: All Residents of Sai Krupa Co-operative Housing Society Ltd.

This notice is to inform all esteemed residents of Sai Krupa Co-operative Housing Society Ltd. of an anticipated intermittent disruption in power supply scheduled for today, 28th June 2025. This disruption is a consequence of unforeseen load management challenges communicated by the Maharashtra State Electricity Distribution Company Limited (MSEDCL).

MSEDCL has assured the Society that diligent efforts are underway to restore normal power supply by evening. We understand this may cause inconvenience, and we sincerely regret any disruption to your daily routine.

Residents are kindly requested to exercise judicious use of electricity and refrain from operating high-consumption appliances during peak hours to mitigate the overall impact of the power disruption. Generator backup will be prioritized for elevators and essential services to ensure the continued well-being of all residents.

**Grievance Redressal Mechanism:**

In case of any grievances or concerns related to the power disruption, residents are requested to contact the Building Maintenance Committee through the provided channels. The Committee will address concerns promptly and efficiently.

**Right to Information (RTI) Act, 2005:**

As per the provisions of the Right to Information Act, 2005, residents can seek information pertaining to this notice. Please direct your inquiries to the Secretary of the Society for further details and clarifications.

**Contact Information:**

Mr. Ramesh Patil
Secretary
Building Maintenance Committee
Contact Number: 9819456723
Email: saikrupachs.vashi@gmail.com

**By Order of the Managing Committee,**

[Signature]

Mr. Ramesh Patil
Secretary
Sai Krupa Co-operative Housing Society Ltd.
Sector 17, Vashi, Navi Mumbai – 400703

`;
