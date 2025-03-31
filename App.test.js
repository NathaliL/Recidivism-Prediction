import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import App from '../App';

// Create a mock Axios instance
const mock = new MockAdapter(axios);

describe('RecidiVision App', () => {
    test('renders form inputs correctly', () => {
        render(<App />);

        expect(screen.getByLabelText(/Gender:/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Race:/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Age at Release:/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Education Level:/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Supervision Risk Score/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Residence PUMA/i)).toBeInTheDocument();
        expect(screen.getByLabelText(/Jobs Per Year/i)).toBeInTheDocument();
    });

    test('shows loading spinner when submitting', async () => {
        render(<App />);
        
        // Mock API response
        mock.onPost('http://127.0.0.1:5000/predict').reply(200, {
            prediction: "Recidivist",
            probabilities: { "Non-Recidivist": 0.3, "Recidivist": 0.7 },
            explanation_text: "Test explanation"
        });

        const predictButton = screen.getByText(/Predict/i);
        fireEvent.click(predictButton);

        // Expect loading spinner to appear
        expect(screen.getByRole('status')).toBeInTheDocument();

        // Wait for API response
        await waitFor(() => {
            expect(screen.getByText(/Prediction:/i)).toBeInTheDocument();
        });

        // Spinner should disappear
        expect(screen.queryByRole('status')).not.toBeInTheDocument();
    });

    test('displays prediction results correctly', async () => {
        render(<App />);

        mock.onPost('http://127.0.0.1:5000/predict').reply(200, {
            prediction: "Recidivist",
            probabilities: { "Non-Recidivist": 0.3, "Recidivist": 0.7 },
            explanation_text: "Test explanation"
        });

        fireEvent.click(screen.getByText(/Predict/i));

        await waitFor(() => {
            expect(screen.getByText(/Prediction: Recidivist/i)).toBeInTheDocument();
        });

        fireEvent.click(screen.getByText(/Show Explanation/i));

        expect(screen.getByText(/Test explanation/i)).toBeInTheDocument();
    });

    test('displays an error if API call fails', async () => {
        render(<App />);

        mock.onPost('http://127.0.0.1:5000/predict').reply(500);

        fireEvent.click(screen.getByText(/Predict/i));

        await waitFor(() => {
            expect(console.error).toHaveBeenCalled();
        });

        expect(screen.queryByText(/Prediction:/i)).not.toBeInTheDocument();
    });
});
