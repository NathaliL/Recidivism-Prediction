import React, { useState } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Modal, Button, Spinner, OverlayTrigger,Tooltip} from 'react-bootstrap';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, Colors } from 'chart.js/auto';
import './Prediction.css';

function Prediction() {
    const [formData, setFormData] = useState({
        gender: '',
        race: '',
        age_at_release: '',
        education_level: '',
        supervision_risk_score_first: '',
        residence_puma: '',
        jobs_per_year: ''
    });

    const [result, setResult] = useState(null);
    const [showModal, setShowModal] = useState(false);
    const [showExplanation, setShowExplanation] = useState(false);
    const [loading, setLoading] = useState(false);
    const [errors, setErrors] = useState({});

    const handleChange = (e) => {
        const { name, value } = e.target;
        let numericValue = Number(value);
        let errorMessage = "";


        // UI Validation - Show error but allow typing

        if (name === "age_at_release") {
            if (!Number.isInteger(numericValue)) {
                errorMessage = "Age must be a whole number.";
            } else if (numericValue < 18 || numericValue > 80) {
                errorMessage = "Age must be between 18 and 80.";
            }
        }
        
        if (name === "residence_puma") {
            if (!Number.isInteger(numericValue)) {
                errorMessage = "Residence PUMA must be a whole number.";
            } else if (numericValue < 1 || numericValue > 25) {
                errorMessage = "Residence PUMA must be between 1 and 25.";
            }
        }
        
        if (name === "supervision_risk_score_first") {
            if (!Number.isInteger(numericValue)) {
                errorMessage = "Supervision Risk Score must be a whole number.";
            } else if (numericValue < 1 || numericValue > 10) {
                errorMessage = "Supervision Risk Score must be between 1 and 10.";
            }
        }
        
        if (name === "jobs_per_year") {
            if (numericValue < 0 || numericValue > 8) {
                errorMessage = "Jobs Per Year must be between 0 and 8.";
            }
        }
        

        setErrors({ ...errors, [name]: errorMessage });
        setFormData({ ...formData, [name]: value });
    };

    // Check if form is valid: all fields filled and no errors
    const isFormValid = 
    formData.gender &&
    formData.race &&
    formData.age_at_release &&
    formData.education_level &&
    formData.supervision_risk_score_first &&
    formData.residence_puma &&
    formData.jobs_per_year &&
    Object.values(errors).every((error) => error === "");


    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setResult(null);

        try {
            const response = await axios.post('http://127.0.0.1:5000/predict', formData);
            setResult(response.data);
            setShowModal(true);
            setShowExplanation(false);
        } catch (error) {
            console.error("Error making prediction", error);
        } finally {
            setLoading(false);
        }
    };

    const chartData = result?.probabilities ? {
        labels: ['Non-Recidivist', 'Recidivist'],
        datasets: [
            {
                label: 'Probability',
                data: [result.probabilities["Non-Recidivist"], result.probabilities["Recidivist"]],
                backgroundColor: ['#4caf50', '#f44336'],
                borderColor: ['#388e3c', '#c62828'],
                borderWidth: 1,
            }
        ]
    } : {};

    return (
        <div className="container mt-5">
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="gender">Gender:</label>
                    <OverlayTrigger placement="top" overlay={<Tooltip>The self-identified gender of the individual.</Tooltip>}>
                    <select
                        name="gender"
                        className="form-control"
                        value={formData.gender}
                        onChange={handleChange}
                        required
                    >
                        <option value="" disabled>Select Gender</option>
                        <option value="M">Male</option>
                        <option value="F">Female</option>
                    </select>
                    </OverlayTrigger>
                </div>
                <div className="form-group">
                    <label htmlFor="race">Race:</label>
                    <OverlayTrigger placement="top" overlay={<Tooltip>The racial or ethnic background of the individual.</Tooltip>}>
                    <select
                        name="race"
                        className="form-control"
                        value={formData.race}
                        onChange={handleChange}
                        required
                    >
                        <option value="" disabled>Select Race</option>
                        <option value="BLACK">Black</option>
                        <option value="WHITE">White</option>
                    </select>
                    </OverlayTrigger>
                </div>
                <div className="form-group">
                    <label htmlFor="age_at_release">Age at Release:</label>
                    <OverlayTrigger placement="top" overlay={<Tooltip>The age of the individual at the time of release from prison.</Tooltip>}>
                    <input
                        type="number"
                        name="age_at_release"
                        className="form-control"
                        value={formData.age_at_release}
                        onChange={handleChange}
                        required
                    />
                    </OverlayTrigger>
                    
                    {errors.age_at_release && <small className="text-danger">{errors.age_at_release}</small>}
                    
                </div>
                <div className="form-group">
                    <label htmlFor="education_level">Education Level:</label>
                    <OverlayTrigger placement="top" overlay={<Tooltip>The highest level of education completed by the individual.</Tooltip>}>
                    <select
                        name="education_level"
                        className="form-control"
                        value={formData.education_level}
                        onChange={handleChange}
                        required
                    >
                        <option value="" disabled>Select Education Level</option>
                        <option value="Less Than High School Diploma">Less Than High School Diploma</option>
                        <option value="High School Diploma">High School Diploma</option>
                        <option value="At Least Some College">At Least Some College</option>
                    </select>
                    </OverlayTrigger>
                </div>
                <div className="form-group">
                    <label htmlFor="supervision_risk_score_first">Supervision Risk Score:</label>
                    <OverlayTrigger placement="top" overlay={<Tooltip>A numerical risk score indicating the likelihood of violating parole or reoffending.</Tooltip>}>
                    <input
                        type="number"
                        name="supervision_risk_score_first"
                        className="form-control"
                        value={formData.supervision_risk_score_first}
                        onChange={handleChange}
                        required
                    />
                    </OverlayTrigger>
                    {errors.supervision_risk_score_first && <small className="text-danger">{errors.supervision_risk_score_first}</small>}
                    
                </div>
                <div className="form-group">
                    <label htmlFor="residence_puma">Residence PUMA:</label>
                    <OverlayTrigger placement="top" overlay={<Tooltip>The Public Use Microdata Area (PUMA) code where the individual resides.</Tooltip>}>
                    <input
                        type="number"
                        name="residence_puma"
                        className="form-control"
                        value={formData.residence_puma}
                        onChange={handleChange}
                        required
                    />
                    </OverlayTrigger>
                    {errors.residence_puma && <small className="text-danger">{errors.residence_puma}</small>}
                    
                </div>
                <div className="form-group">
                    <label htmlFor="jobs_per_year">Jobs Per Year:</label>
                    <OverlayTrigger placement="top" overlay={<Tooltip>The number of jobs held per year by the individual.</Tooltip>}>
                    <input
                        type="number"
                        name="jobs_per_year"
                        className="form-control"
                        value={formData.jobs_per_year}
                        onChange={handleChange}
                        required
                    />
                    </OverlayTrigger>
                    {errors.jobs_per_year && <small className="text-danger">{errors.jobs_per_year}</small>}
                    
                </div>
                <button 
    type="submit" 
    className="btn submit-btn" 
    disabled={!isFormValid || loading}
>
    {loading ? (
        <>
            <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
            &nbsp; Predicting...
        </>
    ) : "Predict"}
</button>

            </form>

           
            <Modal show={showModal} onHide={() => setShowModal(false)} centered>
                <Modal.Header closeButton className="modal-header-custom">
                    <Modal.Title>Prediction Report</Modal.Title>
                </Modal.Header>
                <Modal.Body className="modal-body-custom">
                    {result && (
                        <>
                            <h4 className="prediction-text">Prediction: <span>{result.prediction}</span></h4>
                            {showExplanation ? (
                                <>
                                    <h5 className="lime-title">Explanation</h5>
                                    <Bar data={chartData} options={{ responsive: true }} />
                                    <ul className="explanation-list">
                                        {result.explanation_text.split("\n").map((line, index) => (
                                            line.trim() && <li key={index}>{line}</li>
                                        ))}
                                    </ul>
                                </>
                            ) : (
                                <Button 
                                    variant="info" 
                                    onClick={() => setShowExplanation(true)}
                                    className="explanation-btn"
                                >
                                    Show Explanation
                                </Button>
                            )}
                        </>
                    )}
                </Modal.Body>
                <Modal.Footer className="modal-footer-custom">
                    <Button variant="secondary" onClick={() => setShowModal(false)}>Close</Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}

export default Prediction;
